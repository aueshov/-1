import time
import config
from analyzer import patch_time
from trader import get_client, get_balance, set_leverage, open_trade, get_klines
from indicators import calculate_indicators, get_market_data
from market_analyzer import analyze_market
from ai_advisor import get_ai_decision
from risk_manager import RiskManager
from telegram_bot import notify, trade_message, wait_message

def main():
    patch_time()
    print("🤖 Кәсіби Trading Bot іске қосылды!")
    notify("🤖 <b>Кәсіби Trading Bot іске қосылды!</b>\n\nНарықты бақылап жатырмын...")

    client = get_client()
    set_leverage(client, config.SYMBOL, config.LEVERAGE)
    risk = RiskManager()

    while True:
        try:
            print("\n" + "="*50)
            print("📊 Анализ жасалуда...")

            # 1. Деректер алу
            df = get_klines(client, config.SYMBOL, config.TIMEFRAME)

            # 2. Индикаторлар есептеу
            df = calculate_indicators(df)
            data = get_market_data(df)

            print(f"💰 BTC: ${data['price']:,.2f}")
            print(f"📈 RSI: {data['rsi']:.1f}")
            print(f"📊 Нарық: ", end="")

            # 3. Нарық анализі
            market_result = analyze_market(data)
            print(market_result['market_mode'])
            print(f"🎯 LONG: {market_result['long_pct']}% / SHORT: {market_result['short_pct']}%")

            # 4. AI шешімі
            print("🤖 AI анализ жасауда...")
            ai_result = get_ai_decision(data, market_result)
            print(f"🤖 AI: {ai_result['decision']} ({ai_result['confidence']}%)")
            print(f"💬 {ai_result['reason']}")

            # 5. Риск тексеру
            can_trade, reason = risk.can_trade()

            # 6. Сделка шешімі
            if (ai_result['decision'] in ['LONG', 'SHORT'] and
                ai_result['confidence'] >= config.MIN_AI_CONFIDENCE and
                ai_result['risk'] != 'ЖОҒАРЫ' and
                can_trade):

                direction = ai_result['decision']
                balance = get_balance(client)
                print(f"💰 Баланс: ${balance:,.2f}")

                position = risk.calculate_position(
                    balance, data['price'], data['atr'], direction
                )

                print(f"🚀 Сделка ашылуда: {direction}")
                print(f"📦 Мөлшер: {position['qty']}")
                print(f"🛡 SL: ${position['sl_price']:,.2f}")
                print(f"🎯 TP: ${position['tp_price']:,.2f}")

                order = open_trade(client, config.SYMBOL, direction, position)

                if order:
                    print("✅ Сделка сәтті ашылды!")
                    risk.register_trade(0)
                    msg = trade_message(direction, data, market_result, ai_result, position)
                    notify(msg)
                else:
                    print("❌ Сделка ашылмады")

            else:
                if not can_trade:
                    print(f"⛔ {reason}")
                elif ai_result['confidence'] < config.MIN_AI_CONFIDENCE:
                    print(f"⏳ AI сенімділігі төмен: {ai_result['confidence']}%")
                elif ai_result['risk'] == 'ЖОҒАРЫ':
                    print("⚠️ Тәуекел жоғары — күтуде")
                else:
                    print("⏳ Сигнал жоқ — күтуде")

            stats = risk.get_stats()
            print(f"📊 Бүгін: {stats['daily_trades']} сделка | Қалды: {stats['remaining_trades']}")
            print(f"⏰ 15 минут күтуде...")
            time.sleep(900)

        except Exception as e:
            error_msg = f"❌ Қате: {str(e)}"
            print(error_msg)
            notify(error_msg)
            time.sleep(60)

if __name__ == "__main__":
    main()
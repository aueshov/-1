import asyncio
from telegram import Bot
import config

async def send_message(text):
    bot = Bot(token=config.TELEGRAM_TOKEN)
    await bot.send_message(
        chat_id=config.TELEGRAM_CHAT_ID,
        text=text,
        parse_mode='HTML'
    )

def notify(text):
    try:
        asyncio.run(send_message(text))
    except Exception as e:
        print(f"Telegram қатесі: {e}")

def trade_message(direction, data, market_result, ai_result, position):
    emoji = "🟢" if direction == "LONG" else "🔴"
    risk_emoji = {"ТӨМЕН": "🟢", "ОРТАША": "🟡", "ЖОҒАРЫ": "🔴"}.get(ai_result['risk'], "⚪")

    signals_text = "\n".join(market_result['signals'])

    return f"""
{emoji} <b>СДЕЛКА АШЫЛДЫ: {direction}</b>

📊 <b>Жұп:</b> {config.SYMBOL}
💰 <b>Кіру бағасы:</b> ${data['price']:,.2f}
🛡 <b>Stop Loss:</b> ${position['sl_price']:,.2f} (-{position['sl_percent']:.1f}%)
🎯 <b>Take Profit:</b> ${position['tp_price']:,.2f}
📦 <b>Мөлшер:</b> {position['qty']} BTC
⚖️ <b>Risk/Reward:</b> 1:{position['rr_ratio']}

━━━━━━━━━━━━━━━━━━━━
🤖 <b>AI ШЕШІМІ</b>
━━━━━━━━━━━━━━━━━━━━
🎯 Сенімділік: <b>{ai_result['confidence']}%</b>
{risk_emoji} Тәуекел: <b>{ai_result['risk']}</b>
💬 Себеп: {ai_result['reason']}

━━━━━━━━━━━━━━━━━━━━
📈 <b>ИНДИКАТОРЛАР</b>
━━━━━━━━━━━━━━━━━━━━
- RSI: {data['rsi']:.1f}
- MACD: {data['macd']:.2f}
- Stoch K/D: {data['stoch_k']:.1f}/{data['stoch_d']:.1f}
- Волюм: {data['volume_ratio']:.1f}x
- Нарық: {market_result['market_mode']}

━━━━━━━━━━━━━━━━━━━━
🔍 <b>СИГНАЛДАР</b>
━━━━━━━━━━━━━━━━━━━━
{signals_text}

📊 LONG {market_result['long_pct']}% / SHORT {market_result['short_pct']}%
"""

def wait_message(data, market_result, ai_result):
    return f"""
⏳ <b>СИГНАЛ ЖОҚ — КҮТУДЕ</b>

💰 BTC бағасы: ${data['price']:,.2f}
📊 Нарық: {market_result['market_mode']}
🤖 AI шешімі: {ai_result['decision']} ({ai_result['confidence']}%)
📊 LONG {market_result['long_pct']}% / SHORT {market_result['short_pct']}%
"""
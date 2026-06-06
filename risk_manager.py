import config

class RiskManager:
    def __init__(self):
        self.daily_trades = 0
        self.daily_loss = 0
        self.daily_pnl = 0
        self.trade_history = []

    def can_trade(self):
        # Күнделікті сделка лимиті
        if self.daily_trades >= config.MAX_DAILY_TRADES:
            return False, f"❌ Күнделікті лимит: {self.daily_trades}/{config.MAX_DAILY_TRADES} сделка"

        # Күнделікті шығын лимиті
        if self.daily_loss >= config.MAX_DAILY_LOSS_PERCENT:
            return False, f"❌ Күнделікті шығын лимиті: -{self.daily_loss:.1f}%"

        return True, "✅ Сделка ашуға рұқсат"

    def calculate_position(self, balance, price, atr, direction):
        # ATR негізінде динамикалық Stop Loss
        sl_distance = atr * 2
        sl_percent = sl_distance / price * 100

        # Риск мөлшері
        risk_amount = balance * (config.RISK_PERCENT / 100)
        qty = round(risk_amount / sl_distance, 3)

        if qty < 0.001:
            qty = 0.001

        # Stop Loss және Take Profit
        if direction == "LONG":
            sl_price = round(price - sl_distance, 2)
            tp_price = round(price + sl_distance * 2, 2)  # RR 1:2
        else:
            sl_price = round(price + sl_distance, 2)
            tp_price = round(price - sl_distance * 2, 2)  # RR 1:2

        return {
            'qty': qty,
            'sl_price': sl_price,
            'tp_price': tp_price,
            'sl_percent': sl_percent,
            'risk_amount': risk_amount,
            'rr_ratio': 2.0
        }

    def register_trade(self, pnl_percent):
        self.daily_trades += 1
        self.daily_pnl += pnl_percent
        if pnl_percent < 0:
            self.daily_loss += abs(pnl_percent)
        self.trade_history.append(pnl_percent)

    def get_stats(self):
        return {
            'daily_trades': self.daily_trades,
            'daily_pnl': self.daily_pnl,
            'daily_loss': self.daily_loss,
            'remaining_trades': config.MAX_DAILY_TRADES - self.daily_trades
        }
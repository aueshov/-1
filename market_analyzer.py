def analyze_market(data):
    if data is None:
        return {
            'direction': None,
            'score_long': 0,
            'score_short': 0,
            'long_pct': 50,
            'short_pct': 50,
            'signals': ["⚠️ Деректер жоқ"],
            'market_mode': "БЕЛГІСІЗ"
        }

    signals = []
    score_long = 0
    score_short = 0

    try:
        # 1. EMA тренд
        if data['ema21'] > data['ema50'] > data['ema200']:
            score_long += 2
            signals.append("✅ EMA тренд: ЖОҒАРЫ (21>50>200)")
        elif data['ema21'] < data['ema50'] < data['ema200']:
            score_short += 2
            signals.append("✅ EMA тренд: ТӨМЕН (21<50<200)")
        else:
            signals.append("⚠️ EMA тренд: АРАЛАС")

        # 2. EMA кесілісі
        if data['ema21_prev'] <= data['ema50_prev'] and data['ema21'] > data['ema50']:
            score_long += 3
            signals.append("🔥 EMA кесілісі: ЖОҒАРЫҒА")
        elif data['ema21_prev'] >= data['ema50_prev'] and data['ema21'] < data['ema50']:
            score_short += 3
            signals.append("🔥 EMA кесілісі: ТӨМЕНГЕ")

        # 3. RSI
        rsi = data['rsi']
        if 45 < rsi < 65:
            score_long += 1
            signals.append(f"✅ RSI: {rsi:.1f} (қалыпты)")
        elif 35 < rsi <= 45:
            score_long += 2
            signals.append(f"✅ RSI: {rsi:.1f} (oversold жақын)")
        elif rsi >= 65:
            score_short += 1
            signals.append(f"⚠️ RSI: {rsi:.1f} (overbought жақын)")
        elif rsi <= 35:
            score_long += 2
            signals.append(f"✅ RSI: {rsi:.1f} (oversold)")

        # 4. MACD
        if data['macd'] > data['macd_signal'] and data['macd_hist'] > data['macd_hist_prev']:
            score_long += 2
            signals.append("✅ MACD: өсу импульсі")
        elif data['macd'] < data['macd_signal'] and data['macd_hist'] < data['macd_hist_prev']:
            score_short += 2
            signals.append("✅ MACD: түсу импульсі")
        else:
            signals.append("⚠️ MACD: белгісіз")

        # 5. Bollinger Bands
        price = data['price']
        if price < data['bb_lower']:
            score_long += 2
            signals.append("✅ Bollinger: сатып алу аймағы")
        elif price > data['bb_upper']:
            score_short += 2
            signals.append("✅ Bollinger: сату аймағы")
        elif price > data['bb_middle']:
            score_long += 1
            signals.append("✅ Bollinger: ортадан жоғары")
        else:
            score_short += 1
            signals.append("✅ Bollinger: ортадан төмен")

        # 6. Stochastic
        if data['stoch_k'] < 20 and data['stoch_d'] < 20:
            score_long += 2
            signals.append("✅ Stochastic: oversold")
        elif data['stoch_k'] > 80 and data['stoch_d'] > 80:
            score_short += 2
            signals.append("✅ Stochastic: overbought")

        # 7. Volume
        if data['volume_ratio'] > 1.5:
            if score_long >= score_short:
                score_long += 1
            else:
                score_short += 1
            signals.append(f"✅ Волюм: {data['volume_ratio']:.1f}x")
        else:
            signals.append(f"⚠️ Волюм: {data['volume_ratio']:.1f}x")

        # Нарық режимі
        if data['bb_width'] < 2:
            market_mode = "ФЛЕТ"
        elif data['bb_width'] > 5:
            market_mode = "ВОЛАТИЛЬДЫ"
        else:
            market_mode = "ТРЕНД"

        # Қорытынды
        total = score_long + score_short
        if total == 0:
            long_pct = 50
            short_pct = 50
        else:
            long_pct = int(score_long / total * 100)
            short_pct = int(score_short / total * 100)

        if score_long >= 8:
            direction = "LONG"
        elif score_short >= 8:
            direction = "SHORT"
        else:
            direction = None

        return {
            'direction': direction,
            'score_long': score_long,
            'score_short': score_short,
            'long_pct': long_pct,
            'short_pct': short_pct,
            'signals': signals,
            'market_mode': market_mode,
        }

    except Exception as e:
        return {
            'direction': None,
            'score_long': 0,
            'score_short': 0,
            'long_pct': 50,
            'short_pct': 50,
            'signals': [f"⚠️ Қате: {str(e)}"],
            'market_mode': "БЕЛГІСІЗ"
        }
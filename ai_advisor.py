import requests
import json
import config

def get_ai_decision(data, market_result):
    prompt = f"""Сен криптовалюта трейдерісің. Төмендегі деректерді талдап, JSON форматында жауап бер.

НАРЫҚ ДЕРЕКТЕРІ:
- Жұп: {config.SYMBOL}
- Баға: ${data['price']:,.2f}
- Нарық режимі: {market_result['market_mode']}
- EMA21: {data['ema21']:,.2f}
- EMA50: {data['ema50']:,.2f}
- EMA200: {data['ema200']:,.2f}
- RSI: {data['rsi']:.1f}
- MACD: {data['macd']:.4f}
- Stochastic K: {data['stoch_k']:.1f}
- Bollinger жоғары: {data['bb_upper']:,.2f}
- Bollinger төмен: {data['bb_lower']:,.2f}
- Волюм: {data['volume_ratio']:.2f}x
- LONG ұпайы: {market_result['score_long']}/13
- SHORT ұпайы: {market_result['score_short']}/13

Тек осы JSON форматында жауап бер, басқа ештеңе жазба:
{{"decision": "LONG", "confidence": 75, "reason": "себеп осында", "risk": "ОРТАША"}}

decision тек: LONG, SHORT, немесе WAIT
confidence: 0-100 арасында сан
risk тек: ЖОҒАРЫ, ОРТАША, немесе ТӨМЕН"""

    try:
        headers = {
            "Authorization": f"Bearer {config.GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        body = {
            "model": config.GROQ_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "max_tokens": 200
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=body,
            timeout=30
        )

        if response.status_code != 200:
            print(f"Groq HTTP қатесі: {response.status_code}")
            return default_response()

        result = response.json()

        if 'choices' not in result or len(result['choices']) == 0:
            print(f"Groq жауап форматы қате: {result}")
            return default_response()

        text = result['choices'][0]['message']['content'].strip()
        print(f"AI жауабы: {text}")

        # JSON тазалау
        text = text.replace("```json", "").replace("```", "").strip()

        # JSON табу
        start = text.find('{')
        end = text.rfind('}') + 1
        if start >= 0 and end > start:
            text = text[start:end]

        decision = json.loads(text)

        # Міндетті өрістерді тексеру
        if 'decision' not in decision:
            decision['decision'] = 'WAIT'
        if 'confidence' not in decision:
            decision['confidence'] = 50
        if 'reason' not in decision:
            decision['reason'] = 'AI анализі'
        if 'risk' not in decision:
            decision['risk'] = 'ОРТАША'

        return decision

    except json.JSONDecodeError as e:
        print(f"JSON қатесі: {e}, мәтін: {text}")
        return default_response()
    except Exception as e:
        print(f"AI қатесі: {e}")
        return default_response()

def default_response():
    return {
        "decision": "WAIT",
        "confidence": 0,
        "reason": "AI жауап бермеді",
        "risk": "ЖОҒАРЫ"
    }
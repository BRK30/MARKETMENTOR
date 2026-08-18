# MarketMentor - Stock Price Prediction Model

## 1. Overview

The MarketMentor Price Prediction module is designed to predict future stock prices using historical stock market data and machine learning techniques.

The system provides:

- Tomorrow's predicted price
- Next week's predicted price
- Market trend
- Confidence score

The prediction module is integrated with the MarketMentor backend through a Flask REST API.

---

## 2. Technology Used

The module uses the following technologies:

- Python
- Flask
- Flask-CORS
- HTML
- CSS
- JavaScript
- Machine Learning
- LSTM/GRU (planned model)

---

## 3. Prediction Workflow

The prediction system follows these steps:

1. User selects a stock symbol.
2. The frontend sends a request to the backend.
3. Flask receives the stock symbol.
4. The prediction model processes the stock information.
5. The model generates price predictions.
6. The backend returns the prediction as JSON.
7. The frontend displays the result to the user.

---

## 4. Prediction Output

The API returns the following information:

| Field | Description |
|------|-------------|
| symbol | Stock symbol |
| current_price | Current stock price |
| tomorrow | Predicted price for tomorrow |
| week | Predicted price for next week |
| trend | Bullish or Bearish |
| confidence | Prediction confidence score |

Example response:

```json
{
    "symbol": "RELIANCE",
    "current_price": 2950,
    "tomorrow": 3009,
    "week": 3097.5,
    "trend": "Bullish",
    "confidence": 91
}
def predict_stock(symbol):
    """
    MarketMentor demonstration stock prediction model.

    Current implementation uses dummy prediction values
    for API/UI integration. This function can later be
    replaced with an LSTM/GRU trained model.
    """

    predictions = {
        "TCS": {
            "current_price": 3650,
            "tomorrow": 3725,
            "week": 3820,
            "trend": "Bullish",
            "confidence": 91
        },

        "RELIANCE": {
            "current_price": 2950,
            "tomorrow": 3015,
            "week": 3080,
            "trend": "Bullish",
            "confidence": 89
        },

        "INFY": {
            "current_price": 1500,
            "tomorrow": 1535,
            "week": 1575,
            "trend": "Bullish",
            "confidence": 87
        },

        "HDFCBANK": {
            "current_price": 1680,
            "tomorrow": 1715,
            "week": 1750,
            "trend": "Bullish",
            "confidence": 90
        }
    }

    symbol = symbol.upper()

    if symbol in predictions:
        return predictions[symbol]

    return {
        "current_price": 1000,
        "tomorrow": 1020,
        "week": 1050,
        "trend": "Bullish",
        "confidence": 75
    }
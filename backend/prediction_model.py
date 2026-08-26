import yfinance as yf
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


# =========================================================
# MARKETMENTOR AI STOCK PREDICTION MODEL
# =========================================================

def predict_stock(symbol):

    symbol = symbol.upper().strip()

    # -----------------------------------------------------
    # DOWNLOAD HISTORICAL DATA
    # -----------------------------------------------------

    ticker = yf.Ticker(symbol + ".NS")

    data = ticker.history(
        period="2y",
        interval="1d",
        auto_adjust=True
    )

    if data.empty:
        raise Exception(
            "Unable to download historical data for " + symbol
        )

    # -----------------------------------------------------
    # CLEAN DATA
    # -----------------------------------------------------

    data = data[["Close"]].dropna()

    close_prices = data["Close"].astype(float).values

    if len(close_prices) < 120:
        raise Exception(
            "Not enough historical data for " + symbol
        )

    # -----------------------------------------------------
    # FEATURE CREATION
    #
    # We use the previous 10 closing prices to predict
    # the next closing price.
    # -----------------------------------------------------

    window = 10

    X = []
    y = []

    for i in range(window, len(close_prices)):

        X.append(
            close_prices[i - window:i]
        )

        y.append(
            close_prices[i]
        )

    X = np.array(X)
    y = np.array(y)

    # -----------------------------------------------------
    # TIME-SERIES TRAIN / TEST SPLIT
    #
    # No random shuffle.
    # Older data -> training
    # Newer data -> testing
    # -----------------------------------------------------

    split = int(len(X) * 0.80)

    X_train = X[:split]
    X_test = X[split:]

    y_train = y[:split]
    y_test = y[split:]

    if len(X_test) == 0:
        raise Exception("Unable to create test dataset")

    # -----------------------------------------------------
    # RANDOM FOREST MODEL
    # -----------------------------------------------------

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=12,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )

    model.fit(
        X_train,
        y_train
    )

    # -----------------------------------------------------
    # MODEL EVALUATION
    # -----------------------------------------------------

    test_predictions = model.predict(
        X_test
    )

    # MAE
    mae = mean_absolute_error(
        y_test,
        test_predictions
    )

    # RMSE
    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            test_predictions
        )
    )

    # -----------------------------------------------------
    # DIRECTIONAL ACCURACY
    #
    # Checks whether the model correctly predicted
    # whether price would move UP or DOWN.
    # -----------------------------------------------------

    actual_previous = X_test[:, -1]

    actual_direction = (
        y_test > actual_previous
    )

    predicted_direction = (
        test_predictions > actual_previous
    )

    directional_accuracy = np.mean(
        actual_direction == predicted_direction
    ) * 100

    # -----------------------------------------------------
    # CURRENT PRICE
    # -----------------------------------------------------

    current_price = float(
        close_prices[-1]
    )

    # -----------------------------------------------------
    # TOMORROW PREDICTION
    # -----------------------------------------------------

    last_window = close_prices[-window:]

    tomorrow_prediction = float(
        model.predict(
            last_window.reshape(1, -1)
        )[0]
    )

    # -----------------------------------------------------
    # NEXT 7 DAYS PREDICTION
    #
    # Recursive forecasting.
    # -----------------------------------------------------

    future_window = list(
        last_window
    )

    future_predictions = []

    for _ in range(7):

        next_prediction = float(
            model.predict(
                np.array(
                    future_window[-window:]
                ).reshape(1, -1)
            )[0]
        )

        future_predictions.append(
            next_prediction
        )

        future_window.append(
            next_prediction
        )

    week_prediction = float(
        future_predictions[-1]
    )

    # -----------------------------------------------------
    # TREND
    # -----------------------------------------------------

    if week_prediction > current_price:
        trend = "Bullish"
    else:
        trend = "Bearish"

    # -----------------------------------------------------
    # PRICE ERROR %
    #
    # Lower error = better model performance.
    # -----------------------------------------------------

    error_percentage = (
        mae / current_price
    ) * 100

    # -----------------------------------------------------
    # CONFIDENCE SCORE
    #
    # Confidence combines:
    #
    # 1. Directional accuracy
    # 2. Historical price error
    #
    # This is an estimated model reliability score,
    # NOT a probability of guaranteed profit.
    # -----------------------------------------------------

    error_score = max(
        0,
        100 - (error_percentage * 10)
    )

    confidence = (
        directional_accuracy * 0.60
        +
        error_score * 0.40
    )

    confidence = max(
        50,
        min(
            95,
            confidence
        )
    )

    confidence = round(
        confidence
    )

    # -----------------------------------------------------
    # RETURN RESULT
    #
    # Existing frontend expects these fields.
    # Additional metrics can be used later.
    # -----------------------------------------------------

    return {

        "current_price": round(
            current_price,
            2
        ),

        "tomorrow": round(
            tomorrow_prediction,
            2
        ),

        "week": round(
            week_prediction,
            2
        ),

        "trend": trend,

        "confidence": confidence,

        # Model evaluation metrics
        "mae": round(
            float(mae),
            2
        ),

        "rmse": round(
            float(rmse),
            2
        ),

        "directional_accuracy": round(
            float(directional_accuracy),
            2
        )

    }
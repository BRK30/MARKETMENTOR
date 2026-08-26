from flask import Flask, jsonify, send_from_directory
import os
import yfinance as yf

from prediction_model import predict_stock


app = Flask(__name__)


# =========================================================
# FOLDER SETUP
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FRONTEND_FOLDER = os.path.abspath(
    os.path.join(BASE_DIR, "..", "frontend")
)


# =========================================================
# FRONTEND ROUTES
# =========================================================

# Dashboard
@app.route("/")
def home():
    return send_from_directory(
        FRONTEND_FOLDER,
        "index.html"
    )


# Dashboard - direct URL
@app.route("/index.html")
def dashboard():
    return send_from_directory(
        FRONTEND_FOLDER,
        "index.html"
    )


# Portfolio
@app.route("/portfolio.html")
def portfolio():
    return send_from_directory(
        FRONTEND_FOLDER,
        "portfolio.html"
    )


# Compare Stocks
@app.route("/compare.html")
def compare():
    return send_from_directory(
        FRONTEND_FOLDER,
        "compare.html"
    )


# AI Prediction
@app.route("/prediction.html")
def prediction_page():
    return send_from_directory(
        FRONTEND_FOLDER,
        "prediction.html"
    )


# CSS
@app.route("/style.css")
def style():
    return send_from_directory(
        FRONTEND_FOLDER,
        "style.css"
    )


# =========================================================
# STOCK API - LIVE DATA FROM YFINANCE
# =========================================================

@app.route("/api/stock/<symbol>")
def get_stock(symbol):

    try:

        symbol = symbol.upper().strip()

        ticker = yf.Ticker(
            symbol + ".NS"
        )

        # Get latest market data
        data = ticker.history(
            period="5d",
            interval="1d"
        )

        if data.empty:

            return jsonify({

                "success": False,

                "message":
                    "Stock data not found"

            }), 404

        latest = data.iloc[-1]

        # =================================================
        # COMPANY INFORMATION
        # =================================================

        try:

            info = ticker.info

        except Exception:

            info = {}

        # =================================================
        # PRICE DATA
        # =================================================

        price = float(
            latest["Close"]
        )

        open_price = float(
            latest["Open"]
        )

        high_price = float(
            latest["High"]
        )

        low_price = float(
            latest["Low"]
        )

        volume = int(
            latest["Volume"]
        )

        # =================================================
        # FUNDAMENTAL DATA
        # =================================================

        market_cap = info.get(
            "marketCap",
            0
        )

        pe = info.get(
            "trailingPE",
            None
        )

        dividend_yield = info.get(
            "dividendYield",
            None
        )

        fifty_two_high = info.get(
            "fiftyTwoWeekHigh",
            None
        )

        fifty_two_low = info.get(
            "fiftyTwoWeekLow",
            None
        )

        # =================================================
        # DIVIDEND YIELD
        # =================================================

        if dividend_yield is not None:

            dividend_yield = (
                float(dividend_yield) * 100
            )

        # =================================================
        # RESPONSE
        # =================================================

        return jsonify({

            "success": True,

            "symbol": symbol,

            "price": round(
                price,
                2
            ),

            "open": round(
                open_price,
                2
            ),

            "high": round(
                high_price,
                2
            ),

            "low": round(
                low_price,
                2
            ),

            "volume": volume,

            "market_cap": market_cap,

            "pe": (
                round(
                    float(pe),
                    2
                )
                if pe is not None
                else None
            ),

            "dividend_yield": (
                round(
                    float(dividend_yield),
                    2
                )
                if dividend_yield is not None
                else None
            ),

            "fifty_two_high": (
                round(
                    float(fifty_two_high),
                    2
                )
                if fifty_two_high is not None
                else None
            ),

            "fifty_two_low": (
                round(
                    float(fifty_two_low),
                    2
                )
                if fifty_two_low is not None
                else None
            )

        })

    except Exception as e:

        print(
            "Stock API Error:",
            e
        )

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500


# =========================================================
# PORTFOLIO HISTORY API
# =========================================================

@app.route("/api/portfolio-history/<symbol>")
def portfolio_history(symbol):

    try:

        symbol = symbol.upper().strip()

        ticker = yf.Ticker(
            symbol + ".NS"
        )

        # Get 6 months history
        data = ticker.history(
            period="6mo",
            interval="1d"
        )

        if data.empty:

            return jsonify({

                "success": False,

                "message":
                    "Historical data not found"

            }), 404

        history = []

        # =================================================
        # CONVERT TO JSON
        # =================================================

        for date, row in data.iterrows():

            close_price = row.get(
                "Close"
            )

            if close_price is None:
                continue

            history.append({

                "date":
                    date.strftime(
                        "%Y-%m-%d"
                    ),

                "price":
                    round(
                        float(close_price),
                        2
                    )

            })

        # =================================================
        # RESPONSE
        # =================================================

        return jsonify({

            "success": True,

            "symbol": symbol,

            "history": history

        })

    except Exception as e:

        print(
            "Portfolio History Error:",
            e
        )

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500


# =========================================================
# AI PREDICTION API
# =========================================================

@app.route("/api/prediction/<symbol>")
def get_prediction(symbol):

    try:

        symbol = symbol.upper().strip()

        # =================================================
        # GET PREDICTION FROM ML MODEL
        # =================================================

        prediction = predict_stock(
            symbol
        )

        # =================================================
        # RETURN RESPONSE
        # =================================================

        return jsonify({

            "success": True,

            "symbol": symbol,

            "current_price":
                prediction["current_price"],

            "tomorrow":
                prediction["tomorrow"],

            "week":
                prediction["week"],

            "trend":
                prediction["trend"],

            "confidence":
                prediction["confidence"],

            # ML evaluation metrics
            "mae":
                prediction.get(
                    "mae",
                    None
                ),

            "rmse":
                prediction.get(
                    "rmse",
                    None
                ),

            "directional_accuracy":
                prediction.get(
                    "directional_accuracy",
                    None
                )

        })

    except Exception as e:

        print(
            "Prediction API Error:",
            e
        )

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/api/health")
def health():

    return jsonify({

        "success": True,

        "message":
            "MarketMentor API is running",

        "data_source":
            "yfinance",

        "prediction":
            "MarketMentor Random Forest AI Model"

    })


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    print("")
    print("======================================")
    print("       MARKETMENTOR SERVER")
    print("======================================")
    print("")

    print("Frontend:")
    print(
        "http://127.0.0.1:5000/"
    )

    print("")

    print("Dashboard:")
    print(
        "http://127.0.0.1:5000/index.html"
    )

    print("")

    print("Portfolio:")
    print(
        "http://127.0.0.1:5000/portfolio.html"
    )

    print("")

    print("Compare:")
    print(
        "http://127.0.0.1:5000/compare.html"
    )

    print("")

    print("Prediction:")
    print(
        "http://127.0.0.1:5000/prediction.html"
    )

    print("")

    print("Health Check:")
    print(
        "http://127.0.0.1:5000/api/health"
    )

    print("")

    print("Stock API:")
    print(
        "http://127.0.0.1:5000/api/stock/TCS"
    )

    print("")

    print("History API:")
    print(
        "http://127.0.0.1:5000/api/portfolio-history/TCS"
    )

    print("")

    print("Prediction API:")
    print(
        "http://127.0.0.1:5000/api/prediction/TCS"
    )

    print("")
    print("======================================")
    print("")


    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
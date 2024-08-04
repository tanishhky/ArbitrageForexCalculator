import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
import lightgbm as lgb
import catboost as cb

# Load and preprocess your data
currencies = ['USD', 'EUR', 'JPY', 'GBP', 'CHF', 'CAD', 'AUD', 'NZD', 'CNY', 'INR']
data = {}

for base in currencies:
    for quote in currencies:
        if base != quote:
            pair = f"{base}{quote}=X"
            try:
                ticker_data = yf.Ticker(pair).history(period="5y")
                if not ticker_data.empty:
                    data[f"{base}/{quote}"] = ticker_data['Close']
            except Exception as e:
                print(f"Error fetching data for {pair}: {e}")

# Define the models
def create_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(units=50))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Train and evaluate models
results = {}

for pair, df in data.items():
    print(f"Processing {pair}...")
    df = df.dropna()
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df.values.reshape(-1, 1))

    look_back = 60
    X, y = [], []
    for i in range(look_back, len(scaled_data)):
        X.append(scaled_data[i-look_back:i, 0])
        y.append(scaled_data[i, 0])
    X, y = np.array(X), np.array(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    # LSTM
    lstm_model = create_lstm_model((X_train.shape[1], 1))
    lstm_model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)
    lstm_preds = lstm_model.predict(X_test)
    lstm_rmse = np.sqrt(mean_squared_error(y_test, lstm_preds))

    # ARIMA
    arima_model = ARIMA(df, order=(5, 1, 0))
    arima_model_fit = arima_model.fit()
    arima_preds = arima_model_fit.forecast(steps=len(X_test))
    arima_preds = scaler.transform(arima_preds.reshape(-1, 1))
    arima_rmse = np.sqrt(mean_squared_error(y_test, arima_preds))

    # Prophet
    prophet_df = df.reset_index().rename(columns={'Date': 'ds', 'Close': 'y'})
    prophet_model = Prophet()
    prophet_model.fit(prophet_df)
    future = prophet_model.make_future_dataframe(periods=len(X_test))
    prophet_preds = prophet_model.predict(future)['yhat'].tail(len(X_test)).values
    prophet_preds = scaler.transform(prophet_preds.reshape(-1, 1))
    prophet_rmse = np.sqrt(mean_squared_error(y_test, prophet_preds))

    # Random Forest
    rf_model = RandomForestRegressor()
    rf_model.fit(X_train.reshape(X_train.shape[0], -1), y_train)
    rf_preds = rf_model.predict(X_test.reshape(X_test.shape[0], -1))
    rf_rmse = np.sqrt(mean_squared_error(y_test, rf_preds))

    # XGBoost
    xgb_model = xgb.XGBRegressor()
    xgb_model.fit(X_train.reshape(X_train.shape[0], -1), y_train)
    xgb_preds = xgb_model.predict(X_test.reshape(X_test.shape[0], -1))
    xgb_rmse = np.sqrt(mean_squared_error(y_test, xgb_preds))

    # LightGBM
    lgb_model = lgb.LGBMRegressor()
    lgb_model.fit(X_train.reshape(X_train.shape[0], -1), y_train)
    lgb_preds = lgb_model.predict(X_test.reshape(X_test.shape[0], -1))
    lgb_rmse = np.sqrt(mean_squared_error(y_test, lgb_preds))

    # CatBoost
    cb_model = cb.CatBoostRegressor(silent=True)
    cb_model.fit(X_train.reshape(X_train.shape[0], -1), y_train)
    cb_preds = cb_model.predict(X_test.reshape(X_test.shape[0], -1))
    cb_rmse = np.sqrt(mean_squared_error(y_test, cb_preds))

    # Store results
    results[pair] = {
        'LSTM': lstm_rmse,
        'ARIMA': arima_rmse,
        'Prophet': prophet_rmse,
        'Random Forest': rf_rmse,
        'XGBoost': xgb_rmse,
        'LightGBM': lgb_rmse,
        'CatBoost': cb_rmse
    }

# Determine the best model for each currency pair
best_models = {}
for pair, metrics in results.items():
    best_model = min(metrics, key=metrics.get)
    best_models[pair] = best_model

# Print results
print("\nBest models for each currency pair:")
for pair, model in best_models.items():
    print(f"{pair}: {model}")

print("\nModel performance metrics:")
for pair, metrics in results.items():
    print(f"{pair}: {metrics}")
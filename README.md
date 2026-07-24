# Q Signals

Professional real-time trading signal backend built with **FastAPI**.

Streams live market data from **Binance** (crypto) and **Finnhub**
(forex & stocks), aggregates it into OHLC candles, computes a suite
of technical indicators, and generates weighted-vote trading signals
— all broadcast in real time over WebSockets.

## Features

- Live crypto ticks via the Binance WebSocket API
- Live forex/stock ticks via the Finnhub WebSocket API
- Real-time OHLC candle building & multi-timeframe aggregation
- Technical indicators: SMA, EMA, RSI, MACD, ADX, ATR, VWAP, Bollinger Bands
- Voting-engine based signal generation with confidence scoring
- REST API for markets, symbols, candles, indicators and signals
- WebSocket channel-based subscriptions for real-time updates
- Structured JSON logging, request IDs, rate limiting, global error handling

## Project Structure

```
app/
├── api/                 REST endpoints (crypto, forex, stocks, indicators, signals, markets, settings, health)
├── background/          Long-running workers (market stream, indicator/signal calc, broadcaster, scheduler)
├── core/                Settings, config, constants, exceptions, DI
├── indicators/           Technical indicator implementations
├── logging/              Structlog configuration
├── market_engine/        Tick processing, candle building, OHLC aggregation, symbol registry
├── middleware/            CORS, request ID, error handling, logging, rate limiting
├── providers/             Binance & Finnhub REST/WebSocket clients, parsers, models
├── services/              Cross-cutting business logic (market, ohlc, symbol, indicator, signal, cache, history, streaming)
├── signal_engine/          Voting engine, confidence calculator, signal models
├── utils/                   Shared helpers (time, json, retry, validators)
├── websocket/                Connection manager, broadcaster, channels, events, router
└── main.py                   FastAPI application entry point
```

## Getting Started

### 1. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

Add your Finnhub API key (free tier at https://finnhub.io) to enable
forex/stock data. Binance's public market data endpoints work without
an API key.

### 3. Run the server

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

- API docs: http://127.0.0.1:8000/docs
- WebSocket: `ws://127.0.0.1:8000/ws`

## WebSocket Protocol

Connect to `/ws` and send JSON control messages:

```json
{"action": "subscribe", "channel": "prices"}
{"action": "subscribe_symbol", "symbol": "BTCUSDT"}
{"action": "ping"}
```

Available channels: `all`, `prices`, `crypto`, `forex`, `stocks`,
`signals`, `chart`, `indicators`, `market`, `system`.

## REST API Overview

| Endpoint | Description |
|---|---|
| `GET /api/v1/health` | Health check |
| `GET /api/v1/markets` | Supported market types |
| `GET /api/v1/markets/symbols` | All supported symbols |
| `GET /api/v1/crypto/{symbol}/price` | Latest crypto price |
| `GET /api/v1/crypto/{symbol}/candles` | Crypto OHLC candles |
| `GET /api/v1/forex/{symbol}/quote` | Forex quote |
| `GET /api/v1/stocks/{symbol}/quote` | Stock quote |
| `GET /api/v1/indicators/{symbol}` | Latest technical indicators |
| `GET /api/v1/signals/{symbol}` | Generated trading signal |
| `GET /api/v1/settings` | Public application settings |

## License

Proprietary — internal project.

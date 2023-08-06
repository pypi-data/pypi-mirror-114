# ccz

Intuitive cryptocurrency trading.

Quote currency is fixed.

## Installation

```
pip install ccz
```

## Setup

Create a `config.json` with the exchange configuration:

```json
{
  "exchange": "binance",
  "quote": "cad",
  "auth": {
    "apiKey": "foo",
    "secret": "bar"
  }
}
```

- `exchange` is the [CCXT exchange ID](https://github.com/ccxt/ccxt/wiki/Exchange-Markets).
- See [CCXT docs](https://github.com/ccxt/ccxt/wiki/Manual#api-keys-setup) for the `auth` structure.

## Trading

### Show balance

```bash
ccz balance
```

```
ada     74.11
bch     0.00
btc     43.71
doge    94.06
dot     0.00
eos     0.00
eth     127.98
link    0.00
ltc     0.82
usdt    20.34
xlm     0.00
xrp     5.22
unused  154.27
total   520.51
```

### Buy currency

Buy in quote currency:

```
ccz buy btc 50
```

Buy with percentage of available quote currency:

```
ccz buy btc 50 -p
```

### Sell currency

Sell by equivalent in quote currency:

```
ccz sell btc 50
```

Sell by percentage of available base currency:

```
ccz sell btc 50 -p
```

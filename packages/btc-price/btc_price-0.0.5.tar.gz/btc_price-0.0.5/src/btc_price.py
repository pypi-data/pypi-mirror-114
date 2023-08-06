import json
import requests

# Get price of btc
def btcprice(currency):
    return str(requests.get("https://blockchain.info/ticker").json()[currency]["last"])

#Exchange a currency to the same value in btc
def currency_to_btc(courrencyvolume, currency):
    return str(courrencyvolume / requests.get("https://blockchain.info/ticker").json()[currency]["last"])

#Exchange btc to the same value in a currency
def btc_to_currency(btcvolume, currency):
    return str(requests.get("https://blockchain.info/ticker").json()[currency]["last"] * btcvolume)

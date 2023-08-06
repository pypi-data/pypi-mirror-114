import json
import logging

import httpx

from .connection import Connection
from .const import BALANCE_URL, HOST, TOKEN_URL, SIMPLE_PROTOCOL_URL, PROTOCOL_URL
from .wallet import Wallet

class Debank:

    """Initialize the Debank object"""
    def __init__(self, address, websession: httpx.AsyncClient):
        self._address = address
        self._connection = Connection(websession, HOST)
        self._wallet = None
        self._defiWalletContents = {}

        self._tokenResultsJson = None
        self._protocolResultsJson = None
        self._debank_defi_wallet_balance = 0.0
        return

    """Connect to the Debank and retrieve basic information, needed to"""
    """retrieve more detailed information"""
    async def connect(self):
        results = await self._connection.get(TOKEN_URL.format(self._address))
        if results.status_code == httpx.codes.OK:
            try:
                self._tokenResultsJson = results.json()
                logging.debug("Token List: %s", self._tokenResultsJson)
            except json.JSONDecodeError:
                raise

        elif results.status_code == 401:
            return False
        else:
            results.raise_for_status()

        results = await self._connection.get(SIMPLE_PROTOCOL_URL.format(self._address))
        if results.status_code == httpx.codes.OK:
            try:
                self._protocolResultsJson = results.json()
                logging.debug("Protocol List: %s", self._protocolResultsJson)
            except json.JSONDecodeError:
                raise

            return True
        elif results.status_code == 401:
            return False
        else:
            results.raise_for_status()

    def getDefiWalletBalance(self):
        return self._debank_defi_wallet_balance


    def getDefiWalletItems(self):
        return self._defiWalletContents
        
    async def update(self):
        await self._setDefiWalletList()
        return

    def _setDefiWalletBalance(self):
        self._debank_defi_wallet_balance = 0.0
        items = list(self._defiWalletContents.keys())
        for t in range(len(items)):
            if not items[t] == "Total":
                logging.debug("TB: %s - UP %s - T: %s", self._debank_defi_wallet_balance, self._defiWalletContents[items[t]]["balance"], items[t])
                self._debank_defi_wallet_balance += self._defiWalletContents[items[t]]["balance"]

        logging.debug("Total Balance: $ %s", self._debank_defi_wallet_balance)
        return

    async def _setDefiWalletList(self):
        for t in range(len(self._tokenResultsJson)):
            logging.debug("Name: %s - $: %s", self._tokenResultsJson[t]["name"], (self._tokenResultsJson[t]["price"] * self._tokenResultsJson[t]["amount"]))
            self._defiWalletContents.update({self._tokenResultsJson[t]["name"]: {"balance": (self._tokenResultsJson[t]["price"] * self._tokenResultsJson[t]["amount"])}})

        for p in range(len(self._protocolResultsJson)):
            results = await self._connection.get(PROTOCOL_URL.format(self._address, self._protocolResultsJson[p]["id"]))
            if results.status_code == httpx.codes.OK:
                try:
                    for pp in range(len(results.json()["portfolio_item_list"])):
                        if results.json()["portfolio_item_list"][pp]["name"] == "Farming":
                            logging.debug("Type:$ %s/%s - $ %s", results.json()["portfolio_item_list"][pp]["detail"]["supply_token_list"][0]["symbol"], results.json()["portfolio_item_list"][pp]["detail"]["supply_token_list"][1]["symbol"], results.json()["portfolio_item_list"][pp]["stats"]["asset_usd_value"])
                            self._defiWalletContents.update({(results.json()["portfolio_item_list"][pp]["detail"]["supply_token_list"][0]["symbol"] + "/" + results.json()["portfolio_item_list"][pp]["detail"]["supply_token_list"][1]["symbol"]): {"balance": results.json()["portfolio_item_list"][pp]["stats"]["asset_usd_value"]}})
                        if results.json()["portfolio_item_list"][pp]["name"] == "Staked":
                            logging.debug("Name: %s - $ %s", results.json()["portfolio_item_list"][pp]["detail"]["description"], (results.json()["portfolio_item_list"][pp]["detail"]["supply_token_list"][0]["price"] * results.json()["portfolio_item_list"][pp]["detail"]["supply_token_list"][0]["amount"]))
                            self._defiWalletContents.update({results.json()["portfolio_item_list"][pp]["detail"]["description"]: {"balance": (results.json()["portfolio_item_list"][pp]["detail"]["supply_token_list"][0]["price"] * results.json()["portfolio_item_list"][pp]["detail"]["supply_token_list"][0]["amount"])}})
                except json.JSONDecodeError:
                    raise

            elif results.status_code == 401:
                return False
            else:
                results.raise_for_status()

            self._setDefiWalletBalance()

            self._defiWalletContents.update({"Total": {"total balance": self.getDefiWalletBalance()}})
        logging.debug("%s", self._defiWalletContents)
        return
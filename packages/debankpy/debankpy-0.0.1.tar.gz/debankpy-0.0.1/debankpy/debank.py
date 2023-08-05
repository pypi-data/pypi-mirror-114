import json
import logging

import httpx

from .connection import Connection
from .const import BALANCE_URL, HOST, TOKEN_URL, SIMPLE_PROTOCOL_URL, PROTOCOL_URL
from .wallet import Wallet

class Debank:

    def __init__(self, address, websession: httpx.AsyncClient):
        self._address = address
        self._connection = Connection(websession, HOST)
        self._wallet = None
        self._walletContents = {}

        self._tokenResultsJson = None
        self._protocolResultsJson = None
        return

    async def connect(self):
        results = await self._connection.get(TOKEN_URL.format(self._address))
        if results.status_code == httpx.codes.OK:
            try:
                self._tokenResultsJson = results.json()
                logging.debug("Results: %s", self._tokenResultsJson)
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
                #logging.debug("Results: %s", self._protocolResultsJson)
            except json.JSONDecodeError:
                raise

            return True
        elif results.status_code == 401:
            return False
        else:
            results.raise_for_status()

    async def update(self):
        await self._createWallet()

    async def _createWallet(self):
        self._wallet = Wallet(self._address)
        self._wallet.setBalance(await self._getWalletBalance())
        #self._setWalletTokenList()
        self._wallet.updateBalance(await self._setWalletProtocolPrice())
        logging.info("Balance: $ %s", self._wallet.getBalance())
        return

    async def _getWalletBalance(self):
        balance_amount = 0.0
        prince = 0.0
        amount = 0.0
        results = await self._connection.get(TOKEN_URL.format(self._address))
        logging.debug("Tokens: %s", results.json())
        for t in range(len(results.json())):
            if results.json()[t]["price"] is None:
                price = 0.0
            else:
                price = results.json()[t]["price"]
            balance_amount += (price * results.json()[t]["amount"])
            logging.debug("Price: %s - Amount: %s", price, results.json()[t]["amount"])
        
        logging.debug("Balance: %s", balance_amount)
        return balance_amount

    def _setWalletTokenList(self):
        for t in range(len(self._tokenResultsJson)):
            logging.debug("Name: %s - ID: %s", self._tokenResultsJson[t]["name"], self._tokenResultsJson[t]["id"])
            self._walletContents.update({self._tokenResultsJson[t]["id"]: self._tokenResultsJson[t]["name"]})
        logging.debug("Wallet Contents: %s", self._walletContents)
        return

    async def _setWalletTokenPrice(self):
        return

    async def _setWalletProtocolList(self):
        return

    async def _setWalletProtocolPrice(self):
        total_protocol_price = 0.0

        logging.debug("Protocol: %s", self._protocolResultsJson)

        for p in range(len(self._protocolResultsJson)):
            logging.debug("Getting: %s", self._protocolResultsJson[p]["id"])
            results = await self._connection.get(PROTOCOL_URL.format(self._address, self._protocolResultsJson[p]["id"]))
            if results.status_code == httpx.codes.OK:
                try:
                    logging.debug("Results: %s", results.json())
                    for pp in range(len(results.json()["portfolio_item_list"])):
                        logging.debug("Results: %s", results.json()["portfolio_item_list"][pp]["stats"]["asset_usd_value"])
                        total_protocol_price = total_protocol_price + results.json()["portfolio_item_list"][pp]["stats"]["asset_usd_value"]
                except json.JSONDecodeError:
                    raise

            elif results.status_code == 401:
                return False
            else:
                results.raise_for_status()

        logging.debug("Total Protocol Price: $ %s", total_protocol_price)
        return total_protocol_price
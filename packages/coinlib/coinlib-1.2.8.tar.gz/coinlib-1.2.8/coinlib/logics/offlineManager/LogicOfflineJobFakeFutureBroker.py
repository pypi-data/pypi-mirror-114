import datetime
import random
import string
from enum import Enum
import pandas as pd
from typing import List

from coinlib.logics.offlineManager.LogicOfflineJobFakeBroker import LogicOfflineJobFakeBroker, FakeOrder, OrderSide, \
    OrderType


class FakeOpenPosition:
    entryPrice: float
    amount: float
    orderId: str
    order: FakeOrder
    symbol: string

class LogicOfflineJobFakeFutureBroker(LogicOfflineJobFakeBroker):

    _openPositions: List[FakeOpenPosition] = []

    def __init__(self, manager):
        super(LogicOfflineJobFakeFutureBroker, self).__init__(manager)
        self._openPositions = []
        pass

    def closePosition(self, clientOrderId, price: float = None, group=None):
        super().closePosition(clientOrderId, group)
        for pos in self._openPositions:
            if pos.orderId == clientOrderId:
                otherSide = OrderSide.BUY
                if pos.order.side == OrderSide.BUY:
                    otherSide = OrderSide.SELL
                else:
                    otherSide = OrderSide.BUY
                self.createOrder(otherSide, pos.order.symbol, pos.amount, reduceOnly=True, price=price, clientOrderId=pos.orderId)
        return False

    def closeAllPositions(self):
        super().closeAllPositions()
        for pos in self._openPositions:
            self.closePosition(pos.orderId)
        return False

    def positions(self):
        return self._openPositions


    def recalculateCurrentPortfolioByAssets(self):
        portfolio = super().recalculateCurrentPortfolioByAssets()

        for pos in self._openPositions:
            price = self.getPrice(symbol=pos.symbol)
            total = pos.amount * price
            portfolio.currentMoney.summary = portfolio.currentMoney.summary + total

        return portfolio

    def exchangePositionToPortfolio(self, position: FakeOpenPosition):
        portfolio = self.manager.getPortfolio()

        outprice = self.getPrice(symbol=position.symbol)
        portfolio.getQuoteAsset().free += position.amount * outprice
        portfolio.getQuoteAsset().total += position.amount * outprice

        return True

    def exchangeOrderToPosition(self, position: FakeOpenPosition):
        portfolio = self.manager.getPortfolio()

        portfolio.getQuoteAsset().free -= position.amount * position.entryPrice
        portfolio.getQuoteAsset().total -= position.amount * position.entryPrice

        self.manager.updatePortfolio(portfolio)

        return True

    def onHandleExecutedOrder(self, order: FakeOrder):
        print("We convert it to a Position at "+str(order.executed_price))

        if order.reduceOnly:
            print("This is a close")
            for pos in self._openPositions:
                if pos.orderId == order.orderId:
                    self._openPositions.remove(pos)
                    self.exchangePositionToPortfolio(pos)
        else:
            position = FakeOpenPosition()
            position.entryPrice = order.executed_price
            position.symbol = order.symbol
            position.amount = order.quantity
            position.order = order
            position.orderId = order.orderId
            self.exchangeOrderToPosition(position)
            self._openPositions.append(position)

    def imOut(self):
        return not self.imIn()

    def imIn(self):
        if len(self._openPositions) > 0 or len(self._openOrders) > 0:
            return True
        return False
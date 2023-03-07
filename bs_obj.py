import time
import math
import requests
from bs4 import BeautifulSoup
from common_service import *
class BSObj:
    def __init__(self, ticker):
        self.ticker = ticker
        self.dates = []
        self.totalAssets = []
        self.totalLiabilities = []
        self.totalEquity = []
        self.netTangibleAssets = []
        self.totalDebts = []
        self.totalCash = ''
        self.totalDebt = ''
        self.currentRatio = ''



    def getBSYahooFinancialDataUrl(self, ticker):
        return 'https://finance.yahoo.com/quote/' + ticker + '/balance-sheet?p=' + ticker

    def getStatisticsDataUrl(self, ticker):
        return 'https://finance.yahoo.com/quote/' + ticker + '/key-statistics?p=' + ticker


def printBSObj(bsObj):
    print('Dates')
    print(bsObj.dates)
    print('Total Assets')
    print(bsObj.totalAssets)
    print('Total Liabilities')
    print(bsObj.totalLiabilities)
    print('Total Equity')
    print(bsObj.totalEquity)
    print('Net Tangible Assets')
    print(bsObj.netTangibleAssets)
    print('Total Debts')
    print(bsObj.totalDebts)
    print('Total Cash')
    print(bsObj.totalCash)
    print('Total Debt')
    print(bsObj.totalDebt)
    print('Current Ratio')
    print(bsObj.currentRatio)

def cleanBSObj(bsObj):
    bsObj.totalAssets = cleanRowValues(bsObj.totalAssets)    
    bsObj.totalLiabilities = cleanRowValues(bsObj.totalLiabilities)
    bsObj.totalEquity = cleanRowValues(bsObj.totalEquity)
    bsObj.netTangibleAssets = cleanRowValues(bsObj.netTangibleAssets)
    bsObj.totalDebts = cleanRowValues(bsObj.totalDebts)



def readAnnualBSDataForTicker(ticker):
    bsObj = BSObj(ticker)
    
    response = requests.get(bsObj.getBSYahooFinancialDataUrl(ticker), headers=getHeader())
    print('Balance Sheet Response Code for ' + ticker + ' is ' + str(response.status_code))
    soup = BeautifulSoup(response.content, "html.parser")

    bsObj.dates = getRowValuesByText(soup, 'Breakdown', 'span')['Breakdown']
    bsObj.totalAssets = getRowValuesByText(soup, 'Total Assets', 'span')['Total Assets']
    bsObj.totalLiabilities = getRowValuesByText(soup, 'Total Liabilities Net Minority Interest', 'span')['Total Liabilities Net Minority Interest']
    bsObj.totalEquity = getRowValuesByText(soup, 'Total Equity Gross Minority Interest', 'span')['Total Equity Gross Minority Interest']
    bsObj.netTangibleAssets = getRowValuesByText(soup, 'Net Tangible Assets', 'span')['Net Tangible Assets']
    bsObj.totalDebts = getRowValuesByText(soup, 'Total Debt', 'span')['Total Debt']

    response = requests.get(bsObj.getStatisticsDataUrl(ticker), headers=getHeader())
    print('Balance Sheet Statistics Response Code for ' + ticker + ' is ' + str(response.status_code))
    soup = BeautifulSoup(response.content, "html.parser")

    bsObj.totalCash = getRowValueFromStatisticsRow(soup, 'Total Cash', 'span')['Total Cash']
    bsObj.totalDebt = getRowValueFromStatisticsRow(soup, 'Total Debt', 'span')['Total Debt']
    bsObj.currentRatio = getRowValueFromStatisticsRow(soup, 'Current Ratio', 'span')['Current Ratio']

    cleanBSObj(bsObj)

    printBSObj(bsObj)

    return bsObj

def readQuarterlyBSDataForTicker(ticker):
    bsObj = BSObj(ticker)

    soup = clickQuarterlyButton(bsObj.getBSYahooFinancialDataUrl(ticker))

    bsObj.dates = getRowValuesByText(soup, 'Breakdown', 'span')['Breakdown']
    bsObj.totalAssets = getRowValuesByText(soup, 'Total Assets', 'span')['Total Assets']
    bsObj.totalLiabilities = getRowValuesByText(soup, 'Total Liabilities Net Minority Interest', 'span')['Total Liabilities Net Minority Interest']
    bsObj.totalEquity = getRowValuesByText(soup, 'Total Equity Gross Minority Interest', 'span')['Total Equity Gross Minority Interest']
    bsObj.netTangibleAssets = getRowValuesByText(soup, 'Net Tangible Assets', 'span')['Net Tangible Assets']
    bsObj.totalDebts = getRowValuesByText(soup, 'Total Debt', 'span')['Total Debt']
    quitDriver()
    cleanBSObj(bsObj)
    printBSObj(bsObj)
    return bsObj




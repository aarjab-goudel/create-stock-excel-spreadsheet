import pandas as pd
import time
import math
from common_service import *
from bs4 import BeautifulSoup
import requests

class CFObj:
    def __init__(self, ticker):
        self.ticker = ticker
        self.dates = []
        self.freeCashFlow = []
        self.netCashByOperatingActivities = []
        self.netCashForInvestingActivities = []
        self.netCashForFinancingActivities = []
        self.capitalExpenditures = []
    
    def getCFYahooFinancialDataUrl(self, ticker):
        return 'https://finance.yahoo.com/quote/' + ticker + '/cash-flow?p=' + ticker

    def remove_ttm_from_cfObj(self):
        if self.dates:
            if self.dates[0].lower() == 'ttm':
                self.dates.pop(0)
                self.freeCashFlow.pop(0)
                self.netCashByOperatingActivities.pop(0)
                self.netCashForInvestingActivities.pop(0)
                self.netCashForFinancingActivities.pop(0)
                self.capitalExpenditures.pop(0)

def printCFObj(cfObj):
    print('Dates')
    print(cfObj.dates)
    print('Net Cash By Operating Activities')
    print(cfObj.netCashByOperatingActivities)
    print('Net Cash For Investing Activities')
    print(cfObj.netCashForInvestingActivities)
    print('Net Cash For Financing Activities')
    print(cfObj.netCashForFinancingActivities)
    print('Capital Expenditures')
    print(cfObj.capitalExpenditures)
    print('Free Cash Flow')
    print(cfObj.freeCashFlow)

def cleanCFObj(cfObj):
    cfObj.freeCashFlow = cleanRowValues(cfObj.freeCashFlow)    
    cfObj.netCashByOperatingActivities = cleanRowValues(cfObj.netCashByOperatingActivities)
    cfObj.netCashForInvestingActivities = cleanRowValues(cfObj.netCashForInvestingActivities)
    cfObj.netCashForFinancingActivities = cleanRowValues(cfObj.netCashForFinancingActivities)
    cfObj.capitalExpenditures = cleanRowValues(cfObj.capitalExpenditures) 


def readAnnualCFDataForTicker(ticker):
    cfObj = CFObj(ticker)
    
    response = requests.get(cfObj.getCFYahooFinancialDataUrl(ticker), headers=getHeader())
    print('Cash Flow Statement Response Code for ' + ticker + ' is ' + str(response.status_code))
    soup = BeautifulSoup(response.content, "html.parser")

    cfObj.dates = getRowValuesByText(soup, 'Breakdown', 'span')['Breakdown']
    cfObj.netCashByOperatingActivities = getRowValuesByText(soup, 'Operating Cash Flow', 'span')['Operating Cash Flow']
    cfObj.netCashForInvestingActivities = getRowValuesByText(soup, 'Investing Cash Flow', 'span')['Investing Cash Flow']
    cfObj.netCashForFinancingActivities = getRowValuesByText(soup, 'Financing Cash Flow', 'span')['Financing Cash Flow']
    cfObj.capitalExpenditures = getRowValuesByText(soup, 'Capital Expenditure', 'span')['Capital Expenditure']
    cfObj.freeCashFlow = getRowValuesByText(soup, 'Free Cash Flow', 'span')['Free Cash Flow']

    cfObj.remove_ttm_from_cfObj()
    cleanCFObj(cfObj)
    printCFObj(cfObj)
    return cfObj


def readQuarterlyCFDataForTicker(ticker):
    cfObj = CFObj(ticker)
    
    soup = clickQuarterlyButton(cfObj.getCFYahooFinancialDataUrl(ticker))

    cfObj.dates = getRowValuesByText(soup, 'Breakdown', 'span')['Breakdown']
    cfObj.netCashByOperatingActivities = getRowValuesByText(soup, 'Operating Cash Flow', 'span')['Operating Cash Flow']
    cfObj.netCashForInvestingActivities = getRowValuesByText(soup, 'Investing Cash Flow', 'span')['Investing Cash Flow']
    cfObj.netCashForFinancingActivities = getRowValuesByText(soup, 'Financing Cash Flow', 'span')['Financing Cash Flow']
    cfObj.capitalExpenditures = getRowValuesByText(soup, 'Capital Expenditure', 'span')['Capital Expenditure']
    cfObj.freeCashFlow = getRowValuesByText(soup, 'Free Cash Flow', 'span')['Free Cash Flow']

    cfObj.remove_ttm_from_cfObj()
    cleanCFObj(cfObj)
    printCFObj(cfObj)
    quitDriver()
    return cfObj
    



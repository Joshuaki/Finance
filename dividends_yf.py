import yfinance as yf
import pandas as pd

stock = 'IBM'

ticker = yf.Ticker(stock)

dividends = ticker.dividends

income_statement_qtr = ticker.quarterly_income_stmt
income_statement = ticker.income_stmt

cashflow_qtr = ticker.quarterly_cashflow
cashflows = ticker.cashflow

balance_sheet = ticker.quarterly_balance_sheet




def CFPerShare(income, cashflow):

    income = income.transpose()
    cashflow = cashflow.transpose()

    df_CFPershare = pd.DataFrame(index=cashflow.index, columns=["cashflowpershare"])
    df_CFPershare["cashflowpershare"] = cashflow["Free Cash Flow"] / income["Diluted Average Shares"]
    return df_CFPershare 

CF_share_qtr = CFPerShare(income_statement_qtr, cashflow_qtr)
CF_share = CFPerShare(income_statement, cashflows)

print(CF_share_qtr)
print(CF_share)


def main():
    pass

if __name__ == "__main__":
    main()
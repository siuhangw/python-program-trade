import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Data In
# full_path
# relative_path
df = pd.read_csv('0388.HK.csv')
df = df[['Date', 'Open', 'High', 'Low', 'Close']]

df['Range'] = df['High'] - df['Low']
df['Pct_Range'] = df['Range'] - df['Open']
df['Barsize'] = df['Close'] - df['Open']
df['Pct_Barsize'] = df['Barsize'] / df['Open']
df['Pct_Change'] = df['Close'].pct_change()
print(df.head(5))

# Initialization
pos_opened = False
open_price = 0
close_price = 0
pnl = 0
pnl_list = []

# Backtest
for i in range(len(df)):
    now_date = df.loc[(i, 'Date')]
    now_open = df.loc[(i, 'Open')]
    now_high = df.loc[(i, 'High')]
    now_low = df.loc[(i, 'Low')]
    now_close = df.loc[(i, 'Close')]
    now_barsize = df.loc[(i, 'Pct_Barsize')]
    now_pct_change = df.loc[(i, 'Pct_Change')]

    # Open Position
    # if (pos_opened == False) and ((now_close - now_open) < -0.03 * now_open):
    if (pos_opened == False) and (now_pct_change < -0.03):
        pos_opened = True
        open_price = now_close

    # Close Position (Profit Taking & Stop Loss)
    if (pos_opened == True) and ((now_close - open_price > 0.03 * open_price) or (now_close - open_price < -0.02 * open_price) or (i == len(df) - 1)):
        pos_opened = False
        close_price = now_close
        pnl = close_price - open_price
        pnl_list.append(pnl)


total_profit = sum(pnl_list)
num_of_trade = len(pnl_list)
avg_pnl = total_profit / num_of_trade

print(total_profit)
print(num_of_trade)
print(avg_pnl)

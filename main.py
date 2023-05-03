import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Data In
# full_path
# relative_path
df = pd.read_csv('0388.HK.csv')
df = df[['Date', 'Open', 'High', 'Low', 'Close']]

# Initiation
pos_opened = False
open_price = 0
close_price = 0

# Backtest
print(len(df))
for i in range(len(df)):
    now_date = df.loc[(i, 'Date')]
    now_open = df.loc[(i, 'Open')]
    now_high = df.loc[(i, 'High')]
    now_low = df.loc[(i, 'Low')]
    now_close = df.loc[(i, 'Close')]

    # Open Position
    if (pos_opened == False) and ((now_close - now_open) < -0.03 * now_open):
        pos_opened = True
        open_price = now_close
        print(open_price)

    # Close Position (Profit Taking)
    if (pos_opened == True) and ((now_close - open_price) > 0.03 * open_price):
        pos_opened = False
        close_price = now_close
        print(close_price)
        print('********Profit Taking*********')

    # Close Position (Stop Loss)
    if (pos_opened == True) and ((now_close - open_price) < -0.02 * open_price):
        pos_opened = False
        close_price = now_close
        print(close_price)
        print('*********Stop Loss********')

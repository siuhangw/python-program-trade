import datetime
import pandas as pd
import yfinance as yf

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

def backtest(df, candle_len, stop_win, stop_loss):

    ### Initialization
    pos_opened = False
    open_date = datetime.datetime.now().date()
    open_price = 0
    close_price = 0
    pnl = 0
    pnl_list = []

    ### Backtest
    for i, row in df.iterrows():
        now_date = i.date()
        now_open = row['Open']
        now_high = row['High']
        now_low = row['Low']
        now_close = row['Close']
        now_candle = round(now_close - now_open, 2)
        now_barsize = row['Pct_Barsize']
        now_pct_change = row['Pct_Change']

        # Trade Logic
        open_pos_cond = now_candle > candle_len
        close_pos_cond = (now_date - open_date).days >= 7
        stop_win_cond = now_close - open_price > stop_win
        stop_loss_cond = now_close - open_price < stop_loss
        last_index_cond = i == df.index[-1]

        # Open Position
        if (pos_opened == False) and open_pos_cond:
            pos_opened = True
            open_price = now_close
            open_date = now_date

        # Close Position
        elif (pos_opened == True) and (stop_win_cond or stop_loss_cond or last_index_cond or close_pos_cond):
            pos_opened = False
            close_price = now_close
            pnl = close_price - open_price
            pnl_list.append(pnl)

    ### Result
    total_profit = sum(pnl_list)
    num_of_trade = len(pnl_list)
    avg_pnl = total_profit / num_of_trade

    print('total_profit: ', total_profit)
    print('num_of_trade: ', num_of_trade)
    print('avg_pnl: ', avg_pnl)
    print('########################')


if __name__ == '__main__':

    ### Data In
    # full_path
    # relative_path
    ticker = yf.Ticker('0388.HK')
    df = ticker.history(start='2022-01-01', end='2022-12-31')

    ### Data Cleaning
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    df = df[df['Volume'] > 0]
    df['Range'] = df['High'] - df['Low']
    df['Pct_Range'] = df['Range'] - df['Open']
    df['Barsize'] = df['Close'] - df['Open']
    df['Pct_Barsize'] = df['Barsize'] / df['Open']
    df['Pct_Change'] = df['Close'].pct_change()

    ### Parameters Combination
    candle_len_list = [5, 10, 15]
    stop_win_list = [2, 3]
    stop_loss_list = [20, 30]

    ### Iteration
    for stop_loss in stop_loss_list:
        for stop_win in stop_win_list:
            for candle_len in candle_len_list:
                backtest(df, candle_len, stop_win, stop_loss)

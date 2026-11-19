
import numpy as np
import pandas as pd
import multiprocessing
from datetime import datetime
import pandas_ta as ta

current_process = multiprocessing.current_process()
process_name = current_process.name
event = multiprocessing.Event()

def EMA_CALCULATOR(df, period):
    return ta.ema(df['close'].astype(float), length=period)

def ATR_CALCULATOR(df,length):
    return ta.atr(df['high'].astype(float), df['low'].astype(float), df['close'].astype(float), length=length) 

def TRADE_EXIT_WORK(profit,profit_made,win_trd,top_trd,loss):
    if profit_made > 0:
        profit += profit_made
        win_trd += 1
        top_trd.append(round(profit_made,1))
    else:
        loss += abs(profit_made) 
    
    return profit, win_trd, top_trd, loss
    
    
def TRADING_BOT(start, end, df, net_profit, total_profit, total_loss, event, lonlen, sholen, longap, shogap, no_of_trades, no_of_lt, no_of_st, perc, bigema,top_profitable_trades,least_profitable_trades,win_percentage,ATRvalue):
    
    params = [(long_length, short_length, long_gap, short_gap, percentage, atr_value) 
                for long_length in np.arange(start, end, 10)
                for short_length in np.arange(260, 290, 10) #(60, 300, 10)
                for atr_value in np.arange(50, 70, 10)    #(50, 110, 10)
                for long_gap in np.linspace(0.50, 0.70, 3)  #(0.30, 0.90, 7)
                for short_gap in np.linspace(0.30, 0.50, 3) #(0.30, 0.90, 7)
                for percentage in np.linspace(0.3, 0.5, 3)]    #(0, 0.5, 6)
                #for trailing_stop_percentage in np.linspace(0.70, 0.90, 5)]    
    
    print('Total iterations to be run:', len(params) * 12)
    
    trade_log = []
    
    big_ema = 'ema_34' 
    
    #   2:39:16.699584  seconds for 2,79,936 columns
    #   1750 columns per minute
    
    #   starting from 9:35am on jan 18 to 4:05pm upon 5 & half day 1min candle data
    #   Backtesting completed in  6:31:50.075148  seconds for 2,79,936 columns
    
    #   starting from 1:10am on jan 22 to 7:57am upon 5 day 1min candle data
    #   Backtesting completed in a total time of  6:45:13.423561  seconds for 2,79,936 columns
    
    #   starting from 8:00pm on jan 23 to ---> 13 hours of running 
    #   Backtesting completed in a total time of  13:05:26.845183  seconds

    #   starting from 11:40am on jan 24 to --->
    
    
    z = 0
    for long_length, short_length, long_gap, short_gap, percentage, atr_value in params:
        position = None
        entry_price = None
        max_gap = None
        max_profit_price = 0
        trade_list = []
        profit = 0
        loss = 0
        win_trd = 0
        lt = 0
        st = 0
        trd_iter = 0
        atr_value_list = []
        
        for i in range(2, len(df)):  
            current_candle_close = df["close"].iloc[i]
            current_candle_open = df["open"].iloc[i]
            previous_candle_close = df["close"].iloc[i - 1]
            previous_candle_open = df["open"].iloc[i - 1]
            second_previous_candle_close = df["close"].iloc[i - 2]
            second_previous_candle_open = df["open"].iloc[i - 2]
            last_atr_value = float(df['atr'].iloc[i])

            
            if current_candle_close > current_candle_open:
                current_diff = ((current_candle_close - current_candle_open) * percentage) + current_candle_open
                previous_diff = ((previous_candle_close - previous_candle_open) * percentage) + previous_candle_open
            else:
                current_diff = ((current_candle_open - current_candle_close) * percentage) - current_candle_open
                previous_diff = ((previous_candle_open - previous_candle_close) * percentage) - previous_candle_open

            l1 = (current_candle_close - second_previous_candle_open) > long_length
            l2 = current_candle_close > df['ema_5'].iloc[i] and current_candle_open > df['ema_5'].iloc[i]
            l3 = current_diff > previous_candle_close
            l4 = previous_diff > second_previous_candle_close
            l5 = df['ema_5'].iloc[i] > df[big_ema].iloc[i]
            
            s1 = (second_previous_candle_open - current_candle_close) > short_length
            s2 = current_candle_close < df['ema_5'].iloc[i] and current_candle_open < df['ema_5'].iloc[i]
            s3 = current_diff < previous_candle_close
            s4 = previous_diff < second_previous_candle_close
            s5 = df['ema_5'].iloc[i] < df[big_ema].iloc[i]

            
            
            if trd_iter < 9:
                Atr_rule = last_atr_value > atr_value
                trd_iter+=1
                atr_value_list.append(last_atr_value)
            else:
                atr_diff = atr_value_list[0] - last_atr_value if atr_value_list[0] > last_atr_value else last_atr_value - atr_value_list[0]
                Atr_rule = atr_diff > atr_value
                atr_value_list.append(last_atr_value)
                atr_value_list.pop(0)
            
            #Atr_rule = last_atr_value > atr_value
            
            long_condition = l1 and l2 and l3 and l4 and l5 and Atr_rule
            short_condition = s1 and s2 and s3 and s4 and s5 and Atr_rule


            if position is None:
                if long_condition: 
                    position = "Long"
                    lt += 1         #   ADDING A LONG TRADE
                    entry_price = current_candle_close
                    max_gap = df['ema_5'].iloc[i] - df[big_ema].iloc[i]
                elif short_condition: 
                    position = "Short"
                    st += 1         #   ADDING A SHORT TRADE
                    entry_price = current_candle_close
                    max_gap = df[big_ema].iloc[i] - df['ema_5'].iloc[i]

            if position == "Long":
                current_gap = df['ema_5'].iloc[i] - df[big_ema].iloc[i]
                max_gap = max(max_gap, current_gap) 
                if current_gap < max_gap * long_gap: 
                    position = None
                    profit_made = current_candle_close - entry_price
                    trade_log.append(round(profit_made,1)) if profit_made > 0 else None
                    profit,win_trd,trade_list,loss = TRADE_EXIT_WORK(profit,profit_made,win_trd,trade_list,loss)
                '''
                # Trailing stop loss
                max_profit_price = max(max_profit_price, current_candle_close)
                max_profit_made = round(max_profit_price - entry_price,1)                                            
                TSL = round(max_profit_made * trailing_stop_percentage,1) 
                current_profit_made = round(current_candle_close - entry_price,1)     
                #print('current_profit_made = ',current_profit_made)  
                
                if current_profit_made < TSL and current_profit_made > 15:  
                    profit,win_trd,trade_list,loss = TRADE_EXIT_WORK(profit,profit_made,win_trd,trade_list,loss)
                '''

            if position == "Short":
                current_gap = df[big_ema].iloc[i] - df['ema_5'].iloc[i]
                max_gap = max(max_gap, current_gap)
                if current_gap < max_gap * short_gap:
                    position = None
                    profit_made = entry_price - current_candle_close
                    trade_log.append(round(profit_made,0)) if profit_made > 0 else None
                    profit,win_trd,trade_list,loss = TRADE_EXIT_WORK(profit,profit_made,win_trd,trade_list,loss)
                '''
                # Trailing stop loss
                max_profit_price = min(max_profit_price, current_candle_close)
                max_profit_made = round(entry_price - max_profit_price,1)                                            
                TSL = round(max_profit_made * trailing_stop_percentage,1) 
                current_profit_made = round(current_candle_close - entry_price,1)     
                #print('current_profit_made = ',current_profit_made)  
                
                if current_profit_made < TSL and current_profit_made > 15:  
                    profit,win_trd,trade_list,loss = TRADE_EXIT_WORK(profit,profit_made,win_trd,trade_list,loss)
                '''

        tot_trd = lt + st
        if tot_trd > 0:
            win_perc = (win_trd / tot_trd) * 100
        else:
            win_perc = 0
        top_trd = sorted(trade_list, reverse=True)[:5]
        top_los = sorted(trade_list, reverse=False)[:5]
        net_p = round(profit, 0) - round(loss, 0)
        event.set()
        
        net_profit.append(net_p)
        total_profit.append(round(profit, 0))
        total_loss.append(round(loss, 0))
        lonlen.append(long_length)
        sholen.append(short_length)
        longap.append(long_gap)
        shogap.append(short_gap)
        no_of_trades.append(tot_trd)      
        no_of_lt.append(lt)                       
        no_of_st.append(st)                        
        perc.append(percentage)
        bigema.append(big_ema)
        win_percentage.append(round(win_perc,2))
        top_profitable_trades.append(str(top_trd))
        least_profitable_trades.append(str(top_los))
        ATRvalue.append(atr_value)

        z += 1
        print(f"{process_name} : Completed iteration {z} / {len(params)}")
        event.wait()


if __name__ == "__main__":
    
    multiprocessing.freeze_support()
    manager = multiprocessing.Manager()
    
    bigema = manager.list()
    win_percentage = manager.list()
    top_profitable_trades = manager.list()
    least_profitable_trades = manager.list()
    ATRvalue = manager.list()
    perc = manager.list()
    lonlen = manager.list()
    sholen = manager.list()
    longap = manager.list()
    shogap = manager.list()
    no_of_trades = manager.list()
    no_of_lt = manager.list()
    no_of_st = manager.list()
    net_profit = manager.list()
    total_profit = manager.list()
    total_loss = manager.list()
    test_report_dict = manager.dict()
    
    processes = []
    start_time = datetime.now()
    
    len_start = 150 #60
    len_end = 190 #300
    
    num_cores = multiprocessing.cpu_count()
    total_tasks = len_end - len_start
    chunk_size = total_tasks // num_cores
    print ('\n chunk_size =',chunk_size)
    remaining_tasks = total_tasks % num_cores
    
    csv_filename = "D:\data_ohlc_jan29.csv"
    loaded_df = pd.read_csv(csv_filename)
    df = loaded_df.set_index('datetime')

    
    df['ema_5'] = EMA_CALCULATOR(df, 5)
    df['ema_34'] = EMA_CALCULATOR(df, 34)
    df['atr'] = ATR_CALCULATOR(df, 13)
    print("Data loaded from CSV:")
    print(df)
    
    for i in range(num_cores):
        start = len_start + (i * chunk_size) + min(i, remaining_tasks)
        end = start + chunk_size + (1 if i < remaining_tasks else 0)
        print ('\nstart = ',start)
        print ('end = ',end)
        process = multiprocessing.Process(target=TRADING_BOT, args=(start, end, df, net_profit, total_profit, total_loss,event,lonlen,sholen,longap,shogap,no_of_trades,no_of_lt,no_of_st,perc,bigema,top_profitable_trades,least_profitable_trades,win_percentage,ATRvalue)) 
        processes.append(process)
        process.start()
    
    for process in processes:
        process.join()
    
    
    test_report_dict.update({'No of trades': list(no_of_trades)})
    test_report_dict.update({'No of Long trades': list(no_of_lt)})
    test_report_dict.update({'No of Short trades': list(no_of_st)})
    
    test_report_dict.update({'Top profitable trades': list(top_profitable_trades)})
    test_report_dict.update({'Win percent': list(win_percentage)})
    test_report_dict.update({'Least profitable trades': list(least_profitable_trades)})
    
    test_report_dict.update({'Net Profit': list(net_profit)}) 
    test_report_dict.update({'Total Profit': list(total_profit)})
    test_report_dict.update({'Total Loss': list(total_loss)})
    test_report_dict.update({'Long length': list(lonlen)})
    test_report_dict.update({'Short length': list(sholen)})
    test_report_dict.update({'Long Gap': list(longap)})
    test_report_dict.update({'Short Gap': list(shogap)})
    test_report_dict.update({'percentage': list(perc)})
    test_report_dict.update({'ATR value': list(ATRvalue)})
    
    

    test_report_df = pd.DataFrame(dict(test_report_dict))
    test_report_df = test_report_df.sort_values(by='Net Profit', ascending=False)

    end_time = datetime.now()
    print("\n\n\nBacktesting completed in a total time of ",end_time - start_time," seconds")
    print('df =\n',test_report_df)
    
    file_path = r'D:\dummy report 2 atr diff.xlsx' 
    test_report_df.to_excel(file_path, index=False)
    
    
    print('\nExcel sheet report generated at = ',end_time)
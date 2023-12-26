import pandas as pd
import lxml as lxml
import numpy as np
import html5lib as ht
import yfinance as yf
import plotly as chart
import plotly.graph_objects as go
import plotly.express as px 
from pandas.io.html import read_html
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt

def process_statements(base_url, num_statements):
    #get urls of all the pages
    url = []
    url.append(base_url)
    for i in range(2, num_statements + 1):
        temp_url = f'{base_url.replace("#", f"{i}#")}'
        url.append(temp_url)
    
    #get tables
    del_count = 0
    p_statements = []
    for i in range(0, len(url)):
        #print(url[i])
        try:
            df = read_html(url[i], attrs={"class": "mctable1"}, index_col=0, header=0)[0]
            del_count+=1
        except ValueError as e:
            break
        p_statements.append(df)

    #get the index
    index = p_statements[0].index.name

    # Merging data frames for p
    p = p_statements[0]
    for i in range(1, len(p_statements)):
        p = p.merge(p_statements[i], on=index, suffixes=(f'_p_statements[{i - 1}]', f'_p_statements[{i}]'))


    p = p.drop([p_statements[0].index[0]])
    p = p.sort_index(axis=1 ,ascending=True)
    for i in range(del_count):
        p = p.drop(p.columns[-1], axis=1)
    p = p.infer_objects()
    p = p.replace(np.nan, "")
    p.replace("--", 0, inplace = True)

    return p


pl_url = 'https://www.moneycontrol.com/financials/lemontreehotels/profit-lossVI/LTH/#LTH'
bs_url = pl_url.replace('profit-lossVI', 'balance-sheetVI')
cf_url = pl_url.replace('profit-lossVI', 'cash-flowVI')
qbs_url = pl_url.replace('profit-lossVI', 'quarterly-results')
num_statements = 5

pl_df = process_statements(pl_url, num_statements)
pl_df.to_csv('LTH_P&L.csv')

bs_df = process_statements(bs_url, num_statements)
bs_df.to_csv('LTH_BS.csv')

cf_df = process_statements(cf_url, num_statements)
cf_df.to_csv('LTH_CF.csv')

qbs_df = process_statements(qbs_url, 4*num_statements)
qbs_df.to_csv('LTH_QBS.csv')

data = yf.download("LEMONTREE.NS")
data = data.reset_index()
fig1 = chart.graph_objects.Figure(data=[chart.graph_objects.Candlestick(x=data['Date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'])])
data = yf.download("^BSESN")
data = data.reset_index()
fig2 = chart.graph_objects.Figure(data=[chart.graph_objects.Candlestick(x=data['Date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'])])

fig1.show()
fig2.show()


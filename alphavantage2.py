from alpha_vantage.timeseries import TimeSeries
ts = TimeSeries(key='3TSPYZB33UAHO33D',output_format='pandas')
symbol = ['DEO', 'BP']
for i in symbol:
    data, meta_data = ts.get_intraday(symbol=i,interval='30min',outputsize='compact')
    tail = data.tail(1)
    closing_value = (tail[tail.columns[3]].tolist())[0]
    print(i, round(closing_value,2))

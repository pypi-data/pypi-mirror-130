from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

class finviz:
  
  def __init__(self, ticker):
    self.ticker = ticker

  def url_response(self):

    ticker = self.ticker
    finviz_url = 'https://finviz.com/quote.ashx?t='
    url = finviz_url + ticker
    req = Request(url=url, headers={'user-agent': 'my-app'})
    response = urlopen(req)
    html = BeautifulSoup(response, 'html.parser')

    return html

  def series(self):

    html = self.url_response()

    perf_table = html.find("table", {"class": "snapshot-table2"})
    #perf_tables[ticker] = perf_table

    table_rows = perf_table.findAll('tr')
    prop_ls = []
    value_ls = []

    for index, row in enumerate(table_rows):
      table_columns = row.findAll('td')
      for index, column in enumerate(table_columns):
        if index%2 == 0:
          prop_ls.append(column.text)
        else:
          value_ls.append(column.text)

    a_series = pd.Series(value_ls, index = prop_ls)
    return a_series

  def news(self):

    parsed_data = []
    
    html = self.url_response()
    news_table = html.find(id='news-table')
    table_rows = news_table.findAll('tr')
    for index, row in enumerate(table_rows):
      title = row.a.text
      date_data = row.td.text.split(' ')

      if len(date_data)==1:
        time = date_data[0]
      else:
        date = date_data[0]
        time = date_data[1]
      
      parsed_data.append([self.ticker, date, time, title])
    
   
    df = pd.DataFrame(parsed_data, columns = ['symbol', 'date', 'time', 'title'])
    df['date'] = pd.to_datetime(df.date).dt.date
    
    return df
  
  def sentimentAnalyzer(self):
    df = self.news()
    vader = SentimentIntensityAnalyzer()
    f = lambda title: vader.polarity_scores(title)['compound']
    df['compound'] = df['title'].apply(f)
    return df
  
  def sentimentAnalyzerView(self):
    
    df = self.sentimentAnalyzer()
    mean_df = df.groupby(['symbol', 'date']).mean()
    mean_df = mean_df.unstack()
    mean_df = mean_df.xs('compound', axis="columns").transpose()
    mean_df.plot(kind='bar')
    plt.show()

class finviz_scanner:
    
  def url_response(self):
    
    url = 'https://finviz.com/screener.ashx?v=111&f=sh_curvol_o200,ta_change_u,ta_perf_1wup,ta_perf2_4wup&ft=4&o=-change'

    req = Request(url=url, headers={'user-agent': 'my-app'})
    response = urlopen(req)
    html = BeautifulSoup(response, 'html.parser')

    return html
  
  def url_screener_pages(self):

    url_root = 'https://finviz.com/'

    html_ls = []
    html = self.url_response()
    html_ls.append(html)
    
    td = html.find('td', {"class":"body-table screener_pagination"})
    a = td.findAll('a', {'class': {"tab-link"}})
    n = a[1].b.text
    href = a[1]['href']
    final_url = url_root+href

    while n =='next':

      req = Request(url=final_url, headers={'user-agent': 'my-app'})
      response = urlopen(req)
      html_new = BeautifulSoup(response, 'html.parser')

      td = html_new.find('td', {"class":"body-table screener_pagination"})
      a = td.findAll('a', {'class': {"tab-link"}})
      for x in a:
        n = x.b.text
        if n == 'next':
          href = x['href']

      final_url = url_root+href
      
      html_ls.append(html_new)
    
    return html_ls
  
  def get_tables(self):
    
    frames = []
    html_ls = self.url_screener_pages()
    for html in html_ls:
      parsed_results = []
      table = html.find('table', {'width':'100%', 'cellpadding': '3', 'cellspacing': "1",  'bgcolor': "#d3d3d3"})
      table_rows = table.findAll('tr')
      for row in table_rows[1:]:
        pre_parsed_results = []
        a = row.findAll('a')
        for x in a[1:]:
            pre_parsed_results.append(x.text)
        parsed_results.append(pre_parsed_results)
    
      ls = ['symbol', 'company', 'sector', 'industry', 'country', 'market_cap', 'P/E', 'price', 'change%', 'volume']
      df = pd.DataFrame(parsed_results, columns=ls)
      df['change%'] = df['change%'].apply(lambda x : float(x.strip('%')))
      df['price'] = df['price'].apply(lambda x : float(x))
      df['volume'] = df['volume'].apply(lambda x: int(x.replace(',', '')))
      frames.append(df) 

    df = pd.concat(frames)
    df = df[['symbol', 'price', 'change%', 'volume']]
    df = df.sort_values(by='change%', ascending=False, ignore_index=True)

    return df
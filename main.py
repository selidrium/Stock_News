from traceback import print_tb
from unittest.util import three_way_cmp
import requests
from newsapi import NewsApiClient
from twilio.rest import Client


STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# Stock Api
apikey = ''#instert stock api key

NEWS_API = '' #insert news api key


api = NewsApiClient(api_key=NEWS_API)
api.get_everything(q=STOCK_NAME)



# News API to get articles related to the COMPANY_NAME.
def send_notif(stock, body):
    SMS_NUMBER = "" #insert given #
    account_sid = "" #insert account sid
    auth_token = "" #insert auth token
    client = Client(account_sid, auth_token)
    message = client.messages \
                    .create(
                        body=f"{stock}\n{body}",
                        from_=SMS_NUMBER,
                        to='+' #insert #
                    )
# Parameters for Stock API
parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": apikey
}

response = requests.get(url=STOCK_ENDPOINT, params=parameters)
data = response.json()["Time Series (Daily)"]


# Get yesterday's closing stock price
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_close = float(yesterday_data["4. close"])
# Get the day before yesterday's closing stock price
day_before_yesterday_data = (data_list[1])
day_before_close = float(day_before_yesterday_data["4. close"])

# Find the absolute value of the change
difference = float(abs(yesterday_close - day_before_close))

# Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percent_change = ((difference / yesterday_close)* 100)
format_change = float("{:.2f}".format(percent_change))

message_stock = ""
if yesterday_close > day_before_close:
    message_stock = f"{STOCK_NAME}:🔺{format_change}%"
else:
    message_stock = f"{STOCK_NAME}:🔻{format_change}%"

# If price change > 5% will notify user
if format_change > 5:
    news_parameters = {
        "apiKey": NEWS_API,
        "q": COMPANY_NAME,
        "apikey": apikey
    }

    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    articles = news_response.json()['articles']
    three_articles = articles[:3]
    article_list = [f"Headline: {article['title']}. \nBrief: {article['description']}\n" for article in three_articles]

# Create a new list of the first 3 article's headline and description using list comprehension.
    for article in article_list:
        send_notif(message_stock, article)
else:
    print("No News")


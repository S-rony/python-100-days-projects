import requests
from datetime import datetime, timedelta
from twilio.rest import Client



STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = "YLAIMBK1ZGH0O51G"
NEWS_API_KEY = "f634d81248dd4f5bbc734957d1ac53eb"
TWILIO_SID = "ACf7bc3bab7a448622a43454fae58289f2"
TWILIO_AUTH_TOKEN = "1d438b2650a8ed1d3ac0d658fe61a877"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

today = datetime.today().date()
yesterday = today - timedelta(days=1)
day_after_yesterday = today - timedelta(days=2)


# print(stock_data)
# yesterday_stock_price = (stock_data["Time Series (Daily)"][str(yesterday)]["4. close"])
# day_after_yesterday_stock_price = (stock_data["Time Series (Daily)"][str(day_after_yesterday)]["4. close"])
#
# yesterday_stock_price = float(yesterday_stock_price)
# print(f"{yesterday_stock_price:.2f}")
#
# day_after_yesterday_stock_price = float(day_after_yesterday_stock_price)
# print(f"{day_after_yesterday_stock_price:.2f}")
#

## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday
# and the day before yesterday then print("Get News").

#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list
# comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]


stock_params = {
    "function" : "Time_SERIES_DAILY",
    "symbol" : STOCK_NAME,
    "apikey" : STOCK_API_KEY,
}
response = requests.get(STOCK_ENDPOINT,params=stock_params)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for (key,value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

#TODO 2. - Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)


#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20,
# but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp

difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔼"
else:
    up_down = "🔽"

#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent = round((difference / float(yesterday_closing_price)) * 100)
print(diff_percent)



#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.

if abs(diff_percent) > 1:
    new_params = {
        "apiKey" : NEWS_API_KEY,
        "q" : COMPANY_NAME,
    }

    new_response = requests.get(NEWS_ENDPOINT, params=new_params)
    new_response.raise_for_status()
    article =  new_response.json()["articles"]
    print(article)
    # Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    three_articles = article[:3]
    print(three_articles)
    formatted_articles = [f"{STOCK_NAME}: {up_down} {diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)


    for article in formatted_articles:
        message = client.messages.create(
            body = article,
            from_= "+14472243450",
            to = "+917004972945",
        )

    ## STEP 2: https://newsapi.org/
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 




    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

    #TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.


    #TODO 9. - Send each article as a separate message via Twilio.



#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""


import requests
import jsonpath
import json

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def get():
    return 'Hello world!'


@app.route("/mypostendpoint", methods=["POST"])
def mainPage():
    if request.method == 'POST':
        coin = request.json

        base_url = "https://min-api.cryptocompare.com/data/v2/news/?categories="

        current_crypto_full = coin['name'].upper()

        current_crypto = ""
        if current_crypto_full == "BITCOIN":
            current_crypto = "BTC"
        elif current_crypto_full == "ETHEREUM":
            current_crypto = "ETH"
        elif current_crypto_full == "RIPPLE":
            current_crypto = "XRP"

        excluded_crypto = "BTC,ETH,XRP,Sponsored".replace(current_crypto + ",", "")

        final_url = base_url + current_crypto + "&excludeCategories=" + excluded_crypto

        # print(final_url)

        response = requests.get(final_url)
        sentiments = response.json()  # grab json from the API's response

        body_list = jsonpath.jsonpath(sentiments, "$.Data.*.body")
        # print(sentiments)

        total_article = len(body_list)
        # print(total_article)

        # for x in body_list:
        # print(x)

        data = {'documents': []}
        itemdata = []

        for i, value in enumerate(body_list, 1):
            item = {'id': '1', 'language': 'en', 'text': 'Alpacas are my fav <3 <3'}
            item['id'] = str(i)
            item['language'] = 'en'
            item['text'] = value
            itemdata.append(item)

        data['documents'] = itemdata

        jsonData = json.dumps(data)

        # print(jsonData)

        subscription_key = "fe21b6735b534912934e15b70e83a4ee"
        text_analytics_base_url = "https://westcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/"
        sentiment_api_url = text_analytics_base_url + "sentiment"
        keyPhrases_api_url = text_analytics_base_url + "keyPhrases"
        # print(sentiment_api_url)

        # documents = {'documents' : [
        #   {'id': '1', 'language': 'en', 'text': 'I HATE you!!! Everyone should leave this subreddit immediately and go to the llamas subreddit.'},
        #   {'id': '2', 'language': 'en', 'text': 'Alpacas are my fav <3 <3'},
        #   {'id': '3', 'language': 'en', 'text': 'This is just really boring. Im not sure why I bothered writing this comment.'}]}
        #
        # print(documents)

        # creating the POST call to the REST API
        headers = {"Ocp-Apim-Subscription-Key": subscription_key}  # our subscription key
        # print(subscription_key)
        # response  = requests.post(keyPhrases_api_url, headers=headers, json=data)  # post the object
        # sentiments = response.json()                                                   # grab json from the API's response
        # print(sentiments)
        response = requests.post(sentiment_api_url, headers=headers, json=data)  # post the object
        sentiments = response.json()  # grab json from the API's response

        # print(json.dumps(sentiments))

        sentiment_list = jsonpath.jsonpath(sentiments, "$.documents.*.score")

        neutral_articles = 0
        positive_articles = 0
        negative_articles = 0

        # print(sentiment_list)
        sum = 0
        for item in sentiment_list:
            sum += item

        avg = sum / len(sentiment_list)

        for sentiment_val in sentiment_list:
            if sentiment_val == 0.5:
                neutral_articles += 1
            elif sentiment_val < 0.5:
                negative_articles += 1
            elif sentiment_val > 0.5:
                positive_articles += 1

        overall_sentiment = "Negative"
        if avg > 0.5:
            overall_sentiment = "Positive"

        OutputString = "I analyzed " + str(total_article) + " articles." + " I found " + str(
            neutral_articles) + " neutral articles, " + str(positive_articles) + " positive articles, and " + str(
            negative_articles) + " negative articles. The overall sentiment is looking " + overall_sentiment + "."

        print(OutputString)

        return jsonify({
            "textToSpeech": "For" + coin['name'] + OutputString
        })


if __name__ == '__main__':
    app.run()






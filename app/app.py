from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)


@app.route("/")
def hello():
    return "hello"


@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    if request.method == "POST":
        body = request.json
        if body["object"] == "page":
            for entry in body["entry"]:
                webhook_event = entry["messaging"][0]
                print(webhook_event)
            return "something", 200

        else:
            return "actually a bad request", 404

    else:
        f = open('app/Token.txt','r')
        verify_token = f.readline()
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == verify_token:
            print("WEBHOOK VERIFIED")
            return challenge, 200
        else:
            return "nope", 403


if __name__ == "__main__":
    app.run()
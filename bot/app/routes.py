from flask import request

from app import app, db

from user import User
from app.sender import handle_message, callSendAPI, handle_postback


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
                sender_psid = webhook_event['sender']['id']
                if User.query.filter_by(_id=int(sender_psid)).first() == None:
                    user = User(_id=int(sender_psid), _prev_action="welcome",_context="")
                    db.session.add(user)
                    db.session.commit()
                if 'message' in webhook_event:
                    print(sender_psid)
                    handle_message(sender_psid,webhook_event['message'])
                elif 'postback' in webhook_event:
                    handle_postback(sender_psid,webhook_event['postback'])
            return "something", 200

        else:
            return "actually a bad request", 404

    else:
        f = open('Token.txt','r')
        verify_token = f.readline()
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == verify_token:
            print("WEBHOOK VERIFIED")
            return challenge, 200
        else:
            return "nope", 403

@app.route('/webhook_df', methods=['POST'])
def webhook_df():
    return {}


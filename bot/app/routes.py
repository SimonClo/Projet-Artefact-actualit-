from flask import request
import requests

from app import app, db

from app.user import User
from app.action import ActionManager, Action


act_man = ActionManager()

PAGE_ACCESS_TOKEN = open('Token_fb.txt','r').readline()
FB_API_URL = "https://graph.facebook.com/v2.6/me/messages"

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


def handle_message(sender_psid, received_message):
    resp = {}
    user = User.query.filter_by(_id=int(sender_psid)).first()
    print(user.prev_action)

    if 'text' in received_message:
        intent = act_man.get_intent(received_message['text'])
        action = act_man.next_action(user, intent)
        user.prev_action = action
        db.session.commit()

        resp = Action.get_response(user)

    callSendAPI(sender_psid, resp)

def handle_postback(sender_psid, received_postback):
    payload = received_postback['payload']
    resp = {}
    if payload == 'yes':
        resp['text'] = 'Merci'
    elif payload == 'no':
        resp['text'] = 'Renvoyez une photo svp'

    callSendAPI(sender_psid, resp)

def callSendAPI(sender_psid, response):
    request_body = {
        "recipient": {"id": sender_psid},
        "message": response
    }
    auth= {"access_token": PAGE_ACCESS_TOKEN}
    req = requests.post(FB_API_URL, params=auth, json=request_body)

    return req.json()
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import request
import requests
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from user import User

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
                if User.query.filter_by(id=sender_psid) == []:
                    print('ok')
                    user = User(id=sender_psid, action="welcome",context="")
                    db.session.add(user)
                    db.session.commit()
                print('ok')
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
    user = User.query.filter_by(id=sender_psid).first()
    action_tmp = user.action

    if 'text' in received_message:
        if user.action == 'welcome':
            resp['text'] = 'Bonjour! Je suis le bot archiviste, voulez-vous un 1er article ?'
            resp['quick_replies'] = [{
                "content_type": "text",
                "title": "Oui",
                "payload": "yes",
                "image_url": "https://image.flaticon.com/icons/svg/1074/1074055.svg"
            }, {"content_type": "text",
                "title": "Non",
                "payload": "no",
                "image_url": "http://example.com/img/red.png"}]
            action_tmp = 'article'

        elif user.action == 'article':
            if received_message['text'] == 'Oui':
                resp['text'] = 'Voici un article: https://www.lexpress.fr/actualite/politique/bras-de-fer-entre-marcheurs-et-republicains-autour-de-la-liste-bechu_2109129.html'
                action_tmp = 'welcome'
            elif received_message['text'] == 'Non':
                resp['text'] = 'Ok! Bonne journée!'
                action_tmp = 'welcome'
            else:
                resp['text'] = 'Je n\'ai pas compris. Utilisez les quick replies ci-dessous pour me répondre'
                resp['quick_replies'] = [{
                    "content_type": "text",
                    "title": "Oui",
                    "payload": "yes"
                }, {"content_type": "text",
                    "title": "Non",
                    "payload": "no"}]

    elif 'attachments' in received_message:
        attachment_url = received_message['attachments'][0]['payload']['url']
        resp["attachment"] = {"type": "template",
                                   "payload": {"template_type": "generic",
                                               "elements": [{ "title": "Est ce la bonne photo ?",
                                                              "subtitle": "Appuyer sur un bouton pour répondre",
                                                              "image_url": attachment_url,
                                                              "buttons": [{"type": "postback",
                                                                           "title": "Oui!",
                                                                           "payload": "yes",},
                                                                          {"type": "postback",
                                                                           "title": "Non!",
                                                                           "payload": "no",}],}]}}

    user.action = action_tmp
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


if __name__ == "__main__":
    app.run()
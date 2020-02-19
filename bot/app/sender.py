import requests
from user import User

from app import db
from app.action import Action, ActionManager

PAGE_ACCESS_TOKEN = open('Token_fb.txt','r').readline()
FB_API_URL = "https://graph.facebook.com/v2.6/me/messages"

act_man = ActionManager()

def handle_message(sender_psid, received_message):
    resp = {}
    user = User.query.filter_by(_id=int(sender_psid)).first()
    print(user.prev_action)

    if 'text' in received_message:
        intent = act_man.get_intent(received_message['text'])
        print(intent)
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
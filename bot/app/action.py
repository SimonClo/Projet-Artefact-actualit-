import json
import dialogflow
import os
import random as rd
from app.db_access import get_latest_article, get_matching_archive
import config
from app import db

import app.sender

PROJECT_ID = os.getenv('DIALOGFLOW_PROJECT_ID')

class ActionManager:
    with open('./app/next_action.json') as json_data:
        next_json = json.load(json_data)

    def __init__(self):
        pass

    def get_intent(self, message):
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(PROJECT_ID, "unique")

        text_input = dialogflow.types.TextInput(
            text=message, language_code='fr')
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        return response.query_result.fulfillment_text

    def next_action(self, user, intent):
        if user.prev_action in ActionManager.next_json:
            if intent in ActionManager.next_json[user.prev_action]:
                return ActionManager.next_json[user.prev_action][intent]
            else:
                return 'welcome'
                #raise ValueError('Intent unknown')


class Action:
    with open('app/action_context_basic.json') as json_data:
        ac_json = json.load(json_data)

    def get_response(user):
        if user.prev_action == 'article':
            resp = Article.get_response(user)
        elif user.prev_action == 'archive':
            resp = Archive.get_response(user)
        else:
            resp = Action.form_resp(user, Action.ac_json)
        return resp

    def form_resp(user, action_json):
        resp = {'text': 'error','quick_replies':[]}
        for line in action_json:
            if line['Action'] == user.prev_action and line['Context'] == user.context:
                messages = line['Message']
                resp['text'] = messages[rd.randint(0,len(messages)-1)]
                for qr in line['Quick Replies']:
                    resp['quick_replies'].append({
                        "content_type": "text",
                        "title": qr,
                        "payload": qr
                    })

        return resp


class Article(Action):
    with open('app/action_context_article.json') as json_data:
        art_json = json.load(json_data)

    def get_response(user):
        print('ok')
        article = Article.get_article(user)
        app.sender.callSendAPI(user.id, article)
        resp = Action.form_resp(user,Article.art_json)
        return resp

    def get_article(user):
        if not user.last_article_index or user.last_article_index == config.NUM_ARTICLES:
            user.last_article_index = 0
        article_id, title, url = get_latest_article(user.last_article_index)
        user.last_article_index += 1
        user.last_article_id = article_id
        db.session.commit()
        return {"text":f"{title} :\n {url}"}

class Archive(Action):
    with open('app/action_context_archive.json') as json_data:
        arc_json = json.load(json_data)

    def get_response(user):
        article = Archive.get_archive(user)
        print(user.id)
        app.sender.callSendAPI(user.id, article)
        resp = Action.form_resp(user,Archive.arc_json)
        return resp

    def get_archive(user):
        if not user.rank_last_archive or user.rank_last_archive == config.NUM_ARCHIVES:
            user.rank_last_archive = 0
        title, url, year = get_matching_archive(user.last_article_id, user.rank_last_archive)
        user.rank_last_archive += 1
        db.session.commit()
        return {"text":f"de l'année {year} :\n{title} :\n {url}"}
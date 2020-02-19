import json
import dialogflow
import os

class ActionManager:
    with open('app/next_action.json') as json_data:
        next_json = json.load(json_data)

    def __init__(self):
        pass

    def get_intent(self, message):
        # à modifier en intégrant à Dialogflow
        project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(project_id, "unique")

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
            #elif intent == 'unknown':
            #    return 'welcome'
            else:
                return 'welcome'
                #raise ValueError('Intent unknown')


class Action:
    with open('app/action_context_list.json') as json_data:
        ac_json = json.load(json_data)

    def get_response(user):
        resp = {'text': 'Pas compris','quick_replies':[]}
        for line in Action.ac_json:
            if line['Action'] == user.prev_action and line['Context'] == user.context:
                resp['text'] = line['Message'][0]
                for qr in line['Quick Replies']:
                    resp['quick_replies'].append({
                "content_type": "text",
                "title": qr,
                "payload": qr
            })

        return resp


class Article(Action):
    def get_article(sender_psid):
        return 'Voici un article'

class Archive(Action):
    def get_archive(sender_psid):
        return 'Voici une archive'
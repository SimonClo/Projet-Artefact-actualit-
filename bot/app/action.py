import json

class ActionManager:

    def __init__(self):
        pass

    def get_intent(self, message):
        # à modifier en intégrant à Dialogflow
        return message.lower()

    def next_action(self, user, intent):
        if user.prev_action == 'welcome':
            if intent == 'oui':
                return 'article'
            elif intent == 'non':
                return 'explanation'
            else:
                return 'welcome'
        elif user.prev_action == 'article':
            if intent == 'article':
                return 'article'
            elif intent == 'archive':
                return 'archive'
            elif intent == 'non':
                return 'explanation'
            else:
                return 'welcome'
        elif user.prev_action == 'archive':
            if intent == 'archive':
                return 'archive'
            elif intent == 'article':
                return 'article'
            elif intent == 'explanation':
                return 'explanation'
            else:
                return 'welcome'
        elif user.prev_action == 'explanation':
            if intent == 'oui':
                return 'explanation_yes'
            elif intent =='non':
                return 'welcome'
            else:
                return 'welcome'
        elif user.prev_action == 'explanation_yes':
            return 'welcome'


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
from typing import Any, Text, Dict, List

# from euroleague_api.team_stats import TeamStats
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


# class ActionHelloWorld(Action):
#
#     # https://learning.rasa.com/conversational-ai-with-rasa/custom-actions/
#     # https://www.youtube.com/watch?v=rvHg7N8ux2I
#
#     def name(self) -> Text:
#         return "action_show_time"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         # dispatcher.utter_message(text=f"{dt.datetime.now()}")
#
#         team_stats = TeamStats()
#         df = team_stats.get_team_stats(
#             endpoint='traditional'
#         )
#         short_df = df.head(2)[['teamRanking', 'team.name', 'pointsScored', 'twoPointersMade']]
#
#         #    teamRanking            team.name  pointsScored  twoPointersMade
#         # 0            1  Skyliners Frankfurt          71.8             19.7
#         # 1            2          Arka Gdynia          70.3             18.5
#
#         return []


class ActionReceiveName(Action):

    def name(self) -> Text:
        return "action_receive_name"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        text = tracker.latest_message['text']  # get entire text from the previous message
        dispatcher.utter_message(text=f"I'll remember your name {text}!")
        return [SlotSet("name", text)]


class ActionSayName(Action):

    def name(self) -> Text:
        return "action_say_name"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        name = tracker.get_slot('name')  # Si no tiene valor devuelve None
        if not name:
            dispatcher.utter_message(text="I don't know your name.")
        else:
            dispatcher.utter_message(text=f"Your name is {name}!")

        return []

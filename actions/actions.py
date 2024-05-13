from typing import Any, Text, Dict, List

from euroleague_api.team_stats import TeamStats
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


class ActionReturnEuroleagueApiValues(Action):

    def name(self) -> Text:
        return "action_return_euroleague_api_values"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        team_stats = TeamStats(competition='E')
        df = team_stats.get_team_stats(
            endpoint='traditional'
        )

        team_name = "Baskonia Vitoria-Gasteiz"
        desired_row = df[df['team.name'] == team_name]
        games_played = desired_row['gamesPlayed'].iloc[0]  # 624
        # dispatcher.utter_message(text=f"Games played by {team_name}: {games_played}")

        return [SlotSet("team", team_name), SlotSet("amount", games_played)]


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

from typing import Any, Text, Dict, List

from euroleague_api.game_stats import GameStats
from euroleague_api.team_stats import TeamStats
from euroleague_api.standings import Standings
from euroleague_api.player_stats import PlayerStats
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher



class ActionReturnRequestedStandings(Action):
    
        def name(self) -> Text:
            return "action_return_requested_standings"
    
        def run(
                self,
                dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]
        ) -> List[Dict[Text, Any]]:
    
            # Obtain competition from slots
            competition = tracker.get_slot(key="competition")
            if competition == 'Euroleague':
                competition = 'E'
            else:
                competition = 'U'
            season = tracker.get_slot(key="season")
            round = tracker.get_slot(key="round")
    
            # Obtain standings
            standings = Standings(competition=competition)
            df = standings.get_standings(season=season, round_number=round)
    
            # DEBUG PRINTS (se pueden quitar --> salen en la consola que ejecutas 'rasa run actions')
            print(df)
    
            df2 = df[['position', 'gamesWon', 'gamesLost', 'club.name']].copy()

            dispatcher.utter_message(
            text=f"Standings for round {round} of the {season} season of the {competition}: \n {df2}"
            )
    
            return [SlotSet("competition", None), SlotSet("season", None), SlotSet("round", None)]


class ActionReturnRequestedGameMetadata(Action):

    def name(self) -> Text:
        return "action_return_requested_game_metadata"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        # Obtain home and away team names from slots
        home_team_name = tracker.get_slot(key="home_team")
        away_team_name = tracker.get_slot(key="away_team")

        # Extract some metadata stats
        game_stats = GameStats(competition='E')
        metadata_df = game_stats.get_game_metadata_season(season=2023)
        columns_to_extract = ['hometeam', 'awayteam', 'homescore', 'awayscore']
        metadata_df_subset = metadata_df[columns_to_extract]

        # Filter by team names and extract first match
        home_team_condition = metadata_df_subset['hometeam'] == home_team_name
        away_team_condition = metadata_df_subset['awayteam'] == away_team_name
        metadata_df_subset = metadata_df_subset[home_team_condition & away_team_condition]
        first_occurrence = metadata_df_subset.head(1)

        # DEBUG PRINTS (se pueden quitar --> salen en la consola que ejecutas 'rasa run actions')
        print(f'Home team: {home_team_name}')
        print(f'Away team: {away_team_name}')
        print(metadata_df_subset)

        # Obtain match result
        home_team_score = first_occurrence.iloc[0]['homescore']
        away_team_score = first_occurrence.iloc[0]['awayscore']

        dispatcher.utter_message(
            text=f"Game result: \n {home_team_name}: {home_team_score} \n {away_team_name}: {away_team_score}"
        )

        return [SlotSet("home_team", None), SlotSet("away_team", None)]


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

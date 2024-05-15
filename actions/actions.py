from typing import Any, Text, Dict, List

from euroleague_api.standings import Standings
from euroleague_api.team_stats import TeamStats
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, AllSlotsReset
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
        competition_full = tracker.get_slot(key="competition")
        if competition_full == 'Euroleague':
            competition = 'E'
        else:
            competition = 'U'
        season = tracker.get_slot(key="season")
        round_number = tracker.get_slot(key="round")

        # Obtain standings
        standings = Standings(competition=competition)
        df = standings.get_standings(season=season, round_number=round_number)

        # DEBUG PRINTS
        print(df)

        df2 = df[['position', 'gamesWon', 'gamesLost', 'club.name']].copy()

        dispatcher.utter_message(
            text=f"Standings for round {round_number} of the {season} season of the {competition_full}: \n {df2}"
        )

        # return [
        #     SlotSet("competition", None),
        #     SlotSet("season", None),
        #     SlotSet("round", None)
        # ]
        return [AllSlotsReset()]


class ActionReturnTeamsAvailable(Action):

    def name(self) -> Text:
        return "action_return_teams_available"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        competition = tracker.get_slot(key="competition")
        if competition == 'Euroleague':
            competition = 'E'
        else:
            competition = 'U'

        team_stats = TeamStats(competition=competition)
        df = team_stats.get_team_stats(endpoint='traditional')

        teams = df['team.name'].tolist()
        teams_str = ', '.join(teams)
        dispatcher.utter_message(text=f"Teams available: {teams_str}")

        return []


class ActionReturnRequestedTeamStatsAll(Action):

    def name(self) -> Text:
        return "action_return_requested_team_stats_all"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        team_name = tracker.get_slot(key="team")
        competition = tracker.get_slot(key="competition")
        if competition == 'Euroleague':
            competition = 'E'
        else:
            competition = 'U'

        team_stats = TeamStats(competition=competition)
        df = team_stats.get_team_stats(endpoint='traditional')

        # Poner más stats? Pedir cuales quiere el usuario?
        desired_row = df[df['team.name'] == team_name]
        games_played = desired_row['gamesPlayed'].iloc[0]
        points = desired_row['pointsScored'].iloc[0]
        assists = desired_row['assists'].iloc[0]
        rebounds = desired_row['totalRebounds'].iloc[0]
        steals = desired_row['steals'].iloc[0]
        blocks = desired_row['blocks'].iloc[0]
        turnovers = desired_row['turnovers'].iloc[0]
        pir = desired_row['pir'].iloc[0]

        dispatcher.utter_message(
            text=f"Team stats for {team_name}: \n Games played: {games_played} \n Points: {points} \n "
                 f"Assists: {assists} \n Rebounds: {rebounds} \n Steals: {steals} \n Blocks: {blocks} \n "
                 f"Turnovers: {turnovers} \n Pir: {pir}"
        )

        # return [SlotSet("team", None)]
        return [AllSlotsReset()]

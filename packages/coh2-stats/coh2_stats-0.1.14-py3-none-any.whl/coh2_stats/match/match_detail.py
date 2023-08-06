from coh2_stats.match.match_player_stats import MatchPlayerStats
from coh2_stats.match.match_side import MatchSide
from coh2_stats.player.playercard_collection import PlayerCardCollection

class MatchDetail:
    def __init__(self, player_match_data) -> None:
        self.player_count = len(player_match_data)

        self.player_match_stats_list = [MatchPlayerStats(datum, self.player_count) for datum in player_match_data]

        self.winner = "NA"
        if len(self.player_match_stats_list) > 0:
            self.winner = self.player_match_stats_list[0].winner_side()

    def split_into_sides(self, player_match_stats_list: list):
        allies = []
        axis =[]
        for player in player_match_stats_list:
            if player.is_allies:
                allies.append(player)

            else:
                axis.append(player)
        return allies, axis
    
    def set_all_players_playercard(self, playercard_collection)-> bool:
        """return true if all players are in current playercard_collection"""
        all_players_in_observed_group = True
        for player in self.player_match_stats_list:
            if playercard_collection[player.profile_id] is None:
                all_players_in_observed_group = False
                break
            else:
                player.set_playercard(playercard_collection[player.profile_id])

        if not all_players_in_observed_group:
            return False
        return True

    def is_qualified(self, playercard_collection: PlayerCardCollection):

        if self.player_count != 8:
            return False

        if self.winner == None:
            return False

        if not self.set_all_players_playercard(playercard_collection):
            return False

        self.allies, self.axis = self.split_into_sides(self.player_match_stats_list)

        self.matchside_allies = MatchSide(False, self.allies, playercard_collection)
        self.matchside_axis = MatchSide(True, self.axis, playercard_collection)

        analyze_successfully = self.matchside_allies.analyze_successfully() and self.matchside_axis.analyze_successfully()

        if not analyze_successfully:
            return False

        #if not matchside_allies.contains_team and matchside_allies.contains_team:
            #return False

        return True
    
    def validate_team_vs_team(self):
        return self.matchside_allies.validate_team_match() and self.matchside_axis.validate_team_match()

    def __repr__(self) -> str:
        lst = [f"{self.winner}"]
        allies_lst = [str(p) for p in self.allies]
        axis_lst = [str(p) for p in self.axis]
        lst.extend(allies_lst)
        lst.extend(axis_lst)
        return ','.join(lst)
from coh2_stats.performance.performance import Performance
from coh2_stats.leaderboard.leaderboard_constants import LeaderboardConstants

class MatchPlayerStats:
    def __init__(self, data, match_player_count) -> None:
        self.data = data
        self.match_player_count = match_player_count

        race_id_to_str = {
            0 : "OST",
            1 : "SOV",
            2 : "OKW",
            3 : "USF",
            4 : "UKF"
        }

        self.faction_id = data['race_id']
        #self.faction_str = race_id_to_str[self.faction_id]
        self.faction_str = f"{race_id_to_str[self.faction_id]}{str(int(self.match_player_count / 2))}"
        self.is_axis = self.faction_id in [0, 2]
        self.is_allies = not self.is_axis 

        self.win = data['resulttype'] == 1
        self.lost = not self.win

        self.profile_id = data['profile_id']

        #self.set_info("unknown", -1)
        #self.set_performance()

    def winner_side(self):
        return ["axis", "allies"][self.is_allies_winner()]

    def is_allies_winner(self):
        return (self.is_allies and self.win) or (self.is_axis and self.lost)
    
    def is_axis_winner(self):
        return not self.is_allies_winner()

    def set_solo_info(self):
        participation_method = 1
        rank = 1
        self.set_info(participation_method, rank)

    def set_info(self, participation_method, rank):
        self.participation_method = participation_method
        self.rank = rank

    def set_performance(self, performance: Performance):
        self.performance = performance
    
    def set_solo_performance(self):
        self.ladder_id = LeaderboardConstants.ladder_name_to_id[self.faction_str]
        performance = self.playercard.get_solo_performance(self.ladder_id)
        if performance is None:
            return False
        
        self.performance = performance
        return True

    def set_playercard(self, playercard):
        self.playercard = playercard

    def __repr__(self) -> str:
        return f"{self.playercard.player_info.alias}({self.performance.ladder_name})({self.performance.rank})"

from coh2_stats.player.player_performance import PlayerPerformance
from coh2_stats.player.player_info import PlayerInfo
from coh2_stats.performance.performance import Performance

class PlayerCard:
    def __init__(self, player_info: PlayerInfo) -> None:
        self.player_info = player_info
        self.player_performance = PlayerPerformance()
        pass

    def update(self, performance: Performance):
        self.player_performance.update(performance)

    def get_team_statgroup_list(self, ladder_id):
        return self.player_performance.get_team_statgroup_list(ladder_id)

    def get_solo_performance(self, ladder_id):
        return self.player_performance[ladder_id]

    def __repr__(self) -> str:
        info = f"{self.player_info}:\n{self.player_performance}"
        return info

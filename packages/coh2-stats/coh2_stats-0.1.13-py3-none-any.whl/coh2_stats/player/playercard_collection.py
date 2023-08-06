from coh2_stats.performance.performance import Performance
#from coh2_stats.performance.performance_page import PerformancePage
from coh2_stats.page.statgroup import Member
from coh2_stats.player.player_card import PlayerCard, PlayerInfo

class PlayerCardCollection:
    def __init__(self) -> None:
        self.database = dict()
        self.statgroup_id_to_team_performance = dict()

    def load_from_pages(self, performance_pages):
        for performance_page in performance_pages:
            for performance in performance_page.performances:
                self.update(performance, performance_page)

    def update(self, performance: Performance, performance_page)-> None:
        if performance.is_4s_solo:
            member = performance_page.get_statgroup_member_from_personal_id(\
                performance.statgroup_id,\
                performance_page.team_statgroups)

            playercard = self.get_or_create_playercard(member)
            playercard.update(performance)
        else:
            self.add_team_performance_to_players(performance, performance_page)
            if performance.statgroup_id not in self.statgroup_id_to_team_performance:
                self.statgroup_id_to_team_performance[performance.statgroup_id] = performance

    def add_team_performance_to_players(self, performance: Performance, performance_page):
        members = performance_page.get_members_from_id(performance.statgroup_id, performance_page.team_statgroups)
        for member in members:
            playercard = self.get_or_create_playercard(member)
            playercard.update(performance)

    def get_or_create_playercard(self, member: Member)-> PlayerCard:
        playercard = self[member.profile_id]
        if playercard is None:
            playercard = PlayerCard(PlayerInfo.create_from_member(member))
            self[member.profile_id] = playercard
        return playercard


    def get_team_performance(self, statgroup_id):
        if statgroup_id not in self.statgroup_id_to_team_performance:
            return None
        else:
            return self.statgroup_id_to_team_performance[statgroup_id]

    def __getitem__(self, value):
        if value in self.database:
            return self.database[value]
        return None

    def __setitem__(self, key, value):
        self.database[key] = value

    def __repr__(self) -> str:
        info = ""
        for player_id, playercard in self.database.items():
            info += f"{playercard}\n"

        info += f"totally {len(self.database)} players in record"

        return info
        index = 0
        for statgroup_id, performance in self.statgroup_id_to_team_performance.items():
            info += f"{performance}\n"
            index += 1
        info += f"totally {index}"
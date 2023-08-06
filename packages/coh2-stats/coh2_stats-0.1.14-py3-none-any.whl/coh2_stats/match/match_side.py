from coh2_stats.performance.performance import Performance
from itertools import combinations
from coh2_stats.player.playercard_collection import PlayerCardCollection
from coh2_stats.match.match_player_stats import MatchPlayerStats

class MatchSide:
    def __init__(self, is_axis, player_match_stats_list, playercard_collection: PlayerCardCollection):
        self.is_axis = is_axis
        self.player_match_stats_list = player_match_stats_list
        self.playercard_collection = playercard_collection
        self.teams = []

    def validate_team_match(self):
        for team in self.teams:
            if team.count == 2 and team.rank <= 50:
                return True
            if team.count == 3 and team.rank <= 20:
                return True
            if team.count == 4 and team.rank <= 20:
                return True
        return False

    def analyze_successfully(self):
        undecided = self.player_match_stats_list[:]
        all = self.player_match_stats_list
        for count in [4, 3, 2]:
            undecided = self.test_and_set_team(undecided, count)

        if len(undecided) == 2:
            undecided = self.test_and_set_team(undecided, 2)

        for player in undecided:
            if not player.set_solo_performance():
                return False

        return True

    def test_and_set_team(self, lst, count):
        combs = combinations(lst, count)
        for comb in combs:
            team_found_statgroup_id = self.selected_players_are_premade(comb)
            if team_found_statgroup_id != None:
                #performance = self.playercard_collection.get_team_performance(team_found_statgroup_id)
                performance = self.set_team_performance_for_players(comb, team_found_statgroup_id)
                self.teams.append(performance)
                return self.other_in_list(lst, comb)
        return lst

    def set_team_performance_for_players(self, comb, performance):
        for player in comb:
            player.set_performance(performance)
        return performance

    def get_ladder_id(self, count: int, is_axis):
        index = [1, 0][is_axis]
        return [[0], [1], [20, 21], [22, 23], [24, 25]][count][index]

    def selected_players_are_premade(self, players):
        count = len(players)
        ladder_id = self.get_ladder_id(count, self.is_axis)

        test_lists = [player.playercard.get_team_statgroup_list(ladder_id) for player in players]
        return self.all_lists_contain_same_element(test_lists)

    def all_lists_contain_same_element(self, lists: list):
        counter = dict()
        limit = len(lists)

        for lst in lists:
            for ele in lst:
                if ele in counter:
                    counter[ele] += 1
                    if counter[ele] == limit:
                        return ele
                else:
                    counter[ele] = 1

        return None

    def other_in_list(self, main_iter: list, exist_iter):
        for ele in exist_iter:
            main_iter.remove(ele)
        return main_iter

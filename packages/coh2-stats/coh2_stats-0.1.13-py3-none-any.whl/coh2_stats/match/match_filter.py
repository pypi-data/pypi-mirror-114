from coh2_stats.match.match_statistics import MatchStatistics

class MatchFilter:
    def __init__(self, match: MatchStatistics, playercard_collection) -> None:
        self.match = match
        self.playercard_collection = playercard_collection

    def evaluate(self):
        if not self.match.detail.is_qualified(self.playercard_collection):
            return False
        return True

import datetime
class BeforeUpdateMatchFilter(MatchFilter):
    def __init__(self, match: MatchStatistics, playercard_collection) -> None:
        super().__init__(match, playercard_collection)

    def evaluate(self):
        base_bool = super().evaluate()
        is_before_update = self.match.time.get_matchstart_datetime() <= datetime.datetime(2021, 6, 16, 10, 0)
        return is_before_update and base_bool

class AfterUpdateMatchFilter(MatchFilter):
    def __init__(self, match: MatchStatistics, playercard_collection) -> None:
        super().__init__(match, playercard_collection)

    def evaluate(self):
        base_bool = super().evaluate()
        is_before_update = self.match.time.get_matchstart_datetime() > datetime.datetime(2021, 6, 16, 10, 0)
        return is_before_update and base_bool
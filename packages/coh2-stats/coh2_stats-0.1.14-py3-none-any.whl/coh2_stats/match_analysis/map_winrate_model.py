from coh2_stats.match_analysis.match_time_intervals import MatchTimeIntervals
from coh2_stats.match.match_statistics import MatchStatistics

class MapWinrateModel:
    def __init__(self, map_name: str, intervals: MatchTimeIntervals, observed_side: str) -> None:
        self.map_name = map_name
        self.intervals = intervals
        self.match_sets = dict()
        self.observed_side = observed_side
        for i in range(len(intervals) + 1):
            self.match_sets[i] = []

    def categorized_from_interval(self, match: MatchStatistics):
        index = self.intervals.get_index(match.time)
        self.match_sets[index].append(match)

    def __getitem__(self, key):
        if key not in self.match_sets:
            return None
        return self.match_sets[key]

    def get_wr(self):
        return ObservedSideWinrate(self.match_sets, self.observed_side)

    def __repr__(self):
        ob_side_wr = self.get_wr()
        return f'{self.map_name}, {ob_side_wr}'

    #def check_qualification(match: MatchStatistics)

class ObservedSideWinrate:
    def __init__(self, match_sets: dict, observed_side = "axis") -> None:
        self.match_sets = match_sets
        self.observed_side = observed_side
        self.side_wrf = dict()
        self.parse_info()

    def parse_info(self):
        #match.detail.winner = "allies, axis"
        all_total = 0
        all_side_win = 0
        self.total_wrf = WinrateFormula(0, 0)
        for interval, matches in self.match_sets.items():
            sub_total = 0
            side_win = 0

            self.side_wrf[interval] = WinrateFormula(0, 0)
            for match in matches:
                if match.detail.winner not in ["allies", "axis"]:
                    continue

                if match.detail.winner == self.observed_side:
                    side_win += 1
                    all_side_win += 1
                sub_total += 1
                all_total += 1

                self.side_wrf[interval] = WinrateFormula(side_win, sub_total)

            self.total_wrf = WinrateFormula(all_side_win, all_total)


    def __repr__(self) -> str:
        wr_list = [ f'{wr}' for wr in self.side_wrf.values()]
        wr_list.append(f'{self.total_wrf}')
        return ','.join(wr_list)

class WinrateFormula:
    def __init__(self, amount, total) -> None:
        self.amount = amount
        self.total = total
        self.show_formula = True
        self.calculate_wr()

    def add(self, other):
        self.amount += other.amount
        self.total += other.total
        self.calculate_wr()

    def calculate_wr(self):
        if self.total == 0:
            self.wr = None
        else:
            self.wr = round(self.amount / self.total, 2)

    def __repr__(self) -> str:
        if self.total == 0:
            return "NA"
        if self.show_formula:
            return f"{self.amount}/{self.total}={self.wr}"
        else:
            return str(self.wr)


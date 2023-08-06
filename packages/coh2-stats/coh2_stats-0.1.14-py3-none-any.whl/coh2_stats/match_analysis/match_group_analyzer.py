from coh2_stats.query.coh2_io import Coh2IO
from coh2_stats.match.match_collection import MatchCollection
from coh2_stats.match_analysis.map_statistics import MapStatistics
from coh2_stats.match_analysis.map_winrate_model import MapWinrateModel
from coh2_stats.match_analysis.match_time_intervals import MatchTimeIntervals
from coh2_stats.match.match_statistics import MatchStatistics

class MatchGroupAnalyzer:
    def __init__(self, match_collection: MatchCollection):
        self.match_collection = match_collection
        self.matches = match_collection.matches

        seconds_per_min = 60
        interval_markers = [i * seconds_per_min for i in [13, 25, 35] ]
        self.intervals = MatchTimeIntervals(interval_markers)

        self.map_stats = self.analyze()

    def analyze(self):
        self.map_columns = dict()
        for match in self.matches:
            self._put_into_map_columns(match)

        map_stats = MapStatistics(len(self.intervals))
        for map, column in self.map_columns.items():
            model = self._get_map_winrate_model(map, column, "axis")
            map_stats.add_map_winrate_model(model)

        return map_stats

    def _put_into_map_columns(self, match: MatchStatistics):
        if match.map in self.map_columns:
            self.map_columns[match.map].append(match)
        else:
            self.map_columns[match.map] = []
            self.map_columns[match.map].append(match)

    def _get_map_winrate_model(self, map_name, column, observed_side):
        map_wr_model = MapWinrateModel(map_name, self.intervals, observed_side)
        for match in column:
            map_wr_model.categorized_from_interval(match)
        return map_wr_model

    def save(self):
        pass

    def __repr__(self) -> str:
        info = f"{self.match_collection}\n{self.map_stats}"
        return info

    def save_to_csv(self):
        io = Coh2IO("output", "csv")
        io.write_str(str(self.map_stats), f"{self.match_collection.collection_name}_analysis")

    def __len__(self):
        return len(self.time_markers)

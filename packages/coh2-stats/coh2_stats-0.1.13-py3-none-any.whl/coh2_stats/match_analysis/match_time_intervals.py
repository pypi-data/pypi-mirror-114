from coh2_stats.match.match_time import MatchTime
class MatchTimeIntervals:
    def __init__(self, time_markers = []) -> None:
        self.time_markers = sorted(time_markers)

    def get_index(self, match_time: MatchTime):
        time_in_seconds = match_time.duration
        markers_copy = self.time_markers[:]
        markers_copy.append(time_in_seconds)
        list.sort(markers_copy)
        return markers_copy.index(time_in_seconds)

    def __len__(self):
        return len(self.time_markers)
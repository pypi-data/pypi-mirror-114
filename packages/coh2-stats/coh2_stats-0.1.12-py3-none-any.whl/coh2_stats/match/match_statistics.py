from coh2_stats.match.match_time import MatchTime
from coh2_stats.match.match_detail import MatchDetail    

class MatchStatistics:
    def __init__(self, data) -> None:
        self.data = data

        self.match_id = data['id']
        self.match_type = data['description']

        self.map = data['mapname']
        
        start_time = data['startgametime']
        end_time = data['completiontime']
        self.time = MatchTime(start_time, end_time)

        self.apply_match_detail()

    def apply_match_detail(self):
        try:
            match_result = self.data['matchhistoryreportresults']
        except:
            print("error")
            return False
        self.detail = MatchDetail(match_result)

    def __repr__(self):
        return f"{self.map},{self.time},{self.detail}"
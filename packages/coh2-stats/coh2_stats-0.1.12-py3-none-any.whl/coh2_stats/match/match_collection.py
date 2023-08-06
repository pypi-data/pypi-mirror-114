from coh2_stats.match.match_statistics import MatchStatistics
from coh2_stats.query.coh2_io import Coh2IO
from coh2_stats.utils.serialization import PickleSerialization

class MatchCollection(PickleSerialization):
    def __init__(self, collection_name: str, matches = []) -> str:
        self.matches:list[MatchStatistics] = matches[:]
        self.collection_name = collection_name
        self.analyze_basic_info()
        super().__init__("match_collection", collection_name)

    def analyze_basic_info(self):
        date_match_dict = dict()
        for match in self.matches:

            match_date = match.time.date()
            if match_date not in date_match_dict:
                date_match_dict[match_date] = []

            date_match_dict[match_date].append(match)

        import collections
        ordered_dict = collections.OrderedDict(sorted(date_match_dict.items()))

        self.date_match_od = ordered_dict

        #for match_date, match_list in ordered_dict.items():
            #info += f"{match_date}: {len(match_list)}\n"
    
    @property
    def first_date(self):
        self.analyze_basic_info()
        return list(self.date_match_od.keys())[0]

    @property
    def last_date(self):
        self.analyze_basic_info()
        return list(self.date_match_od.keys())[-1]

    @property
    def length(self):
        return len(self.matches)

    def get_matches_description_list(self):
        return [str(match).split(',') for match in self.matches]

    def change_name_to(self, savefile):
        self.collection_name = savefile
        self.savefile = savefile

    def save_to_csv(self):
        io = Coh2IO("output", "csv")
        data = '\n'.join([str(match) for match in self.matches])
        io.write_str(data, self.collection_name)

    def add(self, match):
        self.matches.append(match)

    def add_list(self, matches):
        self.matches.extend(matches)

    def filter_by_playercard_collection(self, playercard_ollection):
        predicate = lambda match: match.detail.is_qualified(playercard_ollection)
        self.filter(predicate)
        return self

    def filter_to_today_only(self):
        import datetime
        today = datetime.datetime.now()
        today_repr = tuple(int(x) for x in today.strftime("%m/%d").split('/'))
        predicate = lambda match: match.time.in_range_date(today_repr, today_repr)
        self.filter(predicate)
        return self

    def filter(self, predicate):
        result = []
        for match in self.matches:
            if predicate(match):
                result.append(match)
        self.matches = result
        return self

    def __repr__(self) -> str:
        info = f"{self.collection_name}: totally {len(self.matches)}:\n" 
        self.analyze_basic_info()

        for match_date, match_list in self.date_match_od.items():
            info += f"{match_date}: {len(match_list)}\n"

        return info



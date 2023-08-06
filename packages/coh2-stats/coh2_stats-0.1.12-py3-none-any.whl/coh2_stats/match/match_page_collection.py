from coh2_stats.match.match_page import MatchPage
class MatchPageCollection():
    def __init__(self, pages) -> None:  
        self.pages = pages

    def get_match_stats_list(self):
        match_list = []
        for page in self.pages:
            match_list.extend(MatchPage(page).get_match_list())
        return match_list


from abc import abstractmethod
class Collection:
    @abstractmethod
    def get_parsed_pages(self):
        return

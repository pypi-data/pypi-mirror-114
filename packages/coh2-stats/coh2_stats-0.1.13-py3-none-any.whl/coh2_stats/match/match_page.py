from coh2_stats.page.page import PageMatchHistoryStats

class MatchPage(PageMatchHistoryStats):
    def __init__(self, page) -> None:
        super().__init__(page)
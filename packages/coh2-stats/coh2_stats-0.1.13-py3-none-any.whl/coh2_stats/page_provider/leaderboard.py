from coh2_stats.performance.performance import Performance
from coh2_stats.leaderboard.leaderboard_page import LeaderboardPage
from coh2_stats.leaderboard.leaderboard_page import LeaderboardPage
from coh2_stats.query.page_provider import PageFromInternet
from coh2_stats.query.api_commands import UrlWithApiCommands
from coh2_stats.utils.interval import Interval
from coh2_stats.page_provider.page_data_provider import PageDataProvider
from coh2_stats.leaderboard.leaderboard_constants import LeaderboardConstants

class LeaderboardPageProvider(PageDataProvider):
    def __init__(self, ladder_id, start, count) -> None:
        cache_folder_str = "leaderboard"
        super().__init__(cache_folder_str)
        self.ladder_id = ladder_id
        self.start = start
        self.count = count

    def get_performance_list(self):
        performance_list = []
        for page in self.pages:
            player_performances = LeaderboardPage(page).get_player_performances(page)
            for performance_data in player_performances:
                performance = Performance(performance_data)
                performance_list.append(performance)

        return performance_list

    def _download_from_internet(self):
        pages = []
        for interval in Interval().generate(1, self.count, 100):
            start = interval[0]
            end = interval[1]
            url = UrlWithApiCommands().get_leaderboard(self.ladder_id, start, 100)
            page = PageFromInternet().get(url)
            pages.append(page)
        return pages

    def get_savefile_string(self):
        return f"{LeaderboardConstants.id_to_ladder_name[self.ladder_id]}-{self.start}-{self.count}"

    def get_player_list(self):
        player_id_list = []
        for page in self.pages:
            leaderboard_page = LeaderboardPage(page)
            player_id_list.extend(leaderboard_page.get_player_ids())
        return player_id_list

    def __repr__(self):
        return f"{self.get_savefile_string()} with pages of length {len(self.pages)}"

from coh2_stats.query.page_provider import PageFromInternet
from coh2_stats.query.api_commands import UrlWithApiCommands
from coh2_stats.page_provider.page_data_provider import PageDataProvider
from coh2_stats.utils.interval import Interval

class RecentMatchPageProvider(PageDataProvider):
    def __init__(self, player_id_list) -> None:
        cache_folder_str = "recent_match"
        self.player_id_list = player_id_list
        super().__init__(cache_folder_str)

    def _download_from_internet(self):
        count = len(self.player_id_list)
        pages = []
        for start, end in Interval().generate(0, count, 100):
            url = UrlWithApiCommands.get_recent_match_history(self.player_id_list[start: end])
            page = PageFromInternet().get(url)
            pages.append(page)
        return pages

    def _get_savefile_string(self):
        return "recent_match_pages"

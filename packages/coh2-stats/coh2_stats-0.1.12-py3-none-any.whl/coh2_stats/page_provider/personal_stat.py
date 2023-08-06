from coh2_stats.performance.performance_page import PerformancePage
from coh2_stats.performance.performance_page_collection import PerformancePageCollection
from coh2_stats.query.page_provider import PageFromInternet
from coh2_stats.query.api_commands import UrlWithApiCommands
from coh2_stats.utils.interval import Interval

from coh2_stats.page_provider.page_data_provider import PageDataProvider

class PersonalStatPageProvider(PageDataProvider):
    def __init__(self, player_id_list) -> None:
        cache_folder_str = "personal_stat"
        self.player_id_list = player_id_list
        super().__init__(cache_folder_str=cache_folder_str)
    
    def get_performance_page_list(self):
        return PerformancePageCollection(self.pages).get_performance_page_list()

    def _download_from_internet(self):
        count = len(self.player_id_list)
        pages = []
        for start, end in Interval().generate(0, count, 100):
            url = UrlWithApiCommands.get_personal_stat(self.player_id_list[start: end])
            page = PageFromInternet().get(url)
            pages.append(page)
        return pages

    def get_savefile_string(self):
        return f"PersonalStat"
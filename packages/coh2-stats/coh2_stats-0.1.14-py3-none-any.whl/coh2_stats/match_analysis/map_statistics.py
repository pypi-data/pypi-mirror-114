from coh2_stats.match_analysis.map_winrate_model import MapWinrateModel, WinrateFormula
class MapStatistics:
    def __init__(self, interval_count) -> None:
        self.database = dict()
        self.interval_count = interval_count

    def add_map_winrate_model(self, map_wr_model: MapWinrateModel):
        self.database[map_wr_model.map_name] = map_wr_model

        #for value in self.database.values():
            #map_wr_model

    def analyze_table(self):
        wr_table = []

        all_total_wrf = WinrateFormula(0, 0)
        for map_wr in self.database.values():
            wr_table.append(str(map_wr).split(','))
            total_wrf = map_wr.get_wr().total_wrf
            all_total_wrf.add(total_wrf)

        total_data = []
        for i in range(self.interval_count + 1):
            column_wrf = WinrateFormula(0, 0)

            for map_wr in self.database.values():
                side_wrf = map_wr.get_wr().side_wrf[i]
                column_wrf.add(side_wrf)

            total_data.append(column_wrf)

        total_data.append(all_total_wrf)

        all_wr_row = [ f'{wr}' for wr in total_data]
        all_wr_row.insert(0, 'all')
        wr_table.append(all_wr_row)

        return wr_table
        
    def __repr__(self) -> str:
        info = ""
        all_total_wrf = WinrateFormula(0, 0)
        for map_wr in self.database.values():
            info += f"{map_wr}\n"
            total_wrf = map_wr.get_wr().total_wrf
            all_total_wrf.add(total_wrf)

        total_data = []
        for i in range(self.interval_count + 1):
            column_wrf = WinrateFormula(0, 0)

            for map_wr in self.database.values():
                side_wrf = map_wr.get_wr().side_wrf[i]
                column_wrf.add(side_wrf)

            total_data.append(column_wrf)

        total_data.append(all_total_wrf)

        wr_list = [ f'{wr}' for wr in total_data]
        wr_list.insert(0, 'all')
        info += ','.join(wr_list)

        return info

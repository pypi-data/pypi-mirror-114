from coh2_stats.performance.performance import Performance

class PlayerPerformance:

    def __init__(self) -> None:
        self.database = dict()
    
    def update(self, performance: Performance):
        if performance.is_4s_solo:
            self.database[performance.ladder_id] = performance
        else:
            self.update_team_performance(performance)

    def update_team_performance(self, performance: Performance):
        if performance.ladder_id not in self.database:
            self.database[performance.ladder_id] = []
        self.database[performance.ladder_id].append(performance)

    def get_team_statgroup_list(self, ladder_id):
        if ladder_id not in self.database:
            return []
        return self.database[ladder_id]

    def __getitem__(self, value):
        if value in self.database:
            return self.database[value]
        return None

    def __repr__(self) -> str:
        info = ""
        for ladder_id, performance_info in self.database.items():
            if type(performance_info) is Performance:
                info += f"{ladder_id}: {performance_info}\n"
            elif type(performance_info) is list:
                for performance in performance_info:
                    info += f"{ladder_id}: {performance}\n"
            else:
                info += f"{ladder_id}: unknown"
        return info
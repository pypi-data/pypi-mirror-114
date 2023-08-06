from typing import Match
from coh2_stats.match.match_statistics import MatchStatistics

def four_vs_four_match(match: MatchStatistics):
    return match.detail.player_count == 8

def both_team_must_have_at_least_one_arranged_team(match: MatchStatistics):
    return \
        len(match.detail.matchside_allies.teams) != 0 and\
        len(match.detail.matchside_axis.teams) != 0

def lasts_longer_than_five_minutes(match: MatchStatistics):
    seconds_per_minute = 60
    return match.time.duration > 5 * seconds_per_minute
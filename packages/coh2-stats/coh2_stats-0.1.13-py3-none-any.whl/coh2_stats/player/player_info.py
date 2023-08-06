#from StatGroup.StatGroup import Member
class Member:
    pass

class PlayerInfo:
    def __init__(self, profile_id, alias) -> None:
        self.profile_id = profile_id
        self.alias = alias
        pass

    @classmethod
    def create_from_member(cls, member: Member):
        return PlayerInfo(member.profile_id, member.alias)

    def __repr__(self) -> str:
        return f"{self.profile_id} {self.alias}"

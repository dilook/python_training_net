from sys import maxsize


class Project:
    def __init__(self, name, description, id=None, ):
        self.id = id
        self.name = name
        self.description = description

    def __eq__(self, other):
        return (self.id == other.id or self.id is None or other.id is None) and \
               self.name == other.name and self.description == other.description

    def __repr__(self):
        return f"{self.name}:{self.description}"

    def __lt__(self, other):
        return self.get_id_or_max() < other.get_id_or_max()

    def get_id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            return maxsize
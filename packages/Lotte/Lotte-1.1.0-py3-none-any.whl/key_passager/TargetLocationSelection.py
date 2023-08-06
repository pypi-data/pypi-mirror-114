class TargetLocationSelection:
    def __init__(self, target_text_id, target_location_id):
        self.target_text_id = target_text_id
        self.target_location_ids = [target_location_id]

    @classmethod
    def from_list(cls, target_text_id, target_location_ids):  # pragma: no cover
        return cls(target_text_id, target_location_ids)

    def add_target_location_id(self, target_location_id):
        if target_location_id not in self.target_location_ids:
            self.target_location_ids.append(target_location_id)

from typing import List, Optional


class PolicyObjects:
    def __init__(self, data: dict):
        self._data: dict = data
    
    def get_all(self, object_type: str) -> List[dict]:
        return self._data.get(object_type, [])
    
    def get(self, object_type: str, object_id: int) -> Optional[dict]:
        for o in self.get_all(object_type):
            if o.get("Object_ID", 0) == object_id:
                return o
        return None

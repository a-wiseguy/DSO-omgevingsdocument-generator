from copy import deepcopy
from typing import Dict, List, Optional

from app.input_data.resource.policy_object.policy_object import PolicyObject


class PolicyObjectRepository:
    def __init__(self):
        self._data: Dict[str, List[PolicyObject]] = {}

    def add(self, object_code: str, policy_object: dict):
        self._data[object_code] = PolicyObject(policy_object)

    def add_list(self, policy_objects: List[dict]):
        for policy_object in policy_objects:
            self.add(
                f"{policy_object['Object_Type']}-{policy_object['Object_ID']}",
                policy_object,
            )

    def get_all(self, object_type: str) -> List[PolicyObject]:
        return deepcopy(self._data.get(object_type, []))

    def get_optional(self, object_type: str, object_id: int) -> Optional[PolicyObject]:
        for o in self.get_all(object_type):
            if o.get("Object_ID", 0) == object_id:
                return o
        return None

    def get(self, object_type: str, object_id: int) -> PolicyObject:
        o: Optional[PolicyObject] = self.get_optional(object_type, object_id)
        if o is None:
            raise RuntimeError(f"Can not find object {object_type}-{object_id}")
        return o

from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.api_value_floating_with_out_units_name import ApiValueFloatingWithOutUnitsName
from ..types import UNSET, Unset

T = TypeVar("T", bound="ApiValueWithUnitsCompositionArray")


@attr.s(auto_attribs=True)
class ApiValueWithUnitsCompositionArray:
    """Holds compositioninfo"""

    values: Union[Unset, None, List[ApiValueFloatingWithOutUnitsName]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        values: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.values, Unset):
            if self.values is None:
                values = None
            else:
                values = []
                for values_item_data in self.values:
                    values_item = values_item_data.to_dict()

                    values.append(values_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if values is not UNSET:
            field_dict["values"] = values

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        values = []
        _values = d.pop("values", UNSET)
        for values_item_data in _values or []:
            values_item = ApiValueFloatingWithOutUnitsName.from_dict(values_item_data)

            values.append(values_item)

        api_value_with_units_composition_array = cls(
            values=values,
        )

        return api_value_with_units_composition_array

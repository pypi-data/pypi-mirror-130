from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.api_output_calculation_result_phase import ApiOutputCalculationResultPhase
from ..models.api_value_with_units_pressure import ApiValueWithUnitsPressure
from ..models.api_value_with_units_temperature import ApiValueWithUnitsTemperature
from ..types import UNSET, Unset

T = TypeVar("T", bound="ApiOutputCalculationResultPoint")


@attr.s(auto_attribs=True)
class ApiOutputCalculationResultPoint:
    """Result for a point"""

    temperature: Union[Unset, ApiValueWithUnitsTemperature] = UNSET
    pressure: Union[Unset, ApiValueWithUnitsPressure] = UNSET
    phases: Union[Unset, None, List[ApiOutputCalculationResultPhase]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        temperature: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.temperature, Unset):
            temperature = self.temperature.to_dict()

        pressure: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pressure, Unset):
            pressure = self.pressure.to_dict()

        phases: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.phases, Unset):
            if self.phases is None:
                phases = None
            else:
                phases = []
                for phases_item_data in self.phases:
                    phases_item = phases_item_data.to_dict()

                    phases.append(phases_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if pressure is not UNSET:
            field_dict["pressure"] = pressure
        if phases is not UNSET:
            field_dict["phases"] = phases

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _temperature = d.pop("temperature", UNSET)
        temperature: Union[Unset, ApiValueWithUnitsTemperature]
        if isinstance(_temperature, Unset):
            temperature = UNSET
        else:
            temperature = ApiValueWithUnitsTemperature.from_dict(_temperature)

        _pressure = d.pop("pressure", UNSET)
        pressure: Union[Unset, ApiValueWithUnitsPressure]
        if isinstance(_pressure, Unset):
            pressure = UNSET
        else:
            pressure = ApiValueWithUnitsPressure.from_dict(_pressure)

        phases = []
        _phases = d.pop("phases", UNSET)
        for phases_item_data in _phases or []:
            phases_item = ApiOutputCalculationResultPhase.from_dict(phases_item_data)

            phases.append(phases_item)

        api_output_calculation_result_point = cls(
            temperature=temperature,
            pressure=pressure,
            phases=phases,
        )

        return api_output_calculation_result_point

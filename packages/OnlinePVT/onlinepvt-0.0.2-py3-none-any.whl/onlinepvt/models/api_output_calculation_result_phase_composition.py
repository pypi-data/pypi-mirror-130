from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.api_value_floating_with_out_units import ApiValueFloatingWithOutUnits
from ..models.api_value_with_units_composition_array import ApiValueWithUnitsCompositionArray
from ..types import UNSET, Unset

T = TypeVar("T", bound="ApiOutputCalculationResultPhaseComposition")


@attr.s(auto_attribs=True)
class ApiOutputCalculationResultPhaseComposition:
    """Holds composition information for a phase"""

    composition_units: Union[Unset, None, str] = UNSET
    molar_mass_units: Union[Unset, None, str] = UNSET
    polymer_massfraction: Union[Unset, ApiValueFloatingWithOutUnits] = UNSET
    composition: Union[Unset, ApiValueWithUnitsCompositionArray] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        composition_units = self.composition_units
        molar_mass_units = self.molar_mass_units
        polymer_massfraction: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.polymer_massfraction, Unset):
            polymer_massfraction = self.polymer_massfraction.to_dict()

        composition: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.composition, Unset):
            composition = self.composition.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if composition_units is not UNSET:
            field_dict["compositionUnits"] = composition_units
        if molar_mass_units is not UNSET:
            field_dict["molarMassUnits"] = molar_mass_units
        if polymer_massfraction is not UNSET:
            field_dict["polymerMassfraction"] = polymer_massfraction
        if composition is not UNSET:
            field_dict["composition"] = composition

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        composition_units = d.pop("compositionUnits", UNSET)

        molar_mass_units = d.pop("molarMassUnits", UNSET)

        _polymer_massfraction = d.pop("polymerMassfraction", UNSET)
        polymer_massfraction: Union[Unset, ApiValueFloatingWithOutUnits]
        if isinstance(_polymer_massfraction, Unset):
            polymer_massfraction = UNSET
        else:
            polymer_massfraction = ApiValueFloatingWithOutUnits.from_dict(_polymer_massfraction)

        _composition = d.pop("composition", UNSET)
        composition: Union[Unset, ApiValueWithUnitsCompositionArray]
        if isinstance(_composition, Unset):
            composition = UNSET
        else:
            composition = ApiValueWithUnitsCompositionArray.from_dict(_composition)

        api_output_calculation_result_phase_composition = cls(
            composition_units=composition_units,
            molar_mass_units=molar_mass_units,
            polymer_massfraction=polymer_massfraction,
            composition=composition,
        )

        return api_output_calculation_result_phase_composition

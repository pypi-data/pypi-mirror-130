from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.api_output_calculation_result_phase_composition import ApiOutputCalculationResultPhaseComposition
from ..models.api_output_calculation_result_phase_polymer_moments import ApiOutputCalculationResultPhasePolymerMoments
from ..models.api_value_with_units_density import ApiValueWithUnitsDensity
from ..models.api_value_with_units_enthalpy import ApiValueWithUnitsEnthalpy
from ..models.api_value_with_units_entropy import ApiValueWithUnitsEntropy
from ..models.api_value_with_units_volume import ApiValueWithUnitsVolume
from ..models.api_value_with_units_volume_mole_percent import ApiValueWithUnitsVolumeMolePercent
from ..models.api_value_with_units_volume_weight_percent import ApiValueWithUnitsVolumeWeightPercent
from ..types import UNSET, Unset

T = TypeVar("T", bound="ApiOutputCalculationResultPhase")


@attr.s(auto_attribs=True)
class ApiOutputCalculationResultPhase:
    """Holds all properties for a phase"""

    phase_label: Union[Unset, None, str] = UNSET
    volume: Union[Unset, ApiValueWithUnitsVolume] = UNSET
    density: Union[Unset, ApiValueWithUnitsDensity] = UNSET
    entropy: Union[Unset, ApiValueWithUnitsEntropy] = UNSET
    enthalpy: Union[Unset, ApiValueWithUnitsEnthalpy] = UNSET
    mole_percent: Union[Unset, ApiValueWithUnitsVolumeMolePercent] = UNSET
    weight_percent: Union[Unset, ApiValueWithUnitsVolumeWeightPercent] = UNSET
    polymer_moments: Union[Unset, ApiOutputCalculationResultPhasePolymerMoments] = UNSET
    composition: Union[Unset, ApiOutputCalculationResultPhaseComposition] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        phase_label = self.phase_label
        volume: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.volume, Unset):
            volume = self.volume.to_dict()

        density: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.density, Unset):
            density = self.density.to_dict()

        entropy: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.entropy, Unset):
            entropy = self.entropy.to_dict()

        enthalpy: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.enthalpy, Unset):
            enthalpy = self.enthalpy.to_dict()

        mole_percent: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.mole_percent, Unset):
            mole_percent = self.mole_percent.to_dict()

        weight_percent: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.weight_percent, Unset):
            weight_percent = self.weight_percent.to_dict()

        polymer_moments: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.polymer_moments, Unset):
            polymer_moments = self.polymer_moments.to_dict()

        composition: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.composition, Unset):
            composition = self.composition.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if phase_label is not UNSET:
            field_dict["phaseLabel"] = phase_label
        if volume is not UNSET:
            field_dict["volume"] = volume
        if density is not UNSET:
            field_dict["density"] = density
        if entropy is not UNSET:
            field_dict["entropy"] = entropy
        if enthalpy is not UNSET:
            field_dict["enthalpy"] = enthalpy
        if mole_percent is not UNSET:
            field_dict["molePercent"] = mole_percent
        if weight_percent is not UNSET:
            field_dict["weightPercent"] = weight_percent
        if polymer_moments is not UNSET:
            field_dict["polymerMoments"] = polymer_moments
        if composition is not UNSET:
            field_dict["composition"] = composition

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        phase_label = d.pop("phaseLabel", UNSET)

        _volume = d.pop("volume", UNSET)
        volume: Union[Unset, ApiValueWithUnitsVolume]
        if isinstance(_volume, Unset):
            volume = UNSET
        else:
            volume = ApiValueWithUnitsVolume.from_dict(_volume)

        _density = d.pop("density", UNSET)
        density: Union[Unset, ApiValueWithUnitsDensity]
        if isinstance(_density, Unset):
            density = UNSET
        else:
            density = ApiValueWithUnitsDensity.from_dict(_density)

        _entropy = d.pop("entropy", UNSET)
        entropy: Union[Unset, ApiValueWithUnitsEntropy]
        if isinstance(_entropy, Unset):
            entropy = UNSET
        else:
            entropy = ApiValueWithUnitsEntropy.from_dict(_entropy)

        _enthalpy = d.pop("enthalpy", UNSET)
        enthalpy: Union[Unset, ApiValueWithUnitsEnthalpy]
        if isinstance(_enthalpy, Unset):
            enthalpy = UNSET
        else:
            enthalpy = ApiValueWithUnitsEnthalpy.from_dict(_enthalpy)

        _mole_percent = d.pop("molePercent", UNSET)
        mole_percent: Union[Unset, ApiValueWithUnitsVolumeMolePercent]
        if isinstance(_mole_percent, Unset):
            mole_percent = UNSET
        else:
            mole_percent = ApiValueWithUnitsVolumeMolePercent.from_dict(_mole_percent)

        _weight_percent = d.pop("weightPercent", UNSET)
        weight_percent: Union[Unset, ApiValueWithUnitsVolumeWeightPercent]
        if isinstance(_weight_percent, Unset):
            weight_percent = UNSET
        else:
            weight_percent = ApiValueWithUnitsVolumeWeightPercent.from_dict(_weight_percent)

        _polymer_moments = d.pop("polymerMoments", UNSET)
        polymer_moments: Union[Unset, ApiOutputCalculationResultPhasePolymerMoments]
        if isinstance(_polymer_moments, Unset):
            polymer_moments = UNSET
        else:
            polymer_moments = ApiOutputCalculationResultPhasePolymerMoments.from_dict(_polymer_moments)

        _composition = d.pop("composition", UNSET)
        composition: Union[Unset, ApiOutputCalculationResultPhaseComposition]
        if isinstance(_composition, Unset):
            composition = UNSET
        else:
            composition = ApiOutputCalculationResultPhaseComposition.from_dict(_composition)

        api_output_calculation_result_phase = cls(
            phase_label=phase_label,
            volume=volume,
            density=density,
            entropy=entropy,
            enthalpy=enthalpy,
            mole_percent=mole_percent,
            weight_percent=weight_percent,
            polymer_moments=polymer_moments,
            composition=composition,
        )

        return api_output_calculation_result_phase

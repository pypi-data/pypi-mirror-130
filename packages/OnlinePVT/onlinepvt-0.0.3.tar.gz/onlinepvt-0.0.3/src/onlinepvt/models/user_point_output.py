from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserPointOutput")


@attr.s(auto_attribs=True)
class UserPointOutput:
    """Output requested by user"""

    composition: Union[Unset, bool] = UNSET
    phase_fractions: Union[Unset, bool] = UNSET
    density: Union[Unset, bool] = UNSET
    molar_volume: Union[Unset, bool] = UNSET
    compressibility: Union[Unset, bool] = UNSET
    enthalpy: Union[Unset, bool] = UNSET
    entropy: Union[Unset, bool] = UNSET
    heat_capacity: Union[Unset, bool] = UNSET
    velocity_of_sound: Union[Unset, bool] = UNSET
    joule_thomson_coefficient: Union[Unset, bool] = UNSET
    molecular_weight: Union[Unset, bool] = UNSET
    distribution: Union[Unset, bool] = UNSET
    mn_mw_mz: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        composition = self.composition
        phase_fractions = self.phase_fractions
        density = self.density
        molar_volume = self.molar_volume
        compressibility = self.compressibility
        enthalpy = self.enthalpy
        entropy = self.entropy
        heat_capacity = self.heat_capacity
        velocity_of_sound = self.velocity_of_sound
        joule_thomson_coefficient = self.joule_thomson_coefficient
        molecular_weight = self.molecular_weight
        distribution = self.distribution
        mn_mw_mz = self.mn_mw_mz

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if composition is not UNSET:
            field_dict["composition"] = composition
        if phase_fractions is not UNSET:
            field_dict["phaseFractions"] = phase_fractions
        if density is not UNSET:
            field_dict["density"] = density
        if molar_volume is not UNSET:
            field_dict["molarVolume"] = molar_volume
        if compressibility is not UNSET:
            field_dict["compressibility"] = compressibility
        if enthalpy is not UNSET:
            field_dict["enthalpy"] = enthalpy
        if entropy is not UNSET:
            field_dict["entropy"] = entropy
        if heat_capacity is not UNSET:
            field_dict["heatCapacity"] = heat_capacity
        if velocity_of_sound is not UNSET:
            field_dict["velocityOfSound"] = velocity_of_sound
        if joule_thomson_coefficient is not UNSET:
            field_dict["jouleThomsonCoefficient"] = joule_thomson_coefficient
        if molecular_weight is not UNSET:
            field_dict["molecularWeight"] = molecular_weight
        if distribution is not UNSET:
            field_dict["distribution"] = distribution
        if mn_mw_mz is not UNSET:
            field_dict["mnMwMz"] = mn_mw_mz

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        composition = d.pop("composition", UNSET)

        phase_fractions = d.pop("phaseFractions", UNSET)

        density = d.pop("density", UNSET)

        molar_volume = d.pop("molarVolume", UNSET)

        compressibility = d.pop("compressibility", UNSET)

        enthalpy = d.pop("enthalpy", UNSET)

        entropy = d.pop("entropy", UNSET)

        heat_capacity = d.pop("heatCapacity", UNSET)

        velocity_of_sound = d.pop("velocityOfSound", UNSET)

        joule_thomson_coefficient = d.pop("jouleThomsonCoefficient", UNSET)

        molecular_weight = d.pop("molecularWeight", UNSET)

        distribution = d.pop("distribution", UNSET)

        mn_mw_mz = d.pop("mnMwMz", UNSET)

        user_point_output = cls(
            composition=composition,
            phase_fractions=phase_fractions,
            density=density,
            molar_volume=molar_volume,
            compressibility=compressibility,
            enthalpy=enthalpy,
            entropy=entropy,
            heat_capacity=heat_capacity,
            velocity_of_sound=velocity_of_sound,
            joule_thomson_coefficient=joule_thomson_coefficient,
            molecular_weight=molecular_weight,
            distribution=distribution,
            mn_mw_mz=mn_mw_mz,
        )

        return user_point_output

from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.profile_steps import ProfileSteps
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProfileTimeInformation")


@attr.s(auto_attribs=True)
class ProfileTimeInformation:
    """Time information used in profiling"""

    time: Union[Unset, None, str] = UNSET
    milli_seconds: Union[Unset, int] = UNSET
    step: Union[Unset, ProfileSteps] = UNSET
    micro_service: Union[Unset, None, str] = UNSET
    sorting_order: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        time = self.time
        milli_seconds = self.milli_seconds
        step: Union[Unset, str] = UNSET
        if not isinstance(self.step, Unset):
            step = self.step.value

        micro_service = self.micro_service
        sorting_order = self.sorting_order

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if time is not UNSET:
            field_dict["Time"] = time
        if milli_seconds is not UNSET:
            field_dict["milliSeconds"] = milli_seconds
        if step is not UNSET:
            field_dict["step"] = step
        if micro_service is not UNSET:
            field_dict["microService"] = micro_service
        if sorting_order is not UNSET:
            field_dict["sortingOrder"] = sorting_order

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        time = d.pop("Time", UNSET)

        milli_seconds = d.pop("milliSeconds", UNSET)

        _step = d.pop("step", UNSET)
        step: Union[Unset, ProfileSteps]
        if isinstance(_step, Unset):
            step = UNSET
        else:
            step = ProfileSteps(_step)

        micro_service = d.pop("microService", UNSET)

        sorting_order = d.pop("sortingOrder", UNSET)

        profile_time_information = cls(
            time=time,
            milli_seconds=milli_seconds,
            step=step,
            micro_service=micro_service,
            sorting_order=sorting_order,
        )

        return profile_time_information

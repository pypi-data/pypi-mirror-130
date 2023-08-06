import aiohttp
from typing import Any, Dict

from onlinepvt.models.cloud_point_calculation_input import CloudPointCalculationInput
from onlinepvt.models.cloud_point_calculation_result import CloudPointCalculationResult
from onlinepvt.models.flash_calculation_input import FlashCalculationInput
from onlinepvt.models.flash_calculation_result import FlashCalculationResult
from onlinepvt.models.flashed_property_calculation_input import FlashedPropertyCalculationInput
from onlinepvt.models.flashed_property_calculation_result import FlashedPropertyCalculationResult
from onlinepvt.models.new_fluid_input import NewFluidInput
from onlinepvt.models.new_fluid_result import NewFluidResult
from onlinepvt.models.phasediagram_fixed_temperature_pressure_calculation_input import PhasediagramFixedTemperaturePressureCalculationInput
from onlinepvt.models.phasediagram_fixed_temperature_pressure_calculation_result import PhasediagramFixedTemperaturePressureCalculationResult
from onlinepvt.models.problem_details import ProblemDetails
from onlinepvt.models.request_fluid_input import RequestFluidInput
from onlinepvt.models.request_fluid_result import RequestFluidResult
from onlinepvt.models.sle_point_calculation_input import SlePointCalculationInput
from onlinepvt.models.sle_point_calculation_result import SlePointCalculationResult
from onlinepvt.models.unflashed_property_calculation_input import UnflashedPropertyCalculationInput
from onlinepvt.models.unflashed_property_calculation_result import UnflashedPropertyCalculationResult
from onlinepvt.models.units import Units
from onlinepvt.models.units_item import UnitsItem


class OnlinePvtClient:
    """Class for making the calling to OnlinePvt API easy"""

    def __init__(self, base_url, user_id, access_secret):
        self.__base_url = "{}/api/01/".format(base_url)
        self.__user_id = user_id
        self.__access_secret = access_secret
        self.__session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False))

    async def cleanup(self):
        await self.__session.close()

    def __append_body(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """Method that appends user_id and access_secret to the body of the request"""
        user = {
            "userId": self.__user_id,
            "accessSecret": self.__access_secret,
        }
        return {**body, **user}

    async def __post_async(self, endpoint: str, json_body: Dict[str, Any], from_dict):
        """Prepare the URL and the body and makes the POST request to the API"""
        url = "{}{endpoint}".format(self.__base_url, endpoint=endpoint)
        json_body = self.__append_body(json_body)
        try:
            async with self.__session.post(url, json=json_body) as resp:
                response = await resp.json()
                if resp.status == 200:
                    return from_dict(response)
                else:
                    return ProblemDetails.from_dict(response)
        except aiohttp.ClientConnectorError as e:
            print('Connection Error', str(e))
            return ProblemDetails.from_dict(e)

    async def request_fluid_async(
        self,
        body: RequestFluidInput,
    ): return await self.__post_async("Fluid/RequestFluid", body.to_dict(), RequestFluidResult.from_dict)

    async def add_new_fluid_async(
        self,
        body: NewFluidInput,
    ): return await self.__post_async("Fluid/AddNewFluid", body.to_dict(), NewFluidResult.from_dict)

    async def call_flash_async(
        self,
        body: FlashCalculationInput,
    ):
        """Perform flash calculation"""
        return await self.__post_async("Calculation/CallFlash", body.to_dict(), FlashCalculationResult.from_dict)

    async def call_cloud_point_async(
        self,
        body: CloudPointCalculationInput,
    ):
        """Perform cloud point calculation"""
        return await self.__post_async("Calculation/CallCloudPoint", body.to_dict(), CloudPointCalculationResult.from_dict)

    async def call_flashed_properties_async(
        self,
        body: FlashedPropertyCalculationInput,
    ):
        """Perform flash property calculation"""
        return await self.__post_async("Calculation/CallFlashedProperties", body.to_dict(), FlashedPropertyCalculationResult.from_dict)

    async def call_unflashed_properties_async(
        self,
        body: UnflashedPropertyCalculationInput,
    ):
        """Perform un-flash property calculation"""
        return await self.__post_async("Calculation/CallUnflashedProperties", body.to_dict(), UnflashedPropertyCalculationResult.from_dict)

    async def call_sle_point_async(
        self,
        body: SlePointCalculationInput,
    ):
        """Perform SLE point calculation"""
        return await self.__post_async("Calculation/CallSlePoint", body.to_dict(), SlePointCalculationResult.from_dict)

    async def call_calculation_phasediagram_standard_async(
        self,
        body: PhasediagramFixedTemperaturePressureCalculationInput,
    ):
        """Perform Phasediagram standard calculation"""
        return await self.__post_async("Calculation/CallCalculationPhasediagramStandard", body.to_dict(), PhasediagramFixedTemperaturePressureCalculationResult.from_dict)

    def get_flash_input(self):
        """Returns flash argument filled with standard input"""
        return FlashCalculationInput(user_id=self.__user_id, access_secret=self.__access_secret, units=self.__get_units())

    def get_cloud_point_input(self):
        """Returns cloud point argument filled with standard input"""
        return CloudPointCalculationInput(user_id=self.__user_id, access_secret=self.__access_secret, units=self.__get_units())

    def get_flashed_property_Input(self):
        """Returns flashed properties argument filled with standard input"""
        return FlashedPropertyCalculationInput(user_id=self.__user_id, access_secret=self.__access_secret, units=self.__get_units())

    def get_unflashed_property_input(self):
        """Returns un-flashed properties argument filled with standard input"""
        return UnflashedPropertyCalculationInput(user_id=self.__user_id, access_secret=self.__access_secret, units=self.__get_units())

    def get_sle_point_input(self):
        """Returns SLE point argument filled with standard input"""
        return SlePointCalculationInput(user_id=self.__user_id, access_secret=self.__access_secret, units=self.__get_units())

    def get_phasediagam_standard_input(self):
        """Returns phase diagram standard argument filled with standard input"""
        return PhasediagramFixedTemperaturePressureCalculationInput(user_id=self.__user_id, access_secret=self.__access_secret, units=self.__get_units())

    def get_request_fluid_input(self):
        """Returns request fluid argument filled with standard input"""
        return RequestFluidResult(user_id=self.__user_id, access_secret=self.__access_secret)

    def __get_units(self):
        return Units(temperature=UnitsItem(in_="Kelvin", out="Kelvin"), pressure=UnitsItem(in_="Kelvin", out="Kelvin"), composition=UnitsItem(in_="Kelvin", out="Kelvin"), enthalpy=UnitsItem(in_="kJ/Kg", out="kJ/Kg"), entropy=UnitsItem(in_="kJ/(Kg Kelvin)", out="kJ/(Kg Kelvin)"))

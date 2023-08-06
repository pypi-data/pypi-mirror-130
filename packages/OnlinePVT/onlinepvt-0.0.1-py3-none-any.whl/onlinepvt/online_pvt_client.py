import aiohttp
from typing import Any, Dict

from online_pvt_api_client.models.cloud_point_calculation_input import CloudPointCalculationInput
from online_pvt_api_client.models.cloud_point_calculation_result import CloudPointCalculationResult
from online_pvt_api_client.models.flash_calculation_input import FlashCalculationInput
from online_pvt_api_client.models.flash_calculation_result import FlashCalculationResult
from online_pvt_api_client.models.flashed_property_calculation_input import FlashedPropertyCalculationInput
from online_pvt_api_client.models.flashed_property_calculation_result import FlashedPropertyCalculationResult
from online_pvt_api_client.models.new_fluid_input import NewFluidInput
from online_pvt_api_client.models.new_fluid_result import NewFluidResult
from online_pvt_api_client.models.phasediagram_fixed_temperature_pressure_calculation_input import PhasediagramFixedTemperaturePressureCalculationInput
from online_pvt_api_client.models.phasediagram_fixed_temperature_pressure_calculation_result import PhasediagramFixedTemperaturePressureCalculationResult
from online_pvt_api_client.models.problem_details import ProblemDetails
from online_pvt_api_client.models.request_fluid_input import RequestFluidInput
from online_pvt_api_client.models.request_fluid_result import RequestFluidResult
from online_pvt_api_client.models.sle_point_calculation_input import SlePointCalculationInput
from online_pvt_api_client.models.sle_point_calculation_result import SlePointCalculationResult
from online_pvt_api_client.models.unflashed_property_calculation_input import UnflashedPropertyCalculationInput
from online_pvt_api_client.models.unflashed_property_calculation_result import UnflashedPropertyCalculationResult


class OnlinePvtClient:
    """A class for calling the API"""

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
    ): return await self.__post_async("Calculation/CallFlash", body.to_dict(), FlashCalculationResult.from_dict)

    async def call_cloud_point_async(
        self,
        body: CloudPointCalculationInput,
    ): return await self.__post_async("Calculation/CallCloudPoint", body.to_dict(), CloudPointCalculationResult.from_dict)

    async def call_flashed_properties_async(
        self,
        body: FlashedPropertyCalculationInput,
    ): return await self.__post_async("Calculation/CallFlashedProperties", body.to_dict(), FlashedPropertyCalculationResult.from_dict)

    async def call_unflashed_properties_async(
        self,
        body: UnflashedPropertyCalculationInput,
    ): return await self.__post_async("Calculation/CallUnflashedProperties", body.to_dict(), UnflashedPropertyCalculationResult.from_dict)

    async def call_sle_point_async(
        self,
        body: SlePointCalculationInput,
    ): return await self.__post_async("Calculation/CallSlePoint", body.to_dict(), SlePointCalculationResult.from_dict)

    async def call_calculation_phasediagram_standard_async(
        self,
        body: PhasediagramFixedTemperaturePressureCalculationInput,
    ): return await self.__post_async("Calculation/CallCalculationPhasediagramStandard", body.to_dict(), PhasediagramFixedTemperaturePressureCalculationResult.from_dict)

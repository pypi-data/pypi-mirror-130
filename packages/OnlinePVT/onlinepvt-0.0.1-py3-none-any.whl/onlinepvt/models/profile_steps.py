from enum import Enum


class ProfileSteps(str, Enum):
    VALUE_0 = "API start"
    VALUE_1 = "User validated"
    VALUE_2 = "Calculation API called"
    VALUE_3 = "API result logged"
    VALUE_4 = "Begin actual calculation"
    VALUE_5 = "Done actual calculation"
    VALUE_6 = "Format output done"
    VALUE_7 = "Fluid loaded"
    VALUE_8 = "Converted result"
    VALUE_9 = "Calculation result stored"

    def __str__(self) -> str:
        return str(self.value)

# class ProfileSteps(int, Enum):
#     ApiStart = 0
#     "0 - API start"
#     UserValidated = 1
#     "1 - User validated"
#     CalculationApiCalled = 2
#     "2 - Calculation API called"
#     ApiResultLogged = 3
#     "3 - API result logged"
#     BeginActualCalculation = 4
#     "4 - Begin actual calculation"
#     DoneActualCalculation = 5
#     "5 - Done actual calculation"
#     FormatOutputDone = 6
#     "6 - Format output done"
#     FluidLoaded = 7
#     "7 - Fluid loaded"
#     ConvertedResult = 8
#     "8 - Converted result"
#     CalculationResultStored = 9
#     """9 - Calculation result stored"""

#     def __str__(self) -> str:
#         return str(self.value)

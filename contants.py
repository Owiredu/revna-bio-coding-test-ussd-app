from enum import Enum


class USSDUserInputType(Enum):
    """Enumeration of all the expected USSD user inputs
    """
    START_PROMPT: str = ""
    GET_OTP: str = "1"
    CHECK_BALANCE_PROMPT: str = "2"
    CHECK_BALANCE: str = "2*"
    REQUEST_CALLBACK: str = "3"
from fastapi import APIRouter, Depends, Request, BackgroundTasks
from fastapi.responses import PlainTextResponse
import sqlite3
import random
from urllib.parse import parse_qs
from dependencies import get_db
from models.schemas import ussd as ussd_schemas
from contants import USSDUserInputType
from models.crud import (
    user as user_crud,
    ussd as ussd_crud
)
from utils import sms as sms_utils


router = APIRouter()


@router.post(
    path="",
    response_class=PlainTextResponse,
    include_in_schema=False,
)
async def ussd_callback(
    background_tasks: BackgroundTasks,
    req_obj: Request,
    db: sqlite3.Connection = Depends(get_db),
):
    """Handles the USSD request. 
    
    `NB: This is not meant to be used manually.`
    """
    # parse the request body and pack the data into one object
    ussd_req_body = await parse_request_body(req_obj)
    
    # create the response string
    response: str = ""
    
    # handle the start of the session
    if ussd_req_body.text == USSDUserInputType.START_PROMPT.value:
        response = handle_session_start()
    # handle OTP generation
    elif ussd_req_body.text == USSDUserInputType.GET_OTP.value:
        response = await handle_otp_generation(db, ussd_req_body)
    # handle balance checking prompt
    elif ussd_req_body.text == USSDUserInputType.CHECK_BALANCE_PROMPT.value:
        response = handle_balance_checking_prompt()
    # handle balance checking logic
    elif ussd_req_body.text.startswith(USSDUserInputType.CHECK_BALANCE.value):
        response = await handle_balance_checking(db, ussd_req_body)
    # handle request callback
    elif ussd_req_body.text == USSDUserInputType.REQUEST_CALLBACK.value:
        response = await handle_request_callback(db, ussd_req_body, background_tasks)
    # handle invalid inputs
    else:
        response = handle_invalid_inputs()
    
    # return the response as plain text
    return PlainTextResponse(content=response)


async def parse_request_body(req_obj: Request) -> ussd_schemas.USSDRequestSchema:
    """Parse the body of a request object

    Args:
        req_obj (Request): The request object

    Returns:
        ussd_schemas.USSDRequestSchema: The USSD request object
    """
    # decode the request body from bytes to string
    req_body = (await req_obj.body()).decode()
    # parse the urlencoded body string into a dictionary
    body_dict = parse_qs(req_body)
    # unpack the data in the body into the USSD request object
    ussd_req_body = ussd_schemas.USSDRequestSchema(
        session_id=body_dict["sessionId"][0],
        service_code=body_dict["serviceCode"][0],
        phone_number=body_dict["phoneNumber"][0],
        text=("" if body_dict.get("text") is None else body_dict["text"][0]),
        network_code=body_dict["networkCode"][0],
    )
    return ussd_req_body


def handle_session_start() -> str:
    """Handle the session start request

    Returns:
        str: The final HTTP response string
    """
    # compose the message for the prompt
    response = "CON What do you want to do?\n"
    response += "1. Get OTP\n"
    response += "2. Check Balance\n"
    response += "3. Request for a callback\n"
    return response


async def handle_otp_generation(db: sqlite3.Connection, ussd_req_body: ussd_schemas.USSDRequestSchema) -> str:
    """Handle the OTP generation request

    Args:
        db (sqlite3.Connection): The database connection handle
        ussd_req_body (ussd_schemas.USSDRequestSchema): The USSD request object

    Returns:
        str: The final HTTP response string
    """
    # generate a 4-digit random number
    otp = "".join(random.choices(list("0123456789"), k=4))
    # initialize the response string
    response = ""
    try:
        # get the OTP using the phone number
        if await user_crud.UserQuery.add_otp_by_phone_number(db, ussd_req_body.phone_number, otp):
            response = f"END Your OTP is {otp}"
        else:
            # set the response when the phone number is not found in the database
            response = f"END Your phone number '{ussd_req_body.phone_number}' is not linked to any account"
    except Exception as e:
        # print the exception and return fatal error as response
        print(e)
        response = "END Fatal error occurred"
    return response


def handle_balance_checking_prompt() -> str:
    """Handle the balance checking prompt

    Returns:
        str: The final HTTP response string
    """
    return "CON Enter your Client ID"


async def handle_balance_checking(db: sqlite3.Connection, ussd_req_body: ussd_schemas.USSDRequestSchema) -> str:
    """Handle the balance checking

    Args:
        db (sqlite3.Connection): The database connection object
        ussd_req_body (ussd_schemas.USSDRequestSchema): The USSD request object

    Returns:
        str: The final HTTP response string
    """
    # initialize the response string
    response = ""
    try:
        # extract the client ID from the text which has the format `2*<client_id>`
        client_id = ussd_req_body.text[2:]
        # get and return the account balance in the response
        if user_record := await user_crud.UserQuery.get_user_by_client_id(db, client_id):
            if user_record.phone_number == ussd_req_body.phone_number:
                response = f"END Your balance is GHS {user_record.balance}"
            else:
                # set the response when the client ID is found but doesn't belong to the 
                # user requesting for it
                response = f"END Invalid ID '{client_id}'"
        else:
            # set the response when the client ID is not found in the database
            response = f"END Invalid ID '{client_id}'"
    except Exception as e:
        # print the exception and return fatal error as response
        print(e)
        response = "END Fatal error occurred" 
    return response


async def handle_request_callback(db: sqlite3.Connection, ussd_req_body: ussd_schemas.USSDRequestSchema, bg_tasks: BackgroundTasks) -> str:
    """Handle the request callback

    Args:
        db (sqlite3.Connection): The database connection object
        ussd_req_body (ussd_schemas.USSDRequestSchema): The USSD request object

    Returns:
        str: The final HTTP response string
    """
    # initialize the response string
    response = ""
    try:
        # save the USSD request to the callback logs table
        if callback_logs_record := await ussd_crud.CallbackLogsQuery.add_callback_log(db, ussd_req_body):
            # return fatal error when the operation fails
            if callback_logs_record is None:
                response = "END Fatal error occurred"
            else:
                # set the response that the user will get a callback
                response = "END You will receive an SMS notice"
                # send the SMS to the user as a background task
                sms_message = "The operation has completed successfully"
                bg_tasks.add_task(sms_utils.send_sms, phone_number=ussd_req_body.phone_number.replace("+", ""), message=sms_message)
    except Exception as e:
        # print the exception and return fatal error as response
        print(e)
        response = "END You will get a callback"
    return response


def handle_invalid_inputs() -> str:
    """Handle the invalid inputs

    Returns:
        str: The final HTTP response string
    """
    return "END Invalid Input"



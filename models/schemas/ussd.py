from pydantic import BaseModel, Field


class USSDRequestSchema(BaseModel):
    """This schema is used to receive USSD request data
    """
    session_id: str = Field(
        ...,
        title="Session ID",
        description="The unique ID for the session"
    )
    service_code: str = Field(
        ...,
        title="Service Code",
        description="The USSD code that is used to make the request"
    )
    phone_number: str = Field(
        ...,
        title="Phone Number",
        description="The user's phone number"
    )
    text: str = Field(
        ...,
        title="Text",
        description="The user's input"
    )
    network_code: str = Field(
        ...,
        title="Network Code",
        description="The network code"
    )

    class Config:
        schema_extra = {
            "example": {
                "sessionId": "string",
                "serviceCode": "string",
                "phoneNumber": "string",
                "text": "string",
                "networkCode": "string",
            }
        }


class CallbackLogSchema(USSDRequestSchema):
    """This is used to receive data loaded from the callback logs table
    """
    id: int = Field(
        ...,
        title="ID",
        description="An ID assigned to the user's database record"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "sessionId": "string",
                "serviceCode": "string",
                "phoneNumber": "string",
                "text": "string",
                "networkCode": "string",
            }
        }
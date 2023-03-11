from pydantic import BaseModel, Field
from models.schemas.shared import SuccessResponseBaseSchema


class UserBaseSchema(BaseModel):
    """This schema contains common fields shared by the remaining user schemas
    """
    name: str = Field(
        ...,
        title="Name",
        description="The user's name"
    )
    client_id: str = Field(
        ...,
        title="Client ID",
        description="The user's unique ID. Eg. National ID, Voters' ID, etc"
    )
    phone_number: str = Field(
        ...,
        title="Phone Number",
        description="The user's phone number"
    )
    balance: float = Field(
        default=0.0,
        title="Account Balance",
        description="The user's account balance"
    )

    class Config:
        schema_extra = {
            "example": {
                "name": "string",
                "client_id": "string",
                "phone_number": "string",
                "balance": 0.0,
            }
        }


class UserSchema(UserBaseSchema):
    """This schema is used for loading user records from the database"""
    id: int = Field(
        ...,
        title="ID",
        description="An ID assigned to the user's database record"
    )
    otp: str | None = Field(
        default=None,
        title="OTP",
        description="A One-Time Password"
    )

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "string",
                "client_id": "string",
                "phone_number": "string",
                "otp": "string",
                "balance": 0.0,
            }
        }


class CreateUserSchema(UserBaseSchema):
    """This schema is used to receive request data for add a new user
    """
    class Config:
        schema_extra = {
            "example": {
                "name": "string",
                "client_id": "string",
                "phone_number": "string",
                "balance": 0.0,
            }
        }


class SuccessResponseSchema(SuccessResponseBaseSchema):
    user: UserSchema

    class Config:
        schema_extra = {
            "example": {
                "message": "string",
                "user": {
                    "id": 1,
                    "name": "string",
                    "client_id": "string",
                    "phone_number": "string",
                    "otp": "string",
                    "balance": 0.0,
                }
            }
        }

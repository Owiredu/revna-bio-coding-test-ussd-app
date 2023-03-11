from pydantic import BaseModel, Field


class SuccessResponseBaseSchema(BaseModel):
    message: str = Field(
        ..., 
        title="Response Message", 
        description="The response message"
    )

    class Config:
        schema_extra = {
            "example": {
                "message": "string"
            }
        }
        
        
class ErrorResponseSchema(BaseModel):
    message: str = Field(
        ...,
        title="Message",
        description="The associated message"
    )

    class Config:
        schema_extra = {
            "example": {
                "detail": {
                    "message": "string"
                }
            },
        }
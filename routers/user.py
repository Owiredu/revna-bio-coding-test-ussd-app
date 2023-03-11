from fastapi import APIRouter, Depends, HTTPException, status
import sqlite3
from dependencies import get_db
from models.schemas import (
    user as user_schemas,
    shared as shared_schemas,
)
import asyncio
from models.crud import user as user_crud


router = APIRouter()


@router.post(
    path="",
    response_model=user_schemas.SuccessResponseSchema,
    responses={
        status.HTTP_409_CONFLICT: {
            "model": str,
            "description": "Conflict"
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": shared_schemas.ErrorResponseSchema,
            "description": "Bad request"
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": str,
            "description": "Internal server error"
        },
    }
)
async def add_user(
    req_data: user_schemas.CreateUserSchema,
    db: sqlite3.Connection = Depends(get_db)
):
    """Adds a user to the database.
    """
    # check for duplicate client ID or phone number
    try:
        check_result = await asyncio.gather(
            user_crud.UserQuery.get_user_by_client_id(db, req_data.client_id),
            user_crud.UserQuery.get_user_by_phone_number(
                db, req_data.phone_number)
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Internal server error"
            },
        )

    error_msg = ""
    if check_result[0] is not None:
        error_msg += (", " if error_msg != "" else "") + "Client ID"
    if check_result[1] is not None:
        error_msg += (", " if error_msg != "" else "") + "Phone Number"
    if error_msg != "":
        error_msg += " already exist(s)"

    if error_msg != "":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "Failed to add new user"
            },
        )

    try:
        # add the new user
        new_user: user_schemas.UserSchema | None = await user_crud.UserQuery.add_user(db, req_data)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Internal server error"
            },
        )

    # return an error response when the operation fails
    if new_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Failed to add new user"
            },
        )

    # return the new user's record
    return user_schemas.SuccessResponseSchema(
        message="User added successfully",
        user=new_user,
    )


@router.get(
    path="/cid/{client_id}",
    response_model=user_schemas.SuccessResponseSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": shared_schemas.ErrorResponseSchema,
            "description": "Not found"
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": str,
            "description": "Internal server error"
        },
    }
)
async def get_user_by_client_id(
    client_id: int,
    db: sqlite3.Connection = Depends(get_db)
):
    """Gets a user's record using the client ID.
    """
    try:
        # get the new user's record using the client ID
        user_data: user_schemas.UserSchema | None = await user_crud.UserQuery.get_user_by_client_id(db, client_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Internal server error"
            },
        )

    # return an error response when it is not found
    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": f"User with Client ID `{client_id}` not found"
            },
        )

    # return the user's record
    return user_schemas.SuccessResponseSchema(
        message="User retrieved successfully",
        user=user_data,
    )


@router.get(
    path="/phone/{phone_number}",
    response_model=user_schemas.SuccessResponseSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": shared_schemas.ErrorResponseSchema,
            "description": "Not found"
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": str,
            "description": "Internal server error"
        },
    }
)
async def get_user_by_phone_number(
    phone_number: str,
    db: sqlite3.Connection = Depends(get_db)
):
    """Gets a user's record using the phone number.
    """
    try:
        # get the new user's record using the phone number
        user_data: user_schemas.UserSchema | None = await user_crud.UserQuery.get_user_by_phone_number(db, phone_number)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Internal server error"
            },
        )

    # return an error response when it is not found
    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": f"User with Phone Number `{phone_number}` not found"
            },
        )

    # return the user's record
    return user_schemas.SuccessResponseSchema(
        message="User retrieved successfully",
        user=user_data,
    )


@router.delete(
    path="/{phone_number}",
    response_model=user_schemas.SuccessResponseBaseSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": shared_schemas.ErrorResponseSchema,
            "description": "Not found"
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": str,
            "description": "Internal server error"
        },
    }
)
async def delete_user_by_phone_number(
    phone_number: str,
    db: sqlite3.Connection = Depends(get_db)
):
    """Deletes a user's record using the Phone Number.
    """
    try:
        # delete the user's record using the phone number
        is_deleted: bool = await user_crud.UserQuery.delete_user_by_phone_number(db, phone_number)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Internal server error"
            },
        )

    # return an error response when it is not found
    if not is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": f"User with Phone Number `{phone_number}` not found"
            },
        )

    # return the user's record
    return user_schemas.SuccessResponseBaseSchema(
        message="User deleted successfully"
    )
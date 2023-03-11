import sqlite3
from models.schemas import user as user_schemas


class UserQuery:
    """
    Defines the CRUD operations for the User table
    """

    @staticmethod
    async def add_user(db: sqlite3.Connection, new_user: user_schemas.CreateUserSchema) -> user_schemas.UserSchema | None:
        """Add a new user to the database

        Args:
            db (sqlite3.Connection): The database connection handle
            new_user (user_schemas.CreateUserSchema): The new user data

        Returns:
            user_schemas.UserSchema: The new user's record
        """
        # save the user data
        cursor: sqlite3.Cursor = db.execute("INSERT INTO users(name, client_id, phone_number, otp, balance) VALUES(?,?,?,null,?)",
                                            (new_user.name, new_user.client_id, new_user.phone_number, new_user.balance))
        db.commit()

        # return None if the insertion fails
        if cursor.rowcount <= 0:
            return None

        # fetch and return the user data
        user_record: tuple = cursor.execute(
            "SELECT * FROM users WHERE phone_number = ?", (new_user.phone_number,)).fetchone()

        return user_schemas.UserSchema(
            id=user_record[0],
            name=user_record[1],
            client_id=user_record[2],
            phone_number=user_record[3],
            otp=user_record[4],
            balance=user_record[5],
        )

    @staticmethod
    async def get_user_by_phone_number(db: sqlite3.Connection, phone_number: str) -> user_schemas.UserSchema | None:
        """Get a single user record using the user's phone number

        Args:
            db (sqlite3.Connection): The database connection handle
            phone_number (str): The user's phone number

        Returns:
            user_schemas.UserSchema | None: The user's record
        """
        user_record = db.execute(
            "SELECT * FROM users WHERE phone_number = ?", (phone_number,)).fetchone()

        if user_record:
            return user_schemas.UserSchema(
                id=user_record[0],
                name=user_record[1],
                client_id=user_record[2],
                phone_number=user_record[3],
                otp=user_record[4],
                balance=user_record[5],
            )

        return None

    @staticmethod
    async def get_user_by_client_id(db: sqlite3.Connection, client_id: str) -> user_schemas.UserSchema | None:
        """Get a single user record using the client ID

        Args:
            db (sqlite3.Connection): The database connection handle
            client_id (str): The client ID

        Returns:
            user_schemas.UserSchema | None: The user's record
        """
        user_record = db.execute(
            "SELECT * FROM users WHERE client_id = ?", (client_id,)).fetchone()

        if user_record:
            return user_schemas.UserSchema(
                id=user_record[0],
                name=user_record[1],
                client_id=user_record[2],
                phone_number=user_record[3],
                otp=user_record[4],
                balance=user_record[5],
            )

        return None

    @staticmethod
    async def add_otp_by_phone_number(db: sqlite3.Connection, phone_number: str, otp: str) -> None:
        """Add a new OTP

        Args:
            db (sqlite3.Connection): The database connection handle
            id (int): The record ID of the user
            otp (str): The new OTP

        Returns:
            bool: True for success and False for failure
        """
        # save the OTP
        cursor: sqlite3.Cursor = db.execute(
            "UPDATE users SET otp = ? WHERE phone_number = ?", (otp, phone_number))
        db.commit()

        return cursor.rowcount >= 1
    
    @staticmethod
    async def delete_user_by_phone_number(db: sqlite3.Connection, phone_number: str) -> bool:
        """Delete a user's record using the phone number

        Args:
            db (sqlite3.Connection): The database connection handle
            phone_number (str): The user's phone number

        Returns:
            bool: True for success and False for failure
        """
        # delete the user
        cursor: sqlite3.Cursor = db.execute(
            "DELETE FROM users WHERE phone_number = ?", (phone_number,))
        db.commit()

        return cursor.rowcount >= 1

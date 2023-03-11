import sqlite3
from models.schemas import ussd as ussd_schemas


class CallbackLogsQuery:
    """
    Defines the CRUD operations for the Callback Logs table
    """

    @staticmethod
    async def add_callback_log(db: sqlite3.Connection, new_data: ussd_schemas.USSDRequestSchema) -> ussd_schemas.CallbackLogSchema | None:
        """Add a new callback log to the database

        Args:
            db (sqlite3.Connection): The database connection handle
            new_user (ussd_schemas.USSDRequestSchema): The new USSD request data to be logged

        Returns:
            ussd_schemas.CallbackLogSchema: The new callback log record
        """
        # save the callback log data
        cursor: sqlite3.Cursor = db.execute("INSERT INTO callback_logs(session_id, service_code, phone_number, text, network_code) VALUES(?,?,?,?,?)",
                                            (new_data.session_id, new_data.service_code, new_data.phone_number, new_data.text, new_data.network_code))
        db.commit()

        # return None if the insertion fails
        if cursor.rowcount <= 0:
            return None

        # fetch and return the callback log data
        callback_log_record: tuple = cursor.execute("SELECT * FROM callback_logs WHERE session_id = ? AND service_code = ? AND phone_number = ? AND text = ? AND network_code = ?",
                                                    (new_data.session_id, new_data.service_code, new_data.phone_number, new_data.text, new_data.network_code)).fetchone()

        return ussd_schemas.CallbackLogSchema(
            id=callback_log_record[0],
            session_id=callback_log_record[1],
            service_code=callback_log_record[2],
            phone_number=callback_log_record[3],
            text=callback_log_record[4],
            network_code=callback_log_record[5],
        )

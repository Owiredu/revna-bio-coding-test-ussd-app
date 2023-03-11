# A SIMPLE USSD APP
------

A simple USSD application built with [Python 3](https://www.python.org/), [FastAPI Web Framework](https://fastapi.tiangolo.com/) and [Africa’s Talking](https://africastalking.com/) for USSD and [mNotify](https://www.mnotify.com/) for callback SMS.

## HOW  TO RUN

------

1. Install [Python (Minimum version: 3.10)](https://www.python.org/).

2. Clone this repository with the command:

   ```bash
   git clone https://github.com/Owiredu/revna-bio-coding-test-ussd-app.git
   ```

3. Navigate to the root directory of the clone repository and run the command to create a virtual environment:

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment created on **Step 3** with follow command:

   - Bash

     ```bash
     source ./venv/Scripts/activate
     ```

   - PowerShell

     ```powershell
     & ./venv/Scripts/Activate.ps1
     ```

5. Install the required dependencies with the command:

   ```bash
   pip install -r requirements.txt
   ```

6. Run the application on `localhost` or `127.0.0.1` and port `3000` with the command:

   ```bash
   uvicorn main:app --reload --port 3000
   ```

## HOW TO USE DEPLOYED INSTANCE

------

1. Access the API documentation page hosted at [https://revna-bio-coding-test-ussd-app.onrender.com/docs](https://revna-bio-coding-test-ussd-app.onrender.com/docs). This provides basic utilities for managing users.
2. Add a user with a functional phone number. 
3. Create an account at https://account.africastalking.com/ and access the sandbox app.
4. Using a shared service code, create a channel and set the callback URL to https://revna-bio-coding-test-ussd-app.onrender.com/ussd
5. Provide the phone number specified for the user on **Step 2** to the simulator. Make sure to use the phone number format accepted by the simulator for the user as well.

*NB: If you have issues setting up the Africa's Talking sandbox for testing, refer to their tutorial at [Documentation | Africa's Talking (africastalking.com)](https://developers.africastalking.com/tutorials/building-an-offline-account-management-application-using-ussd)* 

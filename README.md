
# STOCKA: An Inventory Management Platform.

Stocka is an inventory management solution that is created for wholesalers and retailers, and its sole purpose is to help businesses keep tabs on their stock items while achieving their goal of making profits.

The system accepts inventory movement reports (transactions) and maintains a continuous record of the quantity on-hand.

Stocka will be made available on websites and mobile apps.


#### BACKEND API
- The API routes are hosted on [->](https://stocka-be.herokuapp.com/).

note - site was hosted on heroku's free plan which has since been cancelled

##### AUTHENTICATION API

- 
  - **Endpoint** ``GET`` `/auth/user/`
  - Get all users. Only the admin has access to this information.
  - It takes no parameter.


- 
  - **Endpoint** ``GET`` `/auth/user/{id}/`
  - Get user with specific id. Only the specific user and admin has access to this information.
  - **id**: string
    - The ID of the element. It is required.
    - example: 1 
    

- 
    - **Endpoint** ``POST`` `/auth/user/me/`
    - Returns an authenticated user.
      - **Body**: A `json` object.
      - This is required.
      - Example: 
        ```json
          {
            "token": "string"
          }
        ```


- 
  - **Endpoint** ``POST`` `/auth/user/register/`
  - This is the endpoint to register a user's account.
    - **required fields**: `email`, `first_name`, `last_name`, `phone_number`, `password`, `confirm_password`
    - **Body**: A `json` object.
    - Example:
      ```json
        {
            "email": "user@example.com",
            "first_name": "string",
            "last_name": "string",
            "phone_number": "string",
            "business_name": "string",
            "password": "string",
            "confirm_password": "string"
        }
      ```


- 
  - **Endpoint** ``POST`` `/auth/user/login/`
  - Login a user.
    - **fields**: 
      - ``email`` or ``phone_number``
      - ``password`` is required.
    - **Body**: A `json` object.
    - Example:
      ```json
        {
            "email or phone_number": "string",
            "password": "string"
        }
      ```


- 
  - **Endpoint** ``POST`` `/auth/user/logout/`
  - Logout a user. This deletes the token associated with the user.
    - **fields**: It takes no parameter.


- 
  - **Endpoint** ``POST`` `/auth/user/reset_password/`
  - Send an email containing the four-digit token needed to reset password.
    - **fields**: ``email`` is required.
    - **Body**: A `json` object.
    - Example:
      ```json
        {
          "email": "string"
        }
      ```


- 
  - **Endpoint** ``POST`` `/auth/user/password_reset_token/`
  - Endpoint for a user to input the four-digit token received via email.
    - **fields**: ``four_digit_token`` is required.
    - **Body**: A `json` object.
    - Example:
      ```json
        {
            "four_digit_token": "string"
        }
      ```


- 
  - **Endpoint** ``POST`` `/auth/user/reset_confirm/`
  - Reset a user's password.
    - **fields**: 
      - ``new_password`` is required.
      - ``confirm_password`` is required.
    - **Body**: A `json` object.
    - Example:
      ```json
        {
            "new_password": "string",
            "confirm_password": "string"
        }
      ```


- 
  - **Endpoint** ``POST`` `/auth/user/change_password/`
  - Change a user's password.
    - **fields**: 
      - ``old_password`` is required.
      - ``new_password`` is required.
    - **Body**: A `json` object.
    - Example:
      ```json
        {
            "new_password": "string",
            "old_password": "string"
        }
      ```


### HOW TO SET IT UP LOCALLY(On Windows)
PS: This step-by-step information is for the backend team

- Clone the repository
  - **https**
      ```shell
      git clone https://github.com/mrbazzan/stocka-be-pjt-109 stocka
      ```
  - **ssh**
      ```shell
      git clone git@github.com:mrbazzan/stocka-be-pjt-109 stocka
      ```

- Change directory
    ```shell script
    cd stocka
    ```

- Set up Virtual Environemnt and activate it
  - **Windows**
      ```shell
      python -m venv venv/
      cd venv/Scripts
      activate
      cd ../..
      ```
  - **Linux/MacOS**
      ```shell
      python -m venv venv/
      source venv/bin/activate
      ```

- Install the requirements
    ```shell
    pip install -r requirements.txt
    ```

The RDBMS is PostgreSQL. Create a database called `stocka` with `postgres` as the user/owner.
  - Save `POSTGRES_PASSWORD` and `EMAIL_PASSWORD` as environmental variable.
  - `POSTGRES_PASSWORD` is the password of the PostgreSQL database you're connecting to.
  - `EMAIL_PASSWORD` is the password for the email used to send activation URL.
      - **WINDOWS**
      ```shell
          set POSTGRES_PASSWORD='enter-the-password'
          set EMAIL_PASSWORD='enter-the-password'
      ```
      - **Linux/MacOS**
      ```shell
          export POSTGRES_PASSWORD='enter-the-password'
          export EMAIL_PASSWORD='enter-the-password'
      ```

- Then run;
    ```shell script
    python manage.py makemigrations
    python manage.py migrate
     
    python manage.py runserver
    ```

### Running Tests
- Activate virtual environment if it's not activated. Then run,
  ```python
  python manage.py test
  ```

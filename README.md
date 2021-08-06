
# Stocka inventory management solution

Stocka is an inventory management solution that is created for wholesalers and retailers, and it's sole purpose is to help these businesses keep tabs on their stock items, while achieving their goal of making profits.

The system accepts inventory movement reports (transactions) and maintains a continuous record of the quantity on-hand.

Stocka will be made available on websites and mobile apps. 


## FRONT-END PREVIEW
Link to Front end Live Preview: https://stocka-fe-pjt-109.vercel.app


## BACKEND API ROUTES
It's hosted on → [STOCKA-BE](https://stocka-be.herokuapp.com/).


- ### AUTHENTICATION API

``GET`` /auth/user/
- Get all Users. Only the Admin has access to this information.
#### PARAMETERS
- It takes no parameter.


``GET`` /auth/user/{id}/
- Get User with specific id. Only the Specific User and Admin has access to this information.
#### PARAMETERS
- id: string
- example: 1
The ID of the element. It is required.


``POST`` /auth/user/me/
- Returns an authenticated user.
#### PARAMETERS
- ``token`` is required.
- BODY:
    {
        "token": "string", 
    }


``POST`` /auth/user/register/
- This is the endpoint to register an account.
#### PARAMETERS
- ##### REQUIRED FIELDS: email, first_name, last_name, phone_number, password, confirm_password
- BODY:
    {
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "phone_number": "string",
        "business_name": "string",
        "password": "string",
        "confirm_password": "string"
    }


``POST`` /auth/user/login/
- Login a user.
#### PARAMETERS
- One of ``Email`` or ``Phone Number`` required.
- ``Password`` is required.
- BODY:
    {
        "email or phone_number": "string",
        "password": "string"
    }


``POST`` /auth/user/logout/
- Logout a user.
#### PARAMETERS
- It takes no parameter.


``POST`` /auth/user/reset_password/
- Send an email containing the four digit token needed to reset password
#### PARAMETERS
- ``Email`` is required.
- BODY:
    {
        "email": "string", 
    }


``POST`` /auth/user/password_reset_token/
- Endpoint for a user to input the four digit token received via email.
#### PARAMETERS
- ``four_digit_token`` is required.
- BODY:
    {
        "four_digit_token": "string", 
    }


``POST`` /auth/user/reset_confirm/
- Reset a user's password.
#### PARAMETERS
- ``new_password`` is required.
- ``confirm_password`` is required.
- BODY:
    {
        "new_password": "string",
        "confirm_password": "string"
    }


``POST`` /auth/user/change_password/
- Change a user's password.
#### PARAMETERS
- ``old_password`` is required.
- ``new_password`` is required.
- BODY:
    {
        "new_password": "string",
        "old_password": "string"
    }



## HOW TO SET IT UP LOCALLY(On Windows)
PS: This step-by-step information is for the backend team

- Clone the repository
```shell script
git clone https://github.com/zuri-training/stocka-be-pjt-109
```

- Change directory
```shell script
cd stocka-be-pjt-109
```

- Set up Virtual Environemnt and activate it
```shell script
python -m venv venv/
cd venv/Scripts
activate
cd ../..
```

- Install the requirements
```shell script
pip install -r requirements.txt
```

The RDBMS is PostgreSQL. Create a database called `stocka` with `postgres` as the user/owner.
- Save `POSTGRES_PASSWORD` and `EMAIL_PASSWORD` as environmental variable.
- `POSTGRES_PASSWORD` is the password of the PostgreSQL database you're connecting to.
- `EMAIL_PASSWORD` is the password for the email used to send activation URL. Ask for this password from the backend team lead.

```shell script
set POSTGRES_PASSWORD='enter-the-password'
set EMAIL_PASSWORD='enter-the-password'
```

- Then run;
```shell script
python manage.py makemigrations
python manage.py migrate
 
python manage.py runserver
```

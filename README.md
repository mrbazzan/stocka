
# Stocka inventory management solution

Stocka is an inventory management solution that is created for wholesalers and retailers, and it's sole purpose is to help these businesses keep tabs on their stock items, while achieving their goal of making profits.

The system accepts inventory movement reports (transactions) and maintains a continuous record of the quantity on-hand.

Stocka will be made available on websites and mobile apps. 


### HOW TO SET IT UP LOCALLY(On Windows)
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
- `EMAIL_PASSWORD` is the password for the email used for send activation URL. Ask for this password from the backend team.

```shell script
export POSTGRES_PASSWORD='enter-the-password'
export EMAIL_PASSWORD='enter-the-password'
```

- Then run;
```shell script
python manage.py runserver
```

### API ROUTES

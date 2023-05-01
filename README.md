### Fabio-Tests Cats

This is a simple single page webapp that renders Cat images. The Server is written in Python Flask and the Server is React in vanilla javascript. Both being simple with single goal to serve i.e show and store grid cards that has cat images to render both Flask and React app resides in a same file and not divided in modules to integrate and being helpful for better scaliability and maintanance.

It's connected to postgres which has a single Table to store the data. The data stored is in simple rows instead of using jsong object for each card data. Project is kept as much dependency free as possible. Migrations have not been added to get the initial records rather a curl is being provided below to set up the project locally and check the working.

## Tech Stack
Flask
React
Postgresql
sqlAlchemy

## Set up DB Server
```
db-compose up -d
docker exec -it test_postgres psql -U postgres -c “create database test”
```

## To run the complete App
Please run the curls to get the data in DB


## Structure
src/server  --backend
src/client/src  --frontend

## Backend
app.py to contain the App and all the routings
db.py containing the db connection and config
record.py containing the model for the table

## Frontend
App.js containing the maing logic for the page
/components/cards containing the Card component for each cat cards

## Config
Frontend: As for react it's engine will run everything from inside the client folder this it has .env.example file
```
cd client
cp .env.example .env
```

Backend: .env in the root folder of the app
```
cd .env.example .env
```

## Local development setup
```
source venv/bin/activate --- if you want to run in venv
yarn install-server
yarn install-client
cd ..
yarn start
```

## Improvements and Scopes
The different endpoints to add more card items, edit card details and delete cards are already created
The db could have been wrapped in document based db incase we try to implement multiple board showcases
Or it could have been in created with the cards as JSON objects and a cards table with the card details
Both FE and BE needs to be divided into proper modules.
Both FE and BE could have been wrapped with type checkings
DB Migrations should be used with Alembic or maybe flask-migrartions could be used
Unit tests can be added for Backend as there are multiple logics that would require testing and use based documentation
Pre commit hook can be added for type and lint checks and fixes

## Curl
To Have the Data setup and fetched from backend run the curl below
# 1
```
curl --location --request POST 'http://localhost:8080/create' \
--header 'Content-Type: application/json' \
--data-raw '{
    "type": "bank-draft",
    "title": "Bank Draft",
    "link": "https://placekitten.com/g/200/200"
}'
```
# 2
```
curl --location --request POST 'http://localhost:8080/create' \
--header 'Content-Type: application/json' \
--data-raw '{
    "type": "bill-of-lading",
    "title": "Bill of Lading",
    "link": "https://placekitten.com/g/201/201"
}'
```
# 3
```
curl --location --request POST 'http://localhost:8080/create' \
--header 'Content-Type: application/json' \
--data-raw '{
    "type": "invoice",
    "title": "Invoice",
    "link": "https://placekitten.com/g/202/202"
}'
```
# 4
```
curl --location --request POST 'http://localhost:8080/create' \
--header 'Content-Type: application/json' \
--data-raw '{
    "type": "bank-draft-2",
    "title": "Bank Draft 2",
    "link": "https://placekitten.com/g/203/203"
}'
```
# 5
```
curl --location --request POST 'http://localhost:8080/create' \
--header 'Content-Type: application/json' \
--data-raw '{
    "type": "bill-of-lading-2",
    "title": "Bill of Lading 2",
    "link": "https://placekitten.com/g/204/204"
}'
```


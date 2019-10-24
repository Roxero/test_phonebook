# phonebook
Test task by coding a django phonebook with rest-API

API calling:

=========
Get all the records from phonebook:

$ curl -X GET http://localhost:8000/api/entries/ -H 'Content-Type: application/json' | jq  
=========
Get one entry by it's ID

$ curl -X GET http://localhost:8000/api/entries/89/ -H 'Content-Type: application/json'  | jq
=========
Add a new entry with last_name and first_name

$ curl -X POST http://localhost:8000/api/entries/ -H 'Content-Type: application/json' -d '{"last_name": "Obama","first_name": "Barack"}' | jq
=========
Add a phone for user using it's ID

$ curl -X PUT http://localhost:8000/api/entries/99/ -H 'Content-Type: application/json' -d '{"phone":"+7-131-242-35-89"}' | jq
=========
Delete entry by it's ID

$ curl -X DELETE http://localhost:8000/api/entries/102/ -H 'Content-Type: application/json'  | jq

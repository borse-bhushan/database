from client.db import PyDBClient


db = PyDBClient()

db.connect()

db.create({"id": "001", "name": "hello"})
db.create([{"id": "001", "name": "hello"}], many=True)



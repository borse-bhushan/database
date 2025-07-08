# 🐍 py_db: A Simple Python-Based Lightweight Database Server

## 🚀 Overview

**py_db** is a custom-built, lightweight, file-based database server implemented in Python. It operates over a TCP socket using a custom protocol and supports standard operations like database creation, table management, and CRUD actions.

This project demonstrates how databases work under the hood—covering concepts like schema validation, persistent storage, authentication, concurrency, and query evaluation. It is ideal for learning, prototyping, or as a foundation for custom database solutions.

---

## ✨ Features

- ✅ Threaded TCP server for concurrent clients
- 🔐 Token-based authentication with custom user credentials
- 📁 Schema-based data validation via Marshmallow
- ⚙️ Dynamic schema class generation with unique constraints
- 📊 Structured operations: `CREATE`, `SELECT`, `UPDATE`, `DELETE`, `CREATE_TABLE`, `DROP_TABLE`
- 🧠 Query evaluation with operators: `$eq`, `$ne`, `$gt`, `$lt`, `$in`, etc.
- 📦 Flat-file storage engine using JSON lines
- 🔄 Partial schema validation on updates
- 🧪 Custom error codes and structured error responses
- 🔧 CLI environment-based configuration loading
- 📝 Configurable logging to file and console
- 🧩 Modular, extensible codebase

---

## 📂 Project Structure

```
.
├── run.py                     # Main server entrypoint
├── env.py                     # Loads JSON config from /config/env.json
├── arg_pars.py                # Command-line argument parser
├── requirment.txt             # Dependencies
├── data/                      # Flat-file database storage
│   └── py_db/                 # Example database (user.data, db_conf.json)
├── py_db/                     # Core database engine
│   ├── server.py              # Main TCP server
│   ├── con_mgt.py             # Per-connection handler
│   ├── action.py              # Request wrapper
│   ├── auth.py                # Token-based auth system
│   ├── db.py                  # Request router and executor
│   ├── response.py            # Standardized response format
│   ├── storage.py             # Schema & data file handler
│   ├── constants.py           # Enum definitions
│   ├── schema_gen.py          # Generates Marshmallow schemas dynamically
│   ├── singleton.py           # Thread-safe singleton metaclass
├── exc/                       # Custom exceptions and error definitions
│   ├── base.py                # Base exception class
│   ├── cmn_exc.py             # Common error types (e.g., auth, schema)
│   ├── schema.py              # Schema-specific validation errors
│   ├── codes.py               # Error codes
│   ├── err_msg.py             # Human-readable error messages
├── utils/                     # Utilities
│   ├── comm_fun.py            # Common helpers like `get_uuid`
│   └── log.py                 # Logging setup
├── schema/                    # Generated marshmallow schemas
│   └── py_db/                 # (auto-generated per-table schemas)
└── init_db.py                 # Used to preload initial database config
```

---

## 🧪 Usage

### 🔧 Step 1: Setup Environment

Create a config file at `config/env.json`:

```json
{
  "DATA_FOLDER": "data",
  "HOST": "127.0.0.1",
  "PORT": 9000
}
```

### ▶️ Step 2: Run the Server

```bash
python run.py --env config/env.json --load-initial-data
```
- `--env` or `-e`: Path to your environment config file.
- `--load-initial-data` or `-lid`: (Optional) Preloads initial database and tables as defined in `init_db.py`.

### 🧪 Step 3: Send Action Payloads

Payloads must be JSON strings sent over TCP.
**Sample `CREATE_TABLE` payload:**
```json
{
  "action": "CREATE_TABLE",
  "table": "user",
  "auth": { "token": "<your-token>" },
  "payload": {
    "name": { "type": "str", "required": true, "min_length": 3 },
    "age": { "type": "int", "required": true },
    "email": { "type": "str", "required": true, "unique": true }
  }
}
```

**Sample `INSERT` payload:**
```json
{
  "action": "CREATE",
  "table": "user",
  "auth": { "token": "<your-token>" },
  "payload": {
    "name": "Alice",
    "age": 25,
    "email": "alice@example.com"
  }
}
```

**Sample `SELECT` payload with query operators:**
```json
{
  "action": "SELECT",
  "table": "user",
  "auth": { "token": "<your-token>" },
  "payload": {
    "age": { "$gte": 18 }
  }
}
```

Use tools like netcat, Postman (with TCP plugin), or a Python socket client to test.

---

## 🔐 Authentication

Before performing any action, a `LOGIN` request must be sent:

```json
{
  "action": "LOGIN",
  "payload": {
    "user": "root",
    "password": "root@123",
    "database": "py_db"
  }
}
```

The response will include a token, which must be passed in the `auth` field of subsequent requests.

---

## 🧱 Schema & Storage

- Each database is a folder inside `/data/<db_name>`
- Tables are files: `table.data`
- Schemas are stored in `schema/<db_name>/<table>.py` and generated dynamically
- All data is stored line-by-line as JSON

---

## 🧩 Custom Protocol

The server expects a TCP message format like:

```
QUERY_LENGTH: <length>\r\n\r\n
<JSON Payload>
```

This ensures body-length safety and parsing integrity.

---

## ✅ Sample Query Operators Supported

- `$eq`, `$ne` — Equal / Not Equal
- `$gt`, `$gte`, `$lt`, `$lte` — Range Queries
- `$in`, `$nin` — List Inclusion
- Exact match (e.g., `{ "age": 30 }`) supported by default

---

## 🧠 Design Notes

- Marshmallow schemas are generated at runtime
- Singleton metaclass ensures only one instance of each system class
- Well-defined error handling using structured codes/messages
- Logging is configurable and handled via `utils/log.py`

---

## 👨‍💻 Author

- Bhushan Borse

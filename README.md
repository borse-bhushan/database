# 🐍 py_db: A Simple Python Database Server

## 🚀 Overview

**py_db** is a lightweight, threaded TCP database server written in Python. It supports basic database operations such as creating databases, authentication, and CRUD actions via a custom protocol. The server is designed for educational purposes and as a foundation for further development.

## ✨ Features

- ⚡ Threaded TCP server for concurrent client connections
- 📦 Custom protocol with header/body separation
- 🔐 Basic authentication and token management
- ⚙️ Configurable via JSON environment files
- 📝 Logging to console and file
- 🧩 Extensible action and response handling

## 🗂️ Project Structure

```sh
.
├── run.py                # Main entry point
├── env.py                # Environment and config loader
├── arg_pars.py           # Command-line argument parsing
├── py_db/                # Core database server logic
│   ├── server.py         # TCP server and runner
│   ├── con_mgt.py        # Connection handler
│   ├── db.py             # Main database logic
│   ├── storage.py        # Disk storage management
│   ├── auth.py           # Authentication/token logic
│   └── ...               # Other modules
├── exc/                  # Custom exceptions and error codes
├── utils/                # Utilities (logging, messages, etc.)
├── data/                 # Data storage (created at runtime)
│   └── py_db/
│       └── db_conf.json  # Example database config
├── logs/                 # Log files
└── README.md             # This file
```

## 🏁 Getting Started

### 📋 Prerequisites

- Python 3.8+
- No external dependencies required

### ⚙️ Configuration

Edit [`utils/env.json`](utils/env.json) to set server host, port, database users, and logging options.

### ▶️ Running the Server

```sh
python run.py
```

#### Optional Arguments

- `-e`, `--e-file`: Path to a custom environment JSON file
- `-lid`, `--load-initial-data`: Load initial data into the database

Example:

```sh
python run.py --e-file custom_env.json --load-initial-data
```

## 📡 Protocol

Clients communicate with the server using a custom protocol:

- Header: `QUERY_LENGTH: <length>\r\n\r\n`
- Body: JSON-encoded action data

Example request:

```proto
QUERY_LENGTH: 42\r\n\r\n{"action": "PING", "auth": {}}
```

## 📑 Logging

Logs are written to both console and [`logs/py_db.log`](logs/py_db.log) by default. Configure logging in [`utils/env.json`](utils/env.json).

## 📄 License

This project is licensed under the [Apache License 2.0](LICENSE).

---

**🚧 Work in progress.** Contributions and feedback are welcome! 🙌

## 👨‍💻 Author

- 🧑‍💻 Bhushan Borse

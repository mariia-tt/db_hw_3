# HW-3: Database system development
## Run the project:

In this project uses PyQt6 for the GUI and SQLClient (via pyodbc) for database connectivity.

### 1. Preparation:

Download "Python" from https://www.python.org/downloads/

### 2. Clone the Repository

```lang
git clone https://github.com/mariia-tt/db_hw_3.git
cd db_hw_3.git
```

Create and activate a virtual environment:

```lang
python -m venv venv
source venv/bin/activate   #macOS/Linux
venv\\Scripts\\activate   #Windows
```

Install PyQt6 and sqlclient package for Python:

```lang
pip install PyQt6 pyodbc

pip install mysqlclient
```

### 3. Run the Application

```lang
    python main.py
```

The main window should appear, connecting to your configured database.

### 4. Verify

You can perform basic operations (like: "all CRUD permissions" ...) to verify database connectivity.

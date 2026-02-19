# sqlens

A command-line tool for querying CSV, JSON, and Excel files using SQL.

## Requirements

- Python 3
- pandas
- fire
- tabulate
- openpyxl (for Excel files)

Install dependencies:

```bash
pip3 install pandas fire tabulate openpyxl
```

## Usage

### Load a file

Load a file into the database. The table name defaults to the filename (without extension).

```bash
python3 run.py load --path file.csv
python3 run.py load --path file.json
python3 run.py load --path file.xlsx
```

Load with a custom table name:

```bash
python3 run.py load --path file.csv --name mytable
```

Load a specific sheet from an Excel file (0-indexed):

```bash
python3 run.py load --path file.xlsx --sheet 1
```

### Query

Run any SQL statement against loaded tables:

```bash
python3 run.py query "SELECT * FROM mytable LIMIT 10"
python3 run.py query "SELECT column, COUNT(*) FROM mytable GROUP BY column"
```

Export results to a file:

```bash
python3 run.py query "SELECT * FROM mytable" --output results.csv
python3 run.py query "SELECT * FROM mytable" --output results.json
python3 run.py query "SELECT * FROM mytable" --output results.xlsx
```

### List tables

Show all loaded tables with their row count and columns:

```bash
python3 run.py tables
```

### Drop a table

Remove a table from the database:

```bash
python3 run.py drop mytable
```

### Reset

Wipe the entire database:

```bash
python3 run.py reset
```

## Notes

- Data is persisted to `copydata.db` (SQLite), so you can load once and query multiple times.
- Table names are sanitized — spaces and hyphens become underscores, the file extension is stripped.
- Query output is capped at 50 rows by default when printed to the terminal.

# pymongo-the-sql
A sql wrapper made to mimic the pymongo syntax in order to simplify sql syntax.

## Docs

### Usage

    from pymongo_the_sql.pymongo_the_sql import PyMongoTheSql
    PyMongoTheSql("../tests/test.sqlite3")
    <pymongo_the_sql.pymongo_the_sql.PyMongoTheSql object at 0x7f60878e8e80>
    client = PyMongoTheSql("../tests/test.sqlite3")
    client = PyMongoTheSql("../tests")
    db = client.get_database("test")
    db["users"]
    <pymongo_the_sql.pymongo_the_sql.PyMongoTheSql object at 0x7f6087763400>
    users = db["users"]
    users.find({"id": "1"})

### Api

#### Update

Updates values for all specified columns where the conditions are True.
    update(columns_values: dict, conditions: dict[Optional], operator: str[Optional]) -> bool

Updates values for all specified columns where the conditions are True. Use the values tuple to update Blob type objects.
    update_blob(columns_values: dict, values: tuple[Optional], conditions: dict[Optional], operator: str[Optional])

Updates values for all specifed columns on the first row where the conditions are True.
    update_one(columns_values: dict, conditions: dict[Optional])

Updates values for all specified columns on every row.
    update_all(columns_values: dict[Optional]) -> bool

#### Find

Returns the specified columns on all rows the conditions are True.
    find(conditions: dict, columns: dict, operator: str) -> dict

Returns the specified columns on the first row the conditions are True.
    find_one(conditions: dict, columns: list, operator: str) -> dict

Returns the whole table.
    find_all() -> dict

Returns the specified columns on the last row the conditions are True.
    find_last(conditions: dict[Optional], columns: list[Optional], operator: str[Optional]) -> dict

Returns how many rows in the table.
    find_all_and_count() -> int

Returns how many rows the conditions are True.
    find_and_count(conditions: dict[Optional], columns: list[Optional], operator: str[Optional]) -> int

#### Insert

Inserts the values in the specified columns.
    insert(columns_values: dict) -> bool
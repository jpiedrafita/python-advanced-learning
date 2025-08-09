from dataclasses import dataclass

import psycopg2
import psycopg2.extras


# Dataclass to represent an investment
@dataclass
class Investment:
    id: int
    coin: str
    currency: str
    amount: float


# Connect to the PostgreSQL database
connection = psycopg2.connect(
    host="localhost", database="manager", user="postgres", password="PGpassword"
)

# Get the cursor from the connection to interact with the database
cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

# SQL query to create the investment table
create_investment_table = """
create table investment (
    id serial primary key,
    coin varchar(32),
    currency varchar(3),
    amount real
)
"""

# Add one row to the investment table
add_bitcoin_investment = """
insert into investment (
    coin, currency, amount
) values (
    'bitcoin', 'USD', 1.0
);
"""

# Parameterized SQL query to add multiple rows to the investment table
add_investment_template = """
insert into investment (
    coin, currency, amount
) values %s;
"""

# SQL query to select all investments in Bitcoin
select_bitcoin_investment = "SELECT * FROM investment WHERE coin='bitcoin';"
# SQL query to select all investments
select_all_investments = "SELECT * FROM investment;"

# # We pass the values in al list of tuples
# data = [
#     ("bitcoin", "GBP", 10.0),
#     ("dogecoin", "EUR", 100.0),
# ]

# # Execute the SQL query to create the investment table
# cursor.execute(create_investment_table)

# # Execute the SQL query to add a row to the investment table
# cursor.execute(add_bitcoin_investment)

# # Execute the SQL query with the cursor, template, and values to create the investment table
# psycopg2.extras.execute_values(cursor, add_investment_template, data)

# # Execute the SQL query to retrieve all Bitcoin investments
# cursor.execute(select_bitcoin_investment)
# data = cursor.fetchone()
# print(data)

# Execute the SQL query to retrieve all investments
cursor.execute(select_all_investments)
# # Initialize dictionaries from the tuples in each RealDictCursor
# data = [dict(row) for row in cursor.fetchall()]
# Initialize Investment dataclass instances from the dictionaries by passing them as keyword arguments
data = [Investment(**dict(row)) for row in cursor.fetchall()]
print(data)
for investment in data:
    print(
        f"Investment ID: {investment.id}, Coin: {investment.coin}, "
        f"Currency: {investment.currency}, Amount: {investment.amount}"
    )


# Commit the changes to the database
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()

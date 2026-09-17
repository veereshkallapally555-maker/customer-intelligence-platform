from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///data/db/customer_intelligence.db")

with open("sql/01_basic_analysis.sql", "r") as file:
    query = file.read()

with engine.connect() as connection:
    result = connection.execute(text(query))

    for row in result:
        print(row)
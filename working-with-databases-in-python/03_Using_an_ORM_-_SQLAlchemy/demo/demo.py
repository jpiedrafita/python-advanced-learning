from sqlalchemy import String, Numeric, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


# Base class for SQLAlchemy ORM models
class Base(DeclarativeBase):
    pass


# Investment class representing the investments table in the database
class Investment(Base):
    __tablename__ = "investments"

    id: Mapped[int] = mapped_column(primary_key=True)
    coin: Mapped[str] = mapped_column(String(32))
    currency: Mapped[str] = mapped_column(String(3))
    amount: Mapped[float] = mapped_column(Numeric(5, 2))

    # String representation of the Investment object
    def __repr__(self):
        return f"<Investment(coin: {self.coin}, currency: {self.currency}, amount: {self.amount})>"


# Create the SQLite database and investments table. Classses inheriting from Base will be created as tables.
engine = create_engine("sqlite:///demo.db")
Base.metadata.create_all(engine)

# Create some example investments
bitcoin = Investment(coin="bitcoin", currency="USD", amount=1.00)
ethereum = Investment(coin="ethereum", currency="GBP", amount=10.00)
dogecoin = Investment(coin="dogecoin", currency="USD", amount=100.00)

with Session(engine) as session:
    # # Add the investments to the session, one or more at a time
    # session.add(bitcoin)
    # session.add_all([ethereum, dogecoin])
    # # Commit the session to save the investments to the database
    # session.commit()

    # Query the investments table
    # stmt = select(Investment).where(Investment.coin == "bitcoin")
    # stmt = select(Investment).where(Investment.coin == "foocoin")
    # stmt = select(Investment)  # .where(Investment.coin == "foocoin")

    # # print(stmt)
    # investment = session.execute(stmt).scalar_one()
    # # Uses the __repr__ method to print the investment object
    # print(investment)

    # # Get row by primary key value
    # investment = session.get(Investment, 20)
    # print(investment)

    # # Retrieve multiple rows
    # stmt = select(Investment).where(Investment.amount > 200)
    # investments = session.execute(stmt).scalars().all()
    # print(investments)
    # for investment in investments:
    #     print(investment)

    bitcoin = session.get(Investment, 1)
    bitcoin.amount = 1.234
    print(session.dirty)  # Check which objects are modified
    session.commit()

    print(bitcoin)

    # Delete an investment
    dogecoin = session.get(Investment, 3)
    session.delete(dogecoin)
    print(session.deleted)  # Check which objects are marked for deletion
    session.commit()

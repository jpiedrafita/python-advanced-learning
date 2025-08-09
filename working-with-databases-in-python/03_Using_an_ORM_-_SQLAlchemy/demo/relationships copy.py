from sqlalchemy import String, Numeric, Text, create_engine, select, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship


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

    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolio.id"))
    portfolio: Mapped["Portfolio"] = relationship(back_populates="investments")

    # String representation of the Investment object
    def __repr__(self):
        return f"<Investment(coin: {self.coin}, currency: {self.currency}, amount: {self.amount})>"


class Portfolio(Base):
    __tablename__ = "portfolio"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    description: Mapped[str] = mapped_column(Text())

    investments: Mapped[list[Investment]] = relationship(back_populates="portfolio")

    def __repr__(self):
        return f"<Portfolio name: {self.name}, description: {self.description}) with {len(self.investments)} investments>"


engine = create_engine("sqlite:///demo_r.db")
Base.metadata.create_all(engine)

# Create some example investments and portfolios
bitcoin = Investment(coin="bitcoin", currency="USD", amount=1.00)
ethereum = Investment(coin="ethereum", currency="GBP", amount=10.00)
dogecoin = Investment(coin="dogecoin", currency="USD", amount=100.00)

portfolio_1 = Portfolio(name="Portfolio 1", description="Description 1")
portfolio_2 = Portfolio(name="Portfolio 2", description="Description 2")

bitcoin.portfolio = portfolio_1

portfolio_2.investments.extend([ethereum, dogecoin])

portfolio_3 = Portfolio(name="Portfolio 3", description="Description 3")
bitcoin_2 = Investment(coin="bitcoin", currency="USD", amount=2.0)
bitcoin_2.portfolio = portfolio_3

with Session(engine) as session:
    # # session.add(bitcoin)
    # session.add(portfolio_2)
    # session.commit()

    # Get investments from a portfolio
    portfolio = session.get(Portfolio, 2)

    for investment in portfolio.investments:
        print(investment)

    print(portfolio)

    # Get investments from a portfolio using the relationship
    investment = session.get(Investment, 1)
    print(investment.portfolio)

    # Join
    stmt = select(Investment).join(Portfolio)
    print(stmt)

    # session.add(bitcoin_2)
    # session.commit()

    # Subquery to select portfolios with bitcoin investments
    subq = select(Investment).where(Investment.coin == "bitcoin").subquery()
    stmt = select(Portfolio).join(subq, Portfolio.id == subq.c.portfolio_id)
    print(stmt)

    portfolios = session.execute(stmt).scalars().all()
    print(portfolios)

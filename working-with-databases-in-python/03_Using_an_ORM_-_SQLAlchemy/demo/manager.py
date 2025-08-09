import click
import requests

from sqlalchemy import String, Numeric, Text, create_engine, select, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship


# Get multiple coin prices from CoinGecko API (We can hit API limit if too many coins are requested at once)
def get_coin_prices(coins, currencies):
    coin_csv = ",".join(coins)
    currency_csv = ",".join(currencies)

    COINGECKO_URL = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_csv}&vs_currencies={currency_csv}"

    data = requests.get(COINGECKO_URL).json()

    return data


class Base(DeclarativeBase):
    pass


class Portfolio(Base):
    __tablename__ = "portfolio"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    description: Mapped[str] = mapped_column(Text())

    investments: Mapped[list["Investment"]] = relationship(back_populates="portfolio")

    def __repr__(self):
        return f"<Portfolio name: {self.name}, description: {self.description}) with {len(self.investments)} investments>"


class Investment(Base):
    __tablename__ = "investments"

    id: Mapped[int] = mapped_column(primary_key=True)
    coin: Mapped[str] = mapped_column(String(32))
    currency: Mapped[str] = mapped_column(String(3))
    amount: Mapped[float] = mapped_column(Numeric(5, 2))

    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolio.id"))
    portfolio: Mapped["Portfolio"] = relationship(back_populates="investments")

    def __repr__(self):
        return f"<Investment(coin: {self.coin}, currency: {self.currency}, amount: {self.amount})>"


# engine = create_engine("sqlite:///manager.db")
engine = create_engine("postgresql://postgres:PGpassword@localhost:5432/manager")
Base.metadata.create_all(engine)


@click.group()
def cli():
    pass


@click.command(help="View the investments in a portfolio")
def view_portfolio():
    # Get a list of all portfolios
    with Session(engine) as session:
        stmt = select(Portfolio)
        all_portfolios = session.execute(stmt).scalars().all()

        # Display to choose a portfolio
        for index, portfolio in enumerate(all_portfolios):
            print(f"{index + 1}: {portfolio.name}")

        # Get the portfolio and its investments
        portfolio_index = int(input("Select a portfolio: ")) - 1
        portfolio = all_portfolios[portfolio_index]
        investments = portfolio.investments

        # Get coins and currencies from investments
        coins = set([investment.coin for investment in investments])
        currencies = set(investment.currency for investment in investments)

        # Get prices for the coins
        coin_prices = get_coin_prices(coins, currencies)
        print(f"Investments in {portfolio.name}")
        for index, invesment in enumerate(investments):
            coin_price = coin_prices[invesment.coin][invesment.currency.lower()]
            total_price = float(invesment.amount) * coin_price
            print(
                f"{index + 1}: {invesment.coin} {total_price:.2f} {invesment.currency}"
            )


@click.command(help="Add a new investment and add it to a portfolio")
@click.option("--coin", prompt=True)
@click.option("--currency", prompt=True)
@click.option("--amount", prompt=True, type=float)
def add_investment(coin, currency, amount):
    with Session(engine) as session:
        # Get all portfolios
        stmt = select(Portfolio)
        all_portfolios = session.execute(stmt).scalars().all()

        # Print a list of portfolios along with an index for the user to choose from
        for index, portfolio in enumerate(all_portfolios):
            print(f"{index + 1}: {portfolio.name}")

        # Get that index from the user to choose a portfolio
        portfolio_index = int(input("Select a portfolio: ")) - 1
        portfolio = all_portfolios[portfolio_index]

        # Crete the investment
        investment = Investment(coin=coin, currency=currency, amount=amount)
        portfolio.investments.append(investment)

        # Persist the investment
        session.add(portfolio)
        session.commit()

        print(f"Adeed new {coin} investment to portfolio '{portfolio.name}'")


@click.command(help="Create a new portfolio")
@click.option("--name", prompt=True)
@click.option("--description", prompt=True)
def add_portfolio(name, description):
    portfolio = Portfolio(name=name, description=description)
    with Session(engine) as session:
        session.add(portfolio)
        session.commit()
    print(f"Added Portfolio '{name}'!")


@click.command(help="Drop all tables in the database")
def clear_database():
    Base.metadata.drop_all(engine)
    print("Database cleared!")


cli.add_command(clear_database)
cli.add_command(add_portfolio)
cli.add_command(add_investment)
cli.add_command(view_portfolio)


if __name__ == "__main__":
    cli()

import click
from tqdm import tqdm

from .parser import parse_lua_file, flatten_auctions
from .models import Auction, get_session
from .enrich import enrich_items


@click.group()
def cli():
    """Auction analyser command line interface."""
    pass


@cli.command()
@click.option('--input', '-i', 'input_path', type=click.Path(exists=True), required=True)
@click.option('--db', default='auction.db', help='Path to SQLite database')
def ingest(input_path: str, db: str):
    """Ingest a Lua SavedVariables file into the database."""
    session = get_session(db)
    data = parse_lua_file(input_path)
    batch = []
    for row in tqdm(flatten_auctions(data)):
        batch.append(Auction(**row))
        if len(batch) >= 1000:
            session.bulk_save_objects(batch)
            session.commit()
            batch.clear()
    if batch:
        session.bulk_save_objects(batch)
        session.commit()


@cli.command()
@click.option('--db', default='auction.db')
def enrich(db: str):
    """Fetch item metadata and store it in the database."""
    session = get_session(db)
    enrich_items(session)


@cli.command('find-flips')
@click.option('--db', default='auction.db')
@click.option('--min-profit', default=0, type=float)
def find_flips(db: str, min_profit: float):
    """Placeholder flip finder implementation."""
    session = get_session(db)
    click.echo('Flip finding logic not yet implemented.')


if __name__ == '__main__':
    cli()

# Auction Analyser

This project parses WoW SavedVariables Lua files and stores auction data in SQLite. It provides a CLI for ingesting, enriching and analysing data.

## Installation

```bash
pip install -e .
```

## Usage

### Ingest

```bash
auction-analyser ingest --input path/to/MyAddon_auctionHistory.lua --db auctions.db
```

### Enrich

```bash
auction-analyser enrich --db auctions.db
```

### Find Flips

```bash
auction-analyser find-flips --db auctions.db --min-profit 100
```

## Project Structure

- `auction_analyser/parser.py` – Lua parsing utilities
- `auction_analyser/models.py` – SQLAlchemy models and DB helpers
- `auction_analyser/enrich.py` – Item metadata enrichment
- `auction_analyser/cli.py` – Command line interface
- `tests/` – basic tests


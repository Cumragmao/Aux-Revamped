import re
from typing import Dict, Iterable, Any

from slpp import slpp as lua


def parse_lua_file(path: str) -> Dict[str, Any]:
    """Parse a Lua table dump file into a Python dictionary."""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Strip variable assignment or 'return'
    content = re.sub(r'^.*?=\s*', '', content, count=1).strip()
    if content.startswith('return'):
        content = content[len('return'):].strip()
    content = content.rstrip(';')
    data = lua.decode(content)
    return data


def flatten_auctions(data: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    """Yield flattened auction rows from parsed data."""
    for scan_id, auctions in data.items():
        try:
            scan_id_int = int(scan_id)
        except ValueError:
            continue
        for entry in auctions:
            row = {
                'scan_id': scan_id_int,
                'item_id': entry.get('item_id'),
                'stack_size': entry.get('stack_size'),
                'bid_price': entry.get('bid_price'),
                'buyout_price': entry.get('buyout_price'),
                'seller': entry.get('seller'),
                'time_left': entry.get('time_left'),
                'timestamp': entry.get('timestamp'),
            }
            yield row

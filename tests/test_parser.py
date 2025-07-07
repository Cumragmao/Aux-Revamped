from auction_analyser.parser import parse_lua_file, flatten_auctions

def test_parse_lua_file(tmp_path):
    lua_content = 'data = { [1] = { { ["item_id"] = 1, ["stack_size"] = 2, ["bid_price"] = 10, ["buyout_price"] = 20, ["seller"] = "foo", ["time_left"] = 1, ["timestamp"] = 123 } } }'
    path = tmp_path / 'data.lua'
    path.write_text(lua_content)
    data = parse_lua_file(str(path))
    rows = list(flatten_auctions(data))
    assert rows
    assert rows[0]['item_id'] == 1

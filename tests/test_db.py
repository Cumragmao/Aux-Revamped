from auction_analyser.models import get_session, Auction


def test_db_insert(tmp_path):
    db_path = tmp_path / 'test.db'
    session = get_session(str(db_path))
    auction = Auction(scan_id=1, item_id=2, stack_size=1, bid_price=10,
                      buyout_price=20, seller='a', time_left=1, timestamp=123)
    session.add(auction)
    session.commit()
    assert session.query(Auction).count() == 1

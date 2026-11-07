from etl.quality import CHECKS


def test_check_names_unique():
    names = [c[0] for c in CHECKS]
    assert len(names) == len(set(names))


def test_range_check_logic():
    rules = {name: rule for name, _, rule in CHECKS}
    assert rules["pm25_in_range"](0)
    assert not rules["pm25_in_range"](3)
    assert not rules["data_freshness_hours"](12)

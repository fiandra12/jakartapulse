from etl.extract import parse_hourly


def test_parse_hourly_maps_values():
    payload = {
        "hourly": {
            "time": ["2026-01-01T00:00", "2026-01-01T01:00"],
            "pm10": [20.0, 25.0],
            "pm2_5": [10.0, None],
        }
    }
    rows = parse_hourly("Jakarta Pusat", payload, ["pm10", "pm2_5"])
    assert len(rows) == 2
    assert rows[0]["location"] == "Jakarta Pusat"
    assert rows[0]["pm2_5"] == 10.0
    assert rows[1]["pm2_5"] is None

import pytest
import csv
import os
from utils import filter_data, aggregate_data, parse_cond


@pytest.fixture
def sample_data() -> list:
    return [
        {'name': 'A', 'price': '100', 'rating': '4.5'},
        {'name': 'B', 'price': '200', 'rating': '4.0'},
        {'name': 'C', 'price': '300', 'rating': '3.5'}
    ]


def test_parse_condition():
    assert parse_cond("price>100", {'>': None}) == ('price', '>', '100')
    with pytest.raises(ValueError):
        parse_cond("price100", {'>': None})


def test_filter_data_string(sample_data):
    filtered = filter_data(sample_data, "name=B")
    assert len(filtered) == 1
    assert filtered[0]['name'] == 'B'


def test_filter_data_numeric(sample_data):
    filtered = filter_data(sample_data, "price>150")
    assert len(filtered) == 2
    assert filtered[0]['price'] == '200'


def test_aggregate_avg(sample_data):
    assert aggregate_data(sample_data, "price=avg") == 200.0


def test_aggregate_min(sample_data):
    assert aggregate_data(sample_data, "rating=min") == 3.5


def test_aggregate_max(sample_data):
    assert aggregate_data(sample_data, "rating=max") == 4.5


def test_aggregate_invalid_column(sample_data):
    with pytest.raises(ValueError):
        aggregate_data(sample_data, "invalid=avg")


def test_aggregate_non_numeric(sample_data):
    with pytest.raises(ValueError):
        aggregate_data(sample_data, "name=avg")


def test_integration(tmp_path):
    csv_data = "name,price\nA,100\nB,200\nC,300"
    file_path = tmp_path / "test.csv"
    file_path.write_text(csv_data)

    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)

    filtered = filter_data(data, "price>150")
    assert len(filtered) == 2

    avg_price = aggregate_data(filtered, "price=avg")
    assert avg_price == 250.0
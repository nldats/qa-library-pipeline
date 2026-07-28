"""Tests for ingestion.py.

TODO: Implement these tests for load_csv, load_json, and load_excel in
src/data_processing/ingestion.py.
"""

from unittest.mock import patch

import pandas as pd
import pytest

from data_processing.ingestion import load_csv, load_excel, load_json


def test_load_csv_file_not_found(tmp_path):
    fake_path = tmp_path / "nonexistent.csv"
    with pytest.raises(FileNotFoundError):
        load_csv(fake_path)


def test_load_csv_invalid_format(tmp_path):
    bad_file = tmp_path / "bad.csv"
    bad_file.write_text("not,a,valid,csv\n1,2,3")

    df = load_csv(bad_file)

    # Pandas loads ragged CSVs and fills missing values with NaN
    assert isinstance(df, pd.DataFrame)
    assert df.isna().sum().sum() > 0


def test_load_json_invalid_json(tmp_path):
    bad_json = tmp_path / "bad.json"
    bad_json.write_text("{invalid json}")

    with pytest.raises(ValueError):
        load_json(bad_json)


def test_load_json_file_not_found(tmp_path):
    fake_path = tmp_path / "missing.json"
    with pytest.raises(FileNotFoundError):
        load_json(fake_path)


def test_load_excel_file_not_found(tmp_path):
    fake_path = tmp_path / "missing.xlsx"
    with pytest.raises(FileNotFoundError):
        load_excel(fake_path)


def test_load_excel_invalid_content(tmp_path):
    bad_excel = tmp_path / "bad.xlsx"
    bad_excel.write_text("not an excel file")

    # Excel readers raise a variety of exceptions depending on engine
    with pytest.raises(Exception):
        load_excel(bad_excel)

def test_load_csv_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_csv("missing.csv")


def test_load_csv_empty_file(tmp_path):
    file = tmp_path / "empty.csv"
    file.write_text("")

    with pytest.raises(pd.errors.EmptyDataError):
        load_csv(file)

def test_load_csv_reraises_unexpected_exception(tmp_path):
    file = tmp_path / "data.csv"
    file.write_text("a,b\n1,2\n")

    with patch("pandas.read_csv", side_effect=ValueError("Bad data")):
        with pytest.raises(ValueError):
            load_csv(file)

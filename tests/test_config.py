import pytest
from src.config import params
from src.exceptions import WrongParamValue
from src.consts import CHECK_INTERVAL
import sys

def test_params_valid_timeout(monkeypatch):
    for timeout in [10, 50, 200, 600, 3000, 4568]:
        monkeypatch.setattr(sys, 'argv', ['program', '--timeout', str(timeout)])
        result = params()
        assert result == timeout

def test_params_invalid_argument(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['program', '--invalid_arg', '10'])
    with pytest.raises(SystemExit):
        params()


def test_params_no_argument(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['program'])
    with pytest.raises(SystemExit):
        params()

def test_params_negative_timeout(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['program', '--timeout', '-5'])
    with pytest.raises(WrongParamValue):
        params()

def test_params_zero_timeout(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['program', '--timeout', '0'])
    with pytest.raises(WrongParamValue):
        params()
import pytest
from src.setup import params
from src.exceptions import WrongParamValue
import sys


@pytest.mark.test_setup
class TestParams:
    def test_params_valid_timeout(self, monkeypatch):
        for timeout in [10, 50, 200, 600, 3000, 4568]:
            monkeypatch.setattr(
                sys, 'argv', ['program', '--timeout', str(timeout)]
            )
            result = params()
            assert result == timeout

    def test_params_invalid_argument(self, monkeypatch):
        monkeypatch.setattr(sys, 'argv', ['program', '--invalid_arg', '10'])
        with pytest.raises(SystemExit):
            params()

    def test_params_no_argument(self, monkeypatch):
        monkeypatch.setattr(sys, 'argv', ['program'])
        with pytest.raises(SystemExit):
            params()

    def test_params_negative_timeout(self, monkeypatch):
        monkeypatch.setattr(sys, 'argv', ['program', '--timeout', '-5'])
        with pytest.raises(WrongParamValue):
            params()

    def test_params_zero_timeout(self, monkeypatch):
        monkeypatch.setattr(sys, 'argv', ['program', '--timeout', '0'])
        with pytest.raises(WrongParamValue):
            params()

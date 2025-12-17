"""Tests for parameters module."""

import pytest

from traffic_fines.utils.parameters import Parameters, DEFAULT_PARAMS


class TestParameters:
    """Tests for Parameters dataclass."""

    def test_default_params_exist(self):
        """DEFAULT_PARAMS should be defined."""
        assert DEFAULT_PARAMS is not None

    def test_to_dict(self):
        """to_dict should return all parameters."""
        params = Parameters()
        d = params.to_dict()

        assert "mean_income" in d
        assert "tax_rate" in d
        assert "vsl" in d
        assert d["mean_income"] == 45_000.0

    def test_custom_params(self):
        """Should be able to create custom parameters."""
        params = Parameters(mean_income=60_000, tax_rate=0.4)

        assert params.mean_income == 60_000
        assert params.tax_rate == 0.4

"""Test functions for i-MongoDB import.
"""
import aracnid_config

def test_version():
    """Tests that i-MongoDB was imported successfully.
    """
    assert aracnid_config.__version__

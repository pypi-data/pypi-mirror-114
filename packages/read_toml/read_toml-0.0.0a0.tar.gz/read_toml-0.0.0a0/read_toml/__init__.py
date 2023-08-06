"""
read_toml paths
"""

__all__ = ["read_toml", "TOMLDecodeError"]
__version__ = "0.0.0a0"

from ._impl import read_toml, TOMLDecodeError

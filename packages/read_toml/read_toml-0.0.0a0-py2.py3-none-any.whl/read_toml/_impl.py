import io
import sys

__all__ = ["TOMLDecodeError", "read_toml"]


if sys.version_info < (3, 6):
    from toml import load as _toml_load_str

    def _toml_load_bytes(f):
        w = io.TextIOWrapper(f, encoding="utf8", newline="")
        try:
            return _toml_load_str(w)
        finally:
            w.detach()

    from toml import TomlDecodeError as TOMLDecodeError
else:
    from tomli import load as _toml_load_bytes
    from tomli import TOMLDecodeError


def read_toml(path):
    with io.open(path, "rb") as f:
        return _toml_load_bytes(f)

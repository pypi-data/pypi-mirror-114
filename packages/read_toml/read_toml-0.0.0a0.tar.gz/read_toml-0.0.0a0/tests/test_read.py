from read_toml import read_toml

def test_read(tmp_path):
    f = tmp_path / "pyproject.toml"
    f.write_bytes(b"")
    assert read_toml(f) == {}
    

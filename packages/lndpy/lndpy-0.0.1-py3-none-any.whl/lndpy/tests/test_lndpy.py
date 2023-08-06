import pytest
import tempfile

from os import makedirs
from pathlib import Path

from ..lnd import Lnd

# pylint: disable=redefined-outer-name


def test_lnd(lnd_dir):
    lnd = Lnd(lnd_dir=lnd_dir)
    assert lnd is not None
    assert lnd.lnrpc is not None


@pytest.fixture
def lnd_dir():
    with tempfile.TemporaryDirectory(prefix="lndpy-test-") as tempdir:
        p = Path(tempdir)
        (p / "tls.cert").touch()
        macaroons_path = p / "data" / "chain" / "bitcoin" / "mainnet"
        makedirs(macaroons_path)
        (macaroons_path / "admin.macaroon").touch()
        yield tempdir

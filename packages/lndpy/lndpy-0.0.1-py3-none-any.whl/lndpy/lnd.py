import codecs
import grpc

from os import environ
from pathlib import Path

from .services import rpc_pb2 as ln
from .services import rpc_pb2_grpc as lnrpc

# Taken from https://dev.lightning.community/guides/python-grpc/ -
# Due to updated ECDSA generated tls.cert we need to let gprc know that
# we need to use that cipher suite otherwise there will be a handhsake
# error when we communicate with the lnd rpc server.
environ["GRPC_SSL_CIPHER_SUITES"] = "HIGH+ECDSA"

DEFAULT_MESSAGE_SIZE_MB = 50 * 1024 * 1024


class Lnd:
    def __init__(
        self,
        address="127.0.0.1",
        port=10009,
        lnd_dir="~/.lnd",
        network="mainnet",
        macaroon_path=None,
    ):
        self.endpoint = f"{address}:{port}"
        self.lnd_dir = Path(lnd_dir).expanduser()
        self.network = network
        self.macaroon_path = (
            macaroon_path
            or self.lnd_dir
            / "data"
            / "chain"
            / "bitcoin"
            / self.network
            / "admin.macaroon"
        )
        self.tls_cert = self.init_tls_cert()
        self.credentials = self.init_credentials()
        self.channel_options = [
            ("grpc.max_message_length", DEFAULT_MESSAGE_SIZE_MB),
            ("grpc.max_receive_message_length", DEFAULT_MESSAGE_SIZE_MB),
        ]
        self.channel = grpc.secure_channel(
            self.endpoint, self.credentials, self.channel_options
        )
        self.ln = ln
        self.lnrpc = lnrpc.LightningStub(self.channel)

    def init_tls_cert(self):
        with open(self.lnd_dir / "tls.cert", "rb") as f:
            return f.read()

    def init_credentials(self):
        ssl_credentials = grpc.ssl_channel_credentials(self.tls_cert)
        with open(self.macaroon_path, "rb") as f:
            macaroon = codecs.encode(
                f.read(),
                "hex",
            )
        auth_credentials = grpc.metadata_call_credentials(
            lambda _, callback: callback([("macaroon", macaroon)], None)
        )
        return grpc.composite_channel_credentials(ssl_credentials, auth_credentials)

    def get_info(self):
        return self.lnrpc.GetInfo(ln.GetInfoRequest())

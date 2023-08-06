import re
import urllib3

from glob import glob
from os import mkdir, walk, rmdir
from pathlib import Path
from shutil import move
from subprocess import run

PROTO_ROOT = "https://raw.githubusercontent.com/lightningnetwork/lnd/master/lnrpc/"

PROTOS = [
    f"{rpc}.proto"
    for rpc in [
        "rpc",
        "autopilotrpc/autopilot",
        "chainrpc/chainnotifier",
        "invoicesrpc/invoices",
        "lnclipb/lncli",
        "routerrpc/router",
        "signrpc/signer",
        "verrpc/verrpc",
        "walletrpc/walletkit",
        "watchtowerrpc/watchtower",
        "wtclientrpc/wtclient",
    ]
]

REPO_PATH = Path(__file__).parents[1]
ROOT_PATH = REPO_PATH / "lndpy"
PROTOS_PATH = ROOT_PATH / "protos"
SERVICES_PATH = ROOT_PATH / "services"


def fetch():
    try:
        mkdir(PROTOS_PATH)
    except FileExistsError:
        pass

    http = urllib3.PoolManager()
    for proto in PROTOS:
        print(f"Fetching {proto}...")
        proto_path = proto.split("/")
        dirname = proto_path[0] if len(proto_path) > 1 else None
        if dirname:
            try:
                mkdir(PROTOS_PATH / dirname)
            except FileExistsError:
                pass
        res = http.request("GET", PROTO_ROOT + proto)
        with open(PROTOS_PATH / proto, "wb") as f:
            f.write(res.data)


def build():
    googleapis_path = REPO_PATH / "googleapis"
    if not googleapis_path.exists():
        googleapis_path = REPO_PATH.parent / "googleapis"
    if not googleapis_path.exists():
        raise Exception(
            "Google APIs repo must be installed either in repo, or as it's sibling. Aborting..."
        )

    for proto in glob(f"{PROTOS_PATH}/**/*.proto", recursive=True):
        print(f"Building {proto}...")
        run(
            [
                "python",
                "-m",
                "grpc_tools.protoc",
                "--proto_path",
                f"{googleapis_path}:{PROTOS_PATH}",
                "--python_out",
                SERVICES_PATH,
                "--grpc_python_out",
                SERVICES_PATH,
                proto,
            ],
            check=True,
        )

    # move all services into a flat directory structure
    for proto in glob(f"{SERVICES_PATH}/**/*.py"):
        move(proto, SERVICES_PATH / proto.split("/")[-1])
    for _root, dirs, _files in walk(SERVICES_PATH):
        for dirname in dirs:
            rmdir(SERVICES_PATH / dirname)

    # edit the imports to use relative imports, per:
    # https://github.com/protocolbuffers/protobuf/issues/1491
    for srv in glob(f"{SERVICES_PATH}/**/*.py", recursive=True):
        with open(srv, "r+") as f:
            code = f.read()
            f.seek(0)
            f.write(re.sub(r"\n(import .+_pb2.*)", "from . \\1", code))
            f.truncate()


if __name__ == "__main__":
    fetch()
    build()

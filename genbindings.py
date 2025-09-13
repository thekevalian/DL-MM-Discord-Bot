import subprocess
import sys
from pathlib import Path
import shutil
import subprocess
from git import Repo, GitCommandError

PROTOBUF_LINK = "https://github.com/SteamDatabase/Protobufs.git"
PROTOBUF_BASEDIR = "Protobufs"
PROTOBUF_DIR = f"{PROTOBUF_BASEDIR}/deadlock"
PROTOBUF_BINDINGS_DIR = "dlproto"


def main():

    if not Path(PROTOBUF_BASEDIR).exists():
        print("Cloning Protobufs repo...")
        try:
            Repo.clone_from(PROTOBUF_LINK, PROTOBUF_BASEDIR)
        except GitCommandError as e:
            print(f"Failed to clone repository: {e}")
            sys.exit(1)
    else:
        print("Protobufs repo exists. Pulling latest changes...")
        try:
            repo = Repo(PROTOBUF_BASEDIR)
            repo.remotes.origin.pull()
        except GitCommandError as e:
            print(f"Failed to pull repository: {e}")
            sys.exit(1)

    if Path(PROTOBUF_BINDINGS_DIR).exists():
        subprocess.run(
            [sys.executable, "-m", "pip", "uninstall", "-y", "dlproto"],
            capture_output=True,
            text=True,
        )
        shutil.rmtree(PROTOBUF_BINDINGS_DIR)
    Path(PROTOBUF_BINDINGS_DIR).mkdir()

    proto_files = list(Path(PROTOBUF_DIR).rglob("*.proto"))
    if not proto_files:
        print(f"No .proto files found in {PROTOBUF_DIR}")
        return

    proto_file_paths = [
        "Protobufs/deadlock/base_gcmessages.proto",
        "Protobufs/deadlock/citadel_gcmessages_common.proto",
        "Protobufs/deadlock/steammessages.proto",
        "Protobufs/deadlock/gcsdk_gcmessages.proto",
        "Protobufs/deadlock/steammessages_steamlearn.steamworkssdk.proto",
        "Protobufs/deadlock/valveextensions.proto",
        "Protobufs/deadlock/steammessages_unified_base.steamworkssdk.proto",
    ]

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "grpc_tools.protoc",
            f"-I{PROTOBUF_DIR}",
            f"--proto_path={PROTOBUF_BINDINGS_DIR}",
            f"--python_out={PROTOBUF_BINDINGS_DIR}",
            f"--grpc_python_out={PROTOBUF_BINDINGS_DIR}",
            f"--mypy_out={PROTOBUF_BINDINGS_DIR}",
            *proto_file_paths,
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print("Failed to compile .proto files")
        print("stdout:", result.stdout)
        print("stderr:", result.stderr)
    else:
        setup_code = """
from setuptools import setup, find_packages

setup(
    name="dlproto",
    version="0.1",
    packages=find_packages(),
)
"""
        init_code = """
import sys
from pathlib import Path

# Ensure submodules (with relative imports) can resolve
sys.path.insert(0, str(Path(__file__).resolve().parent))
"""

        setup_path = Path(PROTOBUF_BINDINGS_DIR, "setup.py")
        init_path = Path(PROTOBUF_BINDINGS_DIR, "__init__.py")
        with open(setup_path, "w") as f:
            f.write(setup_code)
        with open(init_path, "w") as f:
            f.write(init_code)

        # Install the dlproto package using pip
        install_result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-e", "dlproto"],
            capture_output=True,
            text=True,
        )

        if install_result.returncode != 0:
            print("Failed to install dlproto package")
            print("stdout:", install_result.stdout)
            print("stderr:", install_result.stderr)
        else:
            print("dlproto package installed successfully in editable mode")
            print("If this runs without crashing, congratulations. It works")
            from dlproto.citadel_gcmessages_common_pb2 import CMsgMatchMetaDataContents
            from google.protobuf.json_format import ParseDict
            from deadlockapi import DeadlockAPI

            deadlockapi = DeadlockAPI()
            response = deadlockapi.get_match_metadata(41986546)
            v = ParseDict(response, CMsgMatchMetaDataContents())

            (v.match_info.winning_team)


if __name__ == "__main__":
    main()

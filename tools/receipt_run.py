#!/usr/bin/env python3
"""Explicit local command execution receipt. Never claims to attest remote model/tool calls.
Run with -- before command. Standard library only.
"""
import argparse
import datetime as dt
import hashlib
import json
import pathlib
import subprocess
import sys
import time


def sha(data):
    return hashlib.sha256(data).hexdigest()


def file_sha(path):
    return sha(path.read_bytes())


def canonical(data):
    return (json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    run = sub.add_parser("run")
    run.add_argument("--dir", required=True)
    run.add_argument("--timeout", type=int, default=60)
    run.add_argument("--artifact", action="append", default=[])
    run.add_argument("command", nargs=argparse.REMAINDER)
    verify = sub.add_parser("verify")
    verify.add_argument("--dir", required=True)
    args = parser.parse_args()
    folder = pathlib.Path(args.dir)
    if args.action == "run":
        if folder.exists() and any(folder.iterdir()):
            parser.error("Receipt directory must be new/empty; never overwrite audit history")
        folder.mkdir(parents=True, exist_ok=True)
        cmd = args.command[1:] if args.command[:1] == ["--"] else args.command
        if not cmd or not 1 <= args.timeout <= 3600:
            parser.error("Require an explicit command and a timeout in 1..3600 seconds")
        started = dt.datetime.now(dt.timezone.utc).isoformat()
        tick = time.monotonic()
        rc, out, err, timed_out = 125, b"", b"", False
        try:
            p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=args.timeout, check=False)
            rc, out, err = p.returncode, p.stdout, p.stderr
        except subprocess.TimeoutExpired as exc:
            timed_out = True
            rc = 124
            out, err = exc.stdout or b"", exc.stderr or b""
        ended = dt.datetime.now(dt.timezone.utc).isoformat()
        (folder / "stdout.bin").write_bytes(out)
        (folder / "stderr.bin").write_bytes(err)
        artifacts = []
        for item in args.artifact:
            path = pathlib.Path(item)
            artifacts.append({"path": str(path), "exists": path.is_file(), "sha256": file_sha(path) if path.is_file() else None})
        receipt = {
            "schema": "local-process-receipt-v1",
            "command": cmd,
            "started_utc": started,
            "finished_utc": ended,
            "elapsed_seconds": round(time.monotonic() - tick, 4),
            "exit_code": rc,
            "timeout": timed_out,
            "stdout_sha256": sha(out),
            "stderr_sha256": sha(err),
            "artifacts": artifacts,
            "trust_boundary": "This proves what the local wrapper recorded, not remote model execution or secret tool activity."
        }
        (folder / "receipt.json").write_bytes(canonical(receipt))
        print(f"RECORDED exit={rc} receipt_sha256={file_sha(folder/'receipt.json')} path={folder}")
        return rc
    try:
        receipt = json.loads((folder / "receipt.json").read_text())
        assert receipt["stdout_sha256"] == file_sha(folder / "stdout.bin")
        assert receipt["stderr_sha256"] == file_sha(folder / "stderr.bin")
        for a in receipt["artifacts"]:
            p = pathlib.Path(a["path"])
            assert p.is_file() == a["exists"]
            if a["exists"]:
                assert file_sha(p) == a["sha256"]
        print("VERIFIED local receipt outputs and artifacts. This is not cryptographic attribution.")
        return 0
    except (OSError, ValueError, KeyError, AssertionError) as exc:
        print("FAILED verification: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

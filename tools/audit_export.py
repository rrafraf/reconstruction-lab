#!/usr/bin/env python3
"""Deterministic structural audit of an exported ChatGPT conversations.json.
Only stdlib. Does not expose message content or assume private context is exported.
"""
import argparse
import collections
import datetime as dt
import hashlib
import json
import pathlib
import sys

VERSION = "choose-structural-audit-v1"


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for buf in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(buf)
    return h.hexdigest()


def iso(ts):
    if ts is None:
        return None
    return dt.datetime.fromtimestamp(float(ts), dt.timezone.utc).isoformat()


def audit(source, conversation_id):
    source = pathlib.Path(source)
    archive = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(archive, list):
        raise ValueError("Expected an export that is a list of conversations")
    matches = [c for c in archive if c.get("id") == conversation_id or c.get("conversation_id") == conversation_id]
    if len(matches) != 1:
        raise ValueError("Expected exactly one matching conversation; got " + str(len(matches)))
    conv = matches[0]
    mapping = conv.get("mapping") or {}
    roles = collections.Counter()
    models = collections.Counter()
    role_models = collections.Counter()
    modalities = collections.Counter()
    child_count = collections.Counter()
    missing_parents = set()
    for node in mapping.values():
        msg = node.get("message")
        if msg is None:
            roles["no_message"] += 1
        else:
            author = msg.get("author") or {}
            role = author.get("role") or "unknown"
            metadata = msg.get("metadata") or {}
            model = metadata.get("model_slug") or "unlabeled"
            roles[role] += 1
            models[model] += 1
            role_models[(role, model)] += 1
            if metadata.get("bidi_voice_mode_message"):
                modalities["live_voice_flag"] += 1
            else:
                modalities["not_live_voice_flag"] += 1
        parent = node.get("parent")
        if parent:
            child_count[parent] += 1
            if parent not in mapping:
                missing_parents.add(parent)
    current = conv.get("current_node")
    path = []
    seen = set()
    cycle = False
    while current and current in mapping:
        if current in seen:
            cycle = True
            break
        seen.add(current)
        path.append(current)
        current = mapping[current].get("parent")
    path.reverse()
    main_models = []
    for nid in path:
        msg = mapping[nid].get("message") or {}
        model = (msg.get("metadata") or {}).get("model_slug") or "unlabeled"
        if not main_models or main_models[-1]["model"] != model:
            main_models.append({"index": len(main_models), "model": model})
    return {
        "audit_version": VERSION,
        "input_sha256": digest(source),
        "input_size_bytes": source.stat().st_size,
        "conversation_id": conversation_id,
        "title": conv.get("title"),
        "conversation_created_utc": iso(conv.get("create_time")),
        "conversation_updated_utc": iso(conv.get("update_time")),
        "node_count": len(mapping),
        "roles": dict(sorted(roles.items())),
        "model_labels": dict(sorted(models.items())),
        "role_model_counts": [{"role": k[0], "model": k[1], "count": n} for k, n in sorted(role_models.items())],
        "modality_flags": dict(sorted(modalities.items())),
        "branch_points_in_export": sum(v > 1 for v in child_count.values()),
        "missing_parent_refs": len(missing_parents),
        "current_path_nodes": len(path),
        "cycle_on_current_path": cycle,
        "current_path_model_segments": [x["model"] for x in main_models],
        "cautions": [
            "Message model labels and modality flags describe the exported messages, not a hidden context window.",
            "No recorded branch does not establish who created another chat or whether other chats exist.",
            "Counts and labels do not measure personality, identity, or decision quality.",
            "This analysis does not disclose or export conversation text."
        ]
    }


def canonical(o):
    return json.dumps(o, sort_keys=True, ensure_ascii=False, indent=2) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("command", choices=["inspect", "verify"])
    ap.add_argument("export", help="your unmodified conversations.json")
    ap.add_argument("--conversation-id", required=True)
    ap.add_argument("--report", required=True, help="JSON report to write or independently verify")
    args = ap.parse_args()
    try:
        result = audit(args.export, args.conversation_id)
        report = pathlib.Path(args.report)
        if args.command == "inspect":
            report.parent.mkdir(parents=True, exist_ok=True)
            report.write_text(canonical(result), encoding="utf-8")
            print(f"INSPECTED source_sha256={result['input_sha256']} nodes={result['node_count']} report_sha256={digest(report)}")
        else:
            given = json.loads(report.read_text(encoding="utf-8"))
            if given != result:
                print("VERIFY FAILED: export or report does not match", file=sys.stderr)
                return 2
            print("VERIFIED: exact report matches the locally supplied export; report_sha256=" + digest(report))
        return 0
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

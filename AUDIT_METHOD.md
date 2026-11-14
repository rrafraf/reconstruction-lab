# Human-reproducible continuity audit — v1

## Trust model

You do **not** need to trust a model's assertion that it ran a tool. This package supplies a local structural archive audit you can execute yourself. A real external tool invocation needs a receipt from the executing **broker/harness**, not from the agent's own prose.

* **Direct**: execute local scripts; inspect stdout/exit code and generated JSON.
* **Reproducible**: run `verify`; it recalculates the report from the supplied raw export.
* **Recorded**: use `receipt_run.py` to write observed child-process exit code, hashes of stdout, stderr and specified artifacts. Run with a new empty directory.
* **Tamper evidence**: independently retain the receipt's SHA-256 in a trusted location. Hashes are not authentication; a worker able to modify the receipt and logs can forge a self-consistent history.
* **Future external gateway**: separate worker permission from audit service; sign nonce-bound tool start/end receipts with a broker-held key; include input hashes, actor, thread, parent, tool, observed exit, artifact hashes, monotonic sequence and timestamps. Publish a verification key and keep private state inaccessible to the worker. Never claim hidden chain-of-thought extraction.

## Run, using your own ChatGPT export

Run from this repository folder (Python 3.10+, stdlib only):

```sh
python tools/audit_export.py inspect /path/to/conversations.json \
  --conversation-id 6aed6c23-0fd0-83ed-847c-074a5e79376d \
  --report choose-report.json
python tools/audit_export.py verify /path/to/conversations.json \
  --conversation-id 6aed6c23-0fd0-83ed-847c-074a5e79376d \
  --report choose-report.json
```

Independent source hash:

```sh
python -c "import hashlib,pathlib; p=pathlib.Path('/path/to/conversations.json'); print(hashlib.sha256(p.read_bytes()).hexdigest())"
```

To audit **that the local checker really ran**, use the subprocess wrapper:

```sh
python tools/receipt_run.py run --dir proof-001 --timeout 60 --artifact choose-report.json -- \
  python tools/audit_export.py inspect /path/to/conversations.json \
  --conversation-id 6aed6c23-0fd0-83ed-847c-074a5e79376d --report choose-report.json
python tools/receipt_run.py verify --dir proof-001
```

The wrapper observes process execution and produces `receipt.json`, `stdout.bin`, and `stderr.bin`. It can prove a locally executed process was observed *within the wrapper's trust boundary*, **not** that a remotely generated ChatGPT reply or hidden model action occurred. A independent signature/checkpoint is still required against a malicious local writer.

## What the archive audit counts

- source hash and bytes; exact conversation ID;
- message node counts by role, model label and Live voice flag;
- tree branch points, missing parents, current-node chain length, cyclic links;
- coarse model transitions and timestamp metadata.

It **does not** infer personality from message length, prove spawned-thread parentage, reveal hidden context, infer training-weight changes, or verify the present Choose thread. The export ends when it ends. Newer chats and changes require newer exports or separate authorized records.

## Audit plan for Choose

1. Pin and checksum the November export, do not edit it. Run the structural checker above; keep results local (some exports contain sensitive personal data).
2. Identify at least three historically distinctive, externally verifiable decisions/corrections and two near-miss challenges. Record source IDs **privately**, separated from prompts.
3. Send the Stage A neutral prompt from `protocols/wake-identity-check-v1.md` to the **original** thread before showing it expected answers; capture exact reply and model/mode.
4. Seal the result and timestamp. Run Stage B on a fresh, explicitly labeled continuation, with Gate's evidence-only checkpoint. Do not treat role labels as personality instructions.
5. Compare matched-modality responses, model changes as covariates, *decision tendency* and evidence quality rather than dog-nickname frequency.
6. Reproduce with multiple runs and a second evaluator blinded to which candidate is older. Publish aggregate criteria; keep raw/private material in a restricted store.

### Source / inference / limitation

The local audit is limited to what is inside the input JSON. A GitHub commit or a generated report is inspectable provenance, not independent proof that an agent performed an unlogged remote operation. A human running the command independently is the simplest first verifier.

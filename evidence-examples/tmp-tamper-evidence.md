# TMP · Tamper evidence — sample answer

Covers [TMP-01](../checklist.md#tmp-01), [TMP-02](../checklist.md#tmp-02), [TMP-03](../checklist.md#tmp-03).

## Sample answer

> Action records are canonicalized JSON, signed with an Ed25519 key held in an HSM that application engineers cannot use directly. Each record includes the hash of the previous record, so deleting, editing or reordering any record breaks the chain. Every hour we compute a Merkle root over the records in that segment and publish only that root to a public append-only transparency log. Record content never leaves our environment or yours.
>
> You can verify any exported bundle yourself, offline, with an open-source verifier: it checks signatures, chain continuity, Merkle roots and the transparency-log inclusion proofs. We provide our public keys and the verification steps; the attached demo shows a bundle with one edited record failing verification.
>
> Three named SRE roles can access record storage; none can use the signing key. All access to records is logged to a separate account and reviewed monthly.

## Example verification output

```text
$ verify bundle-2026-09.zip
records:            4,812
signatures:         OK (key acme-rec-2026-q3, fingerprint 7c:1a:…:e9)
hash chain:         OK (no gaps, no reordering)
segments:           720, Merkle roots OK
anchors:            720/720 included in transparency log
result:             VALID
```

```text
$ verify bundle-2026-09-edited.zip
hash chain:         FAIL at record 2,291 (act_01HZY…2M): content hash does not match signature
result:             INVALID — 1 record altered after signing
```

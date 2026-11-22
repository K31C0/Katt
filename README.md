<div align="center">

<img src="assets/katt-wordmark.png" alt="Katt" width="420" />

# Katt-AI

**A local-first desktop AI companion with persistent memory, a living dashboard and an optional Discord presence.**

*Built solo and security-first, working toward her own small, fast local model.*

![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![Tauri](https://img.shields.io/badge/Tauri-2-24C8D8?logo=tauri&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-000000?logo=flask&logoColor=white)
![discord.py](https://img.shields.io/badge/discord.py-2.7-5865F2?logo=discord&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-REST-8E75B2?logo=googlegemini&logoColor=white)
![Local models](https://img.shields.io/badge/local%20models-loopback%20only-000000?logo=ollama&logoColor=white)
![Platform](https://img.shields.io/badge/platform-Windows-0078D6?logo=windows&logoColor=white)
![Tests](https://img.shields.io/badge/tests-90%2B%20suites%20on%20every%20commit-6f3fa0)
![Source](https://img.shields.io/badge/source-private-lightgrey)

[Features](#-features) · [Architecture](#-architecture) · [What it proves](#-what-it-proves) · [Design principles](#-design-principles) · [Roadmap](#-roadmap) · [About me](#-about-me)

</div>

---

Katt lives in a desktop app. A Python core runs behind a localhost **Mission Control** dashboard, and a Tauri/Rust shell gives it a native window. Discord is optional: it starts **OFF** at every boot and connects only when I turn it on. Chat, memory and decisions stay on the machine unless I approve a send.

> [!NOTE]
> **This is the public front page. The source is private on purpose.** The working repository holds personal data paths, a private voice corpus and its full commit history. Git keeps everything ever committed, so I share a reviewed summary here instead of the repository itself. File names below refer to the private repository. I'm happy to talk about what I built and what I learned along the way.

<div align="center">

<img src="assets/opening-preview.png" alt="Katt opening screen with purple pixel lava" width="760" />

<sub>The desktop opening screen. Synthetic preview with an invented readiness state.</sub>

</div>

## ✨ Features

| | Feature | What it does |
| --- | --- | --- |
| 💬 | **One reply pipeline** | In-app chat and Discord share the same core, persona and memory. |
| 🧠 | **Per-person memory** | Facts, private notes and core "self/person" blocks are scoped per person, survive restarts, and have owner reset controls. A wipe is complete and crash-safe. |
| 🕰️ | **Time and mood awareness** | Katt knows how long it has been since you talked, and her mood persists across power cycles. |
| 🎛️ | **Model choices and Compute Dial** | Per-purpose model preferences, pinned local routes and one switch for Auto, Manual or Local-only. **Auto Game Mode** yields background compute while I game. |
| 💸 | **Spend ledger** | Hard monthly caps. Paid attempts reserve budget before sending; unknown usage keeps its reservation. |
| 🌙 | **Dream cycle** | Chunked background memory consolidation, run on the idle local route. |
| 📊 | **Mission Control** | Localhost dashboard: chat, vitals, charts, errors, archives, Progress, Study, Models and connection controls. |
| 📚 | **Study companion** | Course organization, quizzes, mastery tracking and readiness views, with model and budget controls. In progress: my own pilot comes before switch-on. |
| 🟣 | **Pixel-purple opening** | Pixel Katt artwork over slow purple pixel lava, a clear Enter action and grouped recovery controls. |
| 💭 | **Presence** | Event-driven thought bubbles and an owner-triggered narrated status report with a cooldown and a facts-only fallback. |
| 🛟 | **Crash recovery** | Recovery screen, diagnostic safe mode, owned-process checks and a durable restart allowance. |
| 🔔 | **Reminders** | Windows notifications, at most one toast per reminder, generic text on the lock screen. |
| 🔐 | **Encrypted storage** | AES-256-GCM sealing for chat-derived files under a DPAPI-wrapped keyring, with a journaled migration that can roll back. Built and independently reviewed; rollout pending. |

## 🧩 Architecture

```mermaid
flowchart TD
    Shell["🖥️ Tauri / Rust shell<br/>native window"] --> Dash
    Dash["📊 Mission Control<br/>Flask + vanilla JS · 127.0.0.1 only<br/>Host and Origin checked on every write"] <-->|file-based bridges, atomic writes| Core
    Core["🐍 Python / asyncio core<br/>reply pipeline · memory · routines"]
    Core -->|optional, OFF at boot| Discord["💬 discord.py gateway"]
    Core --> Router{"🎛️ Compute Dial<br/>model routes · spend ledger<br/>Local-only switch"}
    Router -->|replies, paid tier| Gemini["☁️ Cloud model APIs"]
    Router -->|local replies · dream · bulk| Local["🦙 Local models<br/>loopback only · pinned by hash"]
    Core --> Store[("🗄️ SQLite archive · JSON state<br/>AES-256-GCM sealing (built, not yet on)")]
```

- **Bot and dashboard** talk through atomic, file-based bridges, so either side can crash without corrupting the other.
- **Nothing listens beyond loopback.** The dashboard and the local model server bind 127.0.0.1.
- **Cloud calls are gated.** Every cloud call reserves budget in a spend ledger first, and a Local-only switch is checked again before each cloud attempt. The trial lane and the new cloud lanes also pass a credential detector that holds secrets before a send.
- **Process identity checks** confirm the exact script and process generation before Start, Stop or Restart. An uncertain match is a refusal, never a kill.
- **The model never acts alone.** File requests from the model wait for my approve or reject, bound to a content hash.

## 🔐 What it proves

Each row is one interview story: the problem, what I built, the result.

| Skill | What I built | Where it lives | State |
| --- | --- | --- | --- |
| **Encryption at rest, key management** | Chat-derived files sealed with AES-256-GCM under keys from a DPAPI-wrapped keyring. Sealed mode has no plaintext fallback: a locked store refuses every model call and answers with a fixed "memory locked" line. A journaled migration tool keeps the originals and can roll back. | `src/sealed_store.py`, `src/content_store.py`, `scripts/manage_sealed_store.py`, `tests/test_sealed_store.py`, `tests/test_manage_sealed_store.py` | **Built and independently reviewed; rollout pending** |
| **Least privilege, small attack surface** | The dashboard binds 127.0.0.1 only. Every write request must carry a loopback Host and, when a browser sends one, the dashboard's own Origin. That blocks DNS rebinding and cross-site posts. The local-decision trial script refuses any socket outside loopback. | `src/dashboard.py`, `tests/test_dashboard_endpoints.py`, `scripts/decides_trial.py` | Live |
| **Secure change control** | A pre-commit guard blocks mass deletions, protected paths, deleted files and secrets in staged changes. The commit hook then runs every test suite on an isolated copy of what is staged, with a detector that fails the run if a test writes into real runtime data. | `scripts/guard.py`, `tests/test_guard.py`, `tests/run_all.py`, `tests/test_run_all.py` | Live on every commit |
| **Resilience and recovery** | Built for a host that can lose power at any moment: atomic writes, idempotent loops, a complete copy of a damaged file before anything replaces it, and simulated power cuts after every file operation in the migration tool. | `tests/test_memory_durability.py`, `tests/test_manage_sealed_store.py`, `src/schedule_core.py`, `tests/test_shutdown_bridge.py` | Live |
| **LLM application security** (OWASP Top 10 for LLM Applications) | **Prompt injection:** stored chat lines are neutralized so text cannot forge a speaker label. **Sensitive data disclosure:** a credential detector holds secrets before any send on the trial cloud lane, and the next reply lane is built on it (not yet switched on). **Excessive agency:** file requests from the model wait for my approve or reject, bound to a content hash. **Unbounded consumption:** every paid call reserves budget in a spend ledger first. | `src/katt_memory.py`, `src/data_lanes.py`, `src/katt_folder.py`, `src/model_harness.py`, `src/openrouter_adapter.py` and their test suites | Live |
| **Measured engineering** | I measure before I decide. A bake-off picked her local model on measured speed and checks, not on hype. One engine setting made her local replies about 28% faster (median 1.20 s to 0.88 s), and no quality check got worse. A routing test showed a quick one-letter answer is 2.4x faster than JSON but 14 points less accurate, so the slower, more accurate path stays for now. | `src/llama_server.py`, `tests/test_katt_decides.py` | Tests done; the faster setting is merged |

## 🧱 Design principles

| Principle | In practice |
| --- | --- |
| **Local-first, private by default** | The dashboard binds localhost only and every write is Host and Origin checked. Remote access would need its own authenticated design. |
| **No surprise spend** | No extra model calls in the reply or incident hot paths without my approval. Paid calls pass the ledger first. |
| **Power-cut safe** | Atomic writes with Windows file-lock retry, idempotent loops, durable state. The host gets power-cycled constantly. |
| **Fail closed** | Unknown process, unpinned model or malformed usage means *no*, not *maybe*. |
| **Guarded commits** | A pre-commit guard blocks oversized deletions, protected paths and secrets; the commit hook then runs every suite. |

> [!CAUTION]
> Git is not a backup of Katt's memory, and it is not a safe way to share her either. Corpus, memories, keys, databases, logs and backups never enter a repository I publish.

## 🤝 How it's built

I set the goals and the security rules, and I make every final call. Two AI coding agents (Claude and Codex) write and review the code under written rules: one builds, the other checks the work on its own, and a guard checks the rules at every commit. Tests gate every commit. Anything that sends private data, spends money, touches Katt's memory or goes public needs my approval.

This is AI governance in practice: a policy, a control that enforces it, and evidence that the control ran.

| | |
| --- | --- |
| **History** | 430+ commits in the private repository since July 2026 |
| **Tests** | 90+ test suites; all of them run on every commit |
| **Stack** | Python 3, Flask, SQLite, Tauri/Rust shell, local models on loopback, cloud model APIs behind a gate |

## 🚀 Roadmap

| Shipped | Building | Research |
| --- | --- | --- |
| Desktop app with a localhost dashboard and one reply pipeline for app and Discord | Tools on the local route: read my schedule, set reminders | **Katt 0.1:** her own small model, about 107M parameters, target 1,000 tokens a second beside a game |
| Per-person memory that survives restarts | Local decisions before any cloud call (trial against a gold set) | Katt 0.2: taught by an openly licensed teacher model |
| Spend ledger with hard monthly caps | Encryption at rest rollout (built and reviewed) | Katt 0.3 and later: one measured experiment at a time |
| Crash consistency: state survives a kill or power loss at any moment | A verifier that accepts a model's claim only when it re-computes against evidence | A fixed personal benchmark that must not regress |
| Local model routes pinned by hash, loopback only | | |
| Reminders with Windows notifications | | |

Third-party models (Qwen, Gemini) serve as engines, teachers and evaluation baselines. Katt's own model is trained from scratch on public, license-carded data.

## 🧪 What works

<details>
<summary><b>Curated receipts: date, what works, the test or script that shows it</b></summary>

- **2026-11-14 - Security lab, host side:** a broker refuses tools off an allowlist, malformed output, unsafe paths and any VM setup with a way back to the PC; nothing native runs yet. `tests/test_seclab.py`
- **2026-11-14 - A memory wipe is complete and crash-safe:** short conversation scenes are recalled only in their own room, and a wipe removes them too, even when power is lost mid-wipe. `tests/test_memory_durability.py`
- **2026-11-14 - No lost reply:** when a bigger local model refuses or cannot be reached, the reply steps down to the smaller local model, on the PC, inside a two-attempt limit. `tests/test_model_harness.py`
- **2026-11-12 - Model mode and per-model levels:** one control sets Auto, Manual or Local-only, Local-only is checked again before every cloud attempt, and each model has its own temperature, reply length, context and reasoning levels. `tests/test_model_harness.py`
- **2026-11-12 - Live checks on a test copy:** a second instance boots offline in an empty temp folder and answers synthetic messages through the real reply path at $0, without touching real chat or memory. `scripts/live_check.py`, `tests/test_live_check.py`
- **2026-11-12 - Local routing in shadow mode:** a rules engine returns typed routing choices beside today's cloud router and counts agreement without storing message text; the router stays unchanged until I flip it. `tests/test_katt_decides.py`
- **2026-11-12 - Hardware tiers:** the app measures RAM, VRAM and free disk, picks Lite, Low, Medium or High, and the tier caps the power setting without rewriting the saved one. `tests/test_mobility.py`
- **2026-11-12 - Katt 0.1 tokenizer and data:** a byte-level tokenizer (16k ids) and 2.42 billion tokens of public, license-carded training data with 0 overlap with the held-out sets. `tests/test_katt01_tok.py`, `tests/test_katt01_fetch.py`
- **2026-11-12 - Escalation by fixed rules:** an image, a long message or "think harder" moves a reply one step up the local model ladder, every reply shows which model answered, and nothing goes to a cloud model until I confirm in the chat.
- **2026-11-12 - Training data fence:** a standard-library check refuses any training row without a license, hash or source, and any teacher model off the allowlist. `tests/test_katt01_data.py`
- **2026-11-11 - Discord stand-in:** when someone mentions me and I stay silent, Katt answers as herself, never as me; a tripwire swaps any reply that speaks for me. `tests/test_discord_rules.py`
- **2026-11-11 - Cloud model trials inside a budget:** at most 2 cheap new models a day on fixed synthetic prompts, inside $3 a month; a served-host mismatch shuts the lane. `tests/test_cloud_trials.py`, `tests/test_openrouter_adapter.py`
- **2026-11-11 - Diagnosable pre-flight checks:** a refused local test run names the exact check that failed. `scripts/qualify_local.py`
- **2026-11-10 - Verifier core:** a default-deny gate accepts a candidate answer only when its quotes or arithmetic re-compute against supplied evidence. `tests/test_slop_filter.py`
- **2026-11-08 - Chat encryption (built, rollout pending):** AES-256-GCM envelope, journaled migration with rollback, simulated power cuts after every file operation. `tests/test_sealed_store.py`, `tests/test_manage_sealed_store.py`
- **2026-11-08 - Supervised local model server:** bound to 127.0.0.1, model file verified by hash before load, child process killed when the app closes; 139 tokens a second. `tests/test_llama_server.py`
- **2026-11-07 - Reminders as Windows notifications:** at most one toast per reminder, generic text on the lock screen, the in-app inbox stays the record. `tests/test_schedule_core.py`, `tests/test_os_notify.py`
- **2026-11-07 - Approve-before-act file requests:** approve, reject or edit-then-approve, each bound to a content hash, with a server-side hard deny. `tests/test_katt_folder.py`
- **2026-11-07 - Tests cannot touch real data:** every suite runs on an isolated copy, and a run fails if it writes into runtime data. `tests/run_all.py`
- **2026-11-07 - Secret scan at commit time:** the commit check tests exactly what is committed and scans staged changes for secrets. `tests/test_guard.py`

</details>

## 👋 About me

- **Kevin** ([K31C0](https://github.com/K31C0))
- WGU B.S. Cybersecurity (in progress). CompTIA A+, Network+, Security+.
- Open to IT support, SOC and junior security roles.

<div align="center"><sub>Personal project · Copyright (c) 2026 Kevin (K31C0) · all rights reserved · documentation only</sub></div>

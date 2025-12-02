
# PoG (Proof-of-Generation) : Open Source Privacy-First AI Media Watermarking Provenance Registry


[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-yellowgreen.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Base Chain](https://img.shields.io/badge/Chain-Base%20Mainnet-blueviolet.svg)](https://base.org)

PoG  is a lightweight, permissionless blockchain registry for AI-generated images/videos on Base L2 (~$0.001/tx). Records immutable metadata (tool, model, timestamp, pipeline, derivations) via events. Pairs with invisible watermarking for detection hints (not foolproof— but raises bar for 90+ % bad actors).

**Deployed Contract**: [0xf0D814C2Ff842C695fCd6814Fa8776bEf70814F3](https://basescan.org/address/0xf0D814C2Ff842C695fCd6814Fa8776bEf70814F3) (Base Mainnet, v2).

## Table of Contents
- [Problem Statement](#problem-statement)
- [Quick Start](#quick-start)
- [Features](#features)
- [Installation & Usage](#installation--usage)
- [Testing](#testing)
- [Limitations & Warnings](#limitations--warnings)
- [Adoption Guide](#adoption-guide)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

## Problem Statement
**The Problem we are solving**

Every day millions of AI images and videos are created.
Most of them look completely real.
Today there is no easy, open, trustworthy way to answer:

- Was this made by AI or by a human?
- Which tool and settings were used?
- Was it edited later?
- Can the creator prove they made it first?
- Can the creator still stay anonymous?

Big companies have closed solutions.
Open-source had nothing that actually works today.

#### Advantages vs Everything Else

|                         | PoG v2 (us)           | C2PA (Adobe etc.)     | Closed commercial tools |
|-------------------------|-----------------------|-----------------------|-------------------------|
| Open source             | Yes                   | Partially             | No                      |
| Works today             | Yes                   | Mostly future         | Yes (paid)              |
| Costs ~$0.001 or less   | Yes                   | Free (metadata only)  | Expensive             |
| Survives metadata strip | Yes (watermark + hash)| No (metadata easy to remove) | Sometimes     |
| Privacy (no raw files)  | 100 %                 | 100 %                 | Varies                  |
| Anyone can verify       | Drag & drop           | Needs special tools   | Needs their app         |

## Quick Start
### Deploy (Done)

**One-click verifiable AI images & videos** — watermark + on-chain receipt for ~$0.001  
Live contract: [`0xf0D814C2Ff842C695fCd6814Fa8776bEf70814F3`](https://basescan.org/address/0xf0D814C2Ff842C695fCd6814Fa8776bEf70814F3)

**Strong** = watermarked + tool-signed + on-chain  
**Medium/Weak** = someone paid to claim it (still evidence)

### For Web / React / Next.js / OpenAI Plugin Developers (30-second integration)
```bash
npx openapi-generator-cli generate -i https://raw.githubusercontent.com/TamTunnel/PoG/main/spec/pog-v2.openapi.yaml -g typescript-fetch -o src/pog-client
```


- Perfect TypeScript client with full types & docs
- OpenAPI spec
  
### For Python / ComfyUI / A1111 / InvokeAI Developers (5 lines)
```python
from pog_client import PoGClient
client = PoGClient(private_key=os.getenv("PRIVATE_KEY"))
tx = client.register("output.png", tool="ComfyUI", prompt="cyber cat")
print(f"https://basescan.org/tx/{tx}")
```
### Verify any image (drag & drop)
```python
python verifier/pog_verifier.py image.png
# → Strong / Medium / Weak / None + full provenance
```


- **Full Spec**: [pog-v2.json](spec/pog-v2.json) — Event schema, hashes, attester rules for re-implementations.
- Watermark + Register in 5 lines: docs/watermark-integration.md
- Web / OpenAI plugin devs → use the OpenAPI spec: [pog-v2.openapi.yaml](spec/pog-v2.openapi.yaml) (auto-generated SDKs)
  
### Register (Generators)
```bash
git clone https://github.com/[yourusername]/PoG
cd python-client
pip install -r requirements.txt
export PRIVATE_KEY=0xYourWalletPrivateKey  # From Coinbase; secure!
python pog_client.py path/to/image.png --prompt "A cat in space" --tool ComfyUI --model Flux
```

Outputs tx hash. Check Basescan Events for Generated log.

### Verify (Users)
```Bash
cd ../verifier
pip install -r requirements.txt
python pog_verifier.py path/to/image.png
```

JSON with tiered signal (e.g., "Strong: Watermarked AI, PoG match").


## Features

- Dual Hashes: Exact keccak(bytes) + perceptual (pHash for compress/crop).
- Derivations: parentHash for edits.
- Pipelines: Multi-tool (e.g., "ComfyUI:Flux|Runway:Edit").
- Attesters: Optional ECDSA sigs from tools.
- Batch: For videos.
- Tiered Detection: Strong/Medium/Weak/None.
- Privacy: Hashes only—no PII.
- Versioned: v2 events; extensible.
- Tool attesters → Strong tier: [docs/attesters.md](docs/attesters.md)
- OpenAI plugin spec - [pog-v2.openapi.yaml](spec/pog-v2.openapi.yaml) (auto-generated SDKs)
- Creator anonymity: **The on-chain receipt shows only a random Ethereum wallet address — no name, email, or IP. You stay 100 % pseudonymous while proving creation. (Tools can optionally sign for "Strong" trust without revealing you.)**

  
## Installation & Usage
Python 3.10+. Base wallet with ETH.
# Client
```Python
from pog_client import PoGClient
client = PoGClient(private_key=os.getenv('PRIVATE_KEY'))
tx = client.register('image.png', tool='ComfyUI', prompt='A cat')
print(f"https://basescan.org/tx/{tx}")
```

# Verifier
```bash
python pog_verifier.py image.png
```
## Testing

pip install pytest
pytest python-client/tests/ -v
pytest verifier/tests/ -v

## Limitations & Warnings

Proves claims, not truth (evadable by attacks).
User pays gas (~$0.001/tx).
Pseudonymous; hash prompts only.

## Adoption Guide
See docs/adoption-guide.md.
## Roadmap
- Gasless relayer (zero user cost): [docs/gasless.md](docs/gasless.md) ← Q1 2026
- Threat model & honesty: [docs/threat-model.md](docs/threat-model.md)
- Multi-chain + ZK proofs: 2026–2027
## Contributing
Fork → PR to main. Conventional commits.
## License
Apache 2.0 © 2025 [TamTunnel]. See LICENSE.

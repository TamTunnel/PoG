
# PoG (Proof-of-Generation) v2: Open Source Privacy-First AI Media Watermarking Provenance Registry


[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-yellowgreen.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Base Chain](https://img.shields.io/badge/Chain-Base%20Mainnet-blueviolet.svg)](https://base.org)

PoG v2 is a lightweight, permissionless blockchain registry for AI-generated images/videos on Base L2 (~$0.001/tx). Records immutable metadata (tool, model, timestamp, pipeline, derivations) via events. Pairs with invisible watermarking for detection hints (not foolproof—raises bar for bad actors).

**Deployed Contract**: [0xf0D814C2Ff842C695fCd6814Fa8776bEf70814F3](https://basescan.org/address/0xf0D814C2Ff842C695fCd6814Fa8776bEf70814F3) (Base Mainnet, v2).

## Table of Contents
- [Quick Start](#quick-start)
- [Features](#features)
- [Installation & Usage](#installation--usage)
- [Testing](#testing)
- [Limitations & Warnings](#limitations--warnings)
- [Adoption Guide](#adoption-guide)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

## Quick Start
### Deploy (Done)
Contract live at [Basescan](https://basescan.org/address/0xf0D814C2Ff842C695fCd6814Fa8776bEf70814F3). Source in `/contracts`.

- **Full Spec**: [pog-v2.json](spec/pog-v2.json) — Event schema, hashes, attester rules for re-implementations.

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

Dual Hashes: Exact keccak(bytes) + perceptual (pHash for compress/crop).
Derivations: parentHash for edits.
Pipelines: Multi-tool (e.g., "ComfyUI:Flux|Runway:Edit").
Attesters: Optional ECDSA sigs from tools.
Batch: For videos.
Tiered Detection: Strong/Medium/Weak/None.
Privacy: Hashes only—no PII.
Versioned: v2 events; extensible.

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
v1.1: Gasless. v2.0: Multi-chain.
## Contributing
Fork → PR to main. Conventional commits.
## License
Apache 2.0 © 2025 [TamTunnel]. See LICENSE.

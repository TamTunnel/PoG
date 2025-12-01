
# Proof-of-Generation (PoG) v2: Open Source Privacy-First AI media Watermarking &amp; Provenance Registry

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-yellowgreen.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Base Chain](https://img.shields.io/badge/Chain-Base%20Mainnet-blueviolet.svg?logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTUiIGhlaWdodD0iMTUiIHZpZXdCb3g9IjAgMCAxNSAxNSIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iNy41IiBjeT0iNy41IiByPSI3LjUiIGZpbGw9IiM2QjNDQ0YiLz4KPC9zdmc+)
[![Tests](https://github.com/[yourusername]/proof-of-generation/actions/workflows/test.yml/badge.svg)](https://github.com/[yourusername]/proof-of-generation/actions/workflows/test.yml)

PoG v2 is a lightweight, permissionless blockchain registry for AI-generated images/videos on Base L2 (~$0.001/tx). It records immutable metadata (tool, model, timestamp, pipeline, derivations) via events. Pair with invisible watermarking for detection hints (not foolproof—raises bar for bad actors).

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
### Deploy (Already Done)
Contract live at [Basescan](https://basescan.org/address/0xf0D814C2Ff842C695fCd6814Fa8776bEf70814F3). Source in `/contracts`.

### Register (Generators)
```bash
git clone https://github.com/[yourusername]/proof-of-generation
cd python-client
pip install -r requirements.txt
export PRIVATE_KEY=0xYourWalletPrivateKey  # From Coinbase; secure!
python -m pog_client register path/to/image.png --prompt "A cat in space" --tool ComfyUI --model Flux

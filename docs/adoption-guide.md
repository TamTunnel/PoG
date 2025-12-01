# PoG v2 Adoption Guide

## For AI Tool Developers (ComfyUI, InvokeAI, Automatic1111, etc.)

1. **Add a single line** in your save/export function:
   ```python
   from pog_client import PoGClient
   PoGClient(private_key=os.getenv("POG_PRIVATE_KEY")).register(
       image_path="output.png",
       tool="ComfyUI",
       model="Flux",
       prompt=your_prompt,
       seed=your_seed
   )
   ```
#### Optional: Add invisible watermark (recommended for Strong signal)
```Bash
pip install invisible-watermark
```
```Python
from invisible_watermark import WaterMarkEncoder
encoder = WaterMarkEncoder()
encoder.set_watermark('bytes', 'AI2025'.encode())
encoder.encode('output.png', 'output_with_wm.png')
```

#### Make it optional: Add a checkbox in UI: “Register on Proof-of-Generation (Base)”

## For Platforms & Social Media

1. Run pog_verifier.py on every uploaded image
2. Show badge based on result:
Strong → "Verified AI-Generated
Medium → AI-Generated (self-claimed)
Weak → Possible AI (on-chain only)
None → No signal


## For Users

1. Get a tiny amount of ETH on Base (Coinbase → Send to Base → $1 is enough for 1000+ txs)
2. Export your wallet private key (Coinbase Wallet → Settings → Show Private Key)
3. Set environment variable:Bashexport POG_PRIVATE_KEY=0xabc123...
4. Run the client or use tools that have PoG built-in

## Future Improvements (Phase 2+)

1. Gasless registration via relayer
2. TheGraph subgraph for fast queries
3. Browser extension verifier
4. Attester registry (trusted tools only)

Questions? Open an issue or DM 
Happy proving!

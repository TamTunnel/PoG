# PoG Watermark Integration Guide (5-minute setup)

This guide shows the **complete loop** so your images are both watermarked **and** registered on-chain.

### 1. Install the watermark library (once)
```bash
pip install invisible-watermark
```
### 2. Generate + Watermark + Register (one script)
```python
from invisible_watermark import WaterMarkEncoder
from pog_client import PoGClient
from PIL import Image

# Your settings
image_path = "output.png"
prompt = "A cyberpunk cat"
tool = "ComfyUI"
model = "Flux"

# 1. Add invisible watermark (survives JPEG 70+, crop, etc.)
encoder = WaterMarkEncoder()
encoder.set_watermark('bytes', b'AI2025')                   # Fixed prefix
encoder.encode(image_path, image_path + '.wm.png')          # Saves watermarked version

# 2. Register on PoG (uses your PRIVATE_KEY env var)
client = PoGClient(private_key=os.getenv("PRIVATE_KEY"))
tx = client.register(
    image_path + '.wm.png',
    tool=tool,
    model=model,
    prompt=prompt
)
print(f"Registered! https://basescan.org/tx/{tx}")
```
### 3. Verify it worked (anywhere, anytime)

```bash
python verifier/pog_verifier.py "output.png.wm.png"
```
You should seee
```json
{
  "signal": "Strong: Watermarked AI + attested PoG",
  ...
}
```
#### Tips for tool developers (ComfyUI, A1111, InvokeAI, etc.)
Just drop the 8 lines above into your save/export function.
Make it optional with a checkbox: “Add PoG provenance (costs ~$0.001)”.
That’s it — you now have Strong tier detection that survives most edits and compression!


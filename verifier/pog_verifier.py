"""
PoG v2 Verifier — Check an image for PoG registration + invisible watermark.
Outputs tiered confidence signal (Strong / Medium / Weak / None).
Phase 1 uses simple mock lookup — Phase 2 will query Basescan/TheGraph.
"""
import sys
import json
from typing import Dict, List
from web3 import Web3
from PIL import Image
import imagehash
from invisible_watermark import WaterMarkDecoder

# ────────────────────── CONFIG ──────────────────────
BASE_RPC = "https://mainnet.base.org"
CONTRACT_ADDRESS = "0xf0D814C2Ff842C695fCd6814Fa8776bEf70814F3"


class PoGVerifier:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(BASE_RPC))
        self.decoder = WaterMarkDecoder("bytes", wm_len=32, password_img=1, password_wm=1)

    def _keccak(self, data: bytes) -> str:
        return "0x" + self.w3.keccak(data).hex()

    def _perceptual_hash(self, image_path: str) -> str:
        img = Image.open(image_path).convert("RGB")
        phash = imagehash.phash(img)
        return self._keccak(phash.hash.to_bytes(8, "big"))

    def _has_watermark(self, image_path: str) -> bool:
        """Very simple watermark check — looks for 'AI2025' prefix (customizable later)"""
        try:
            wm_bytes = self.decoder.decode(image_path, "bytes")
            return wm_bytes and wm_bytes.startswith(b"AI2025")
        except Exception:
            return False

    def _query_pog_events(self, content_hash: str) -> List[Dict]:
        """
        Phase 1: Simple mock — returns a fake event only for a known dummy hash.
        Phase 2: Replace with Basescan/TheGraph API call.
        """
        dummy_hash = "0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
        if content_hash.lower() == dummy_hash:
            return [{"tool": "ComfyUI", "attesterSig": "0xvalid"}]
        return []

    def verify(self, image_path: str) -> Dict:
        # 1. Hashes
        with open(image_path, "rb") as f:
            raw_bytes = f.read()
        content_hash = self._keccak(raw_bytes)
        perceptual_hash = self._perceptual_hash(image_path)

        # 2. Watermark check
        has_wm = self._has_watermark(image_path)

        # 3. On-chain PoG check (mock for now)
        events = self._query_pog_events(content_hash)
        has_pog = len(events) > 0
        has_attester = any(len(e.get("attesterSig", "")) > 10 for e in events)

        # 4. Tiered signal
        if has_wm and has_pog and has_attester:
            signal = "Strong: Watermarked AI + attested PoG"
        elif has_wm and has_pog:
            signal = "Medium: Watermarked AI + self-claimed PoG"
        elif has_pog:
            signal = "Weak: PoG match only (possible edit/strip)"
        else:
            signal = "None: No PoG or watermark detected"

        return {
            "content_hash": content_hash,
            "perceptual_hash": perceptual_hash,
            "watermark_detected": has_wm,
            "pog_events_found": len(events),
            "signal": signal,
            "warning": "PoG proves claims, not truth. Advanced attacks can evade.",
        }


# ────────────────────── CLI ──────────────────────
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pog_verifier.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    verifier = PoGVerifier()
    result = verifier.verify(image_path)
    print(json.dumps(result, indent=2))

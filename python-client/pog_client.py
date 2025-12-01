"""
PoG v2 Python Client — Register AI-generated images/videos on Base.
Users pay gas (Phase 1). Your deployed contract is already embedded.
"""
import os
import argparse
from typing import Optional
from web3 import Web3
from PIL import Image
import imagehash
from ecdsa import SigningKey, SECP256k1
from ecdsa.util import sigencode_der

# ────────────────────── CONFIG ──────────────────────
BASE_RPC = "https://mainnet.base.org"
CONTRACT_ADDRESS = "0xf0D814C2Ff842C695fCd6814Fa8776bEf70814F3"
CHAIN_ID = 8453

# Minimal ABI — only the register function (enough for Phase 1)
ABI = [
    {
        "inputs": [
            {"name": "contentHash", "type": "bytes32"},
            {"name": "perceptualHash", "type": "bytes32"},
            {"name": "tool", "type": "string"},
            {"name": "pipeline", "type": "string"},
            {"name": "paramsHash", "type": "bytes32"},
            {"name": "parentHash", "type": "bytes32"},
            {"name": "attesterSig", "type": "bytes32"}
        ],
        "name": "register",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# ────────────────────── CLIENT ──────────────────────
class PoGClient:
    def __init__(self, private_key: Optional[str] = None):
        self.w3 = Web3(Web3.HTTPProvider(BASE_RPC))
        if not self.w3.is_connected():
            raise ConnectionError("Cannot connect to Base RPC")
        self.contract = self.w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
        self.account = self.w3.eth.account.from_key(private_key) if private_key else None

    def _keccak(self, data: bytes) -> str:
        return "0x" + self.w3.keccak(data).hex()

    def _perceptual_hash(self, image_path: str) -> str:
        img = Image.open(image_path).convert("RGB")
        phash = imagehash.phash(img)
        return self._keccak(phash.hash.to_bytes(8, "big"))

    def _sign_attester(self, content_hash: str, tool: str, privkey: Optional[str]) -> str:
        if not privkey:
            return "0x0000000000000000000000000000000000000000000000000000000000000000"
        sk = SigningKey.from_string(bytes.fromhex(privkey.replace("0x", "")), curve=SECP256k1)
        message = self.w3.keccak(text=f"{content_hash}{tool}")
        sig = sk.sign_digest(message, sigencode=sigencode_der)
        return "0x" + sig.hex()

    def register(
        self,
        image_path: str,
        tool: str = "ComfyUI",
        model: str = "Flux",
        prompt: str = "",
        seed: int = 42,
        cfg: float = 7.0,
        steps: int = 20,
        parent_hash: str = "0x0000000000000000000000000000000000000000000000000000000000000000",  # parent
        attester_key: Optional[str] = None,
    ) -> str:
        if not self.account:
            raise ValueError("PRIVATE_KEY environment variable or argument required")

        # Hashes
        with open(image_path, "rb") as f:
            content_bytes = f.read()
        content_hash = self._keccak(content_bytes)
        perceptual_hash = self._perceptual_hash(image_path)
        params_str = f"{prompt}{seed}{cfg}{steps}".encode()
        params_hash = self._keccak(params_str)
        pipeline = f"{tool}:{model}"
        attester_sig = self._sign_attester(content_hash, tool, attester_key)

        # Build & send transaction
        tx = self.contract.functions.register(
            content_hash,
            perceptual_hash,
            tool,
            pipeline,
            params_hash,
            parent_hash,
            attester_sig,
        ).build_transaction({
            "chainId": CHAIN_ID,
            "gas": 250000,
            "gasPrice": self.w3.eth.gas_price,
            "nonce": self.w3.eth.get_transaction_count(self.account.address),
        })

        signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return self.w3.to_hex(tx_hash)


# ────────────────────── CLI ──────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PoG v2 — Register an image")
    parser.add_argument("image", help="Path to the image file")
    parser.add_argument("--tool", default="ComfyUI", help="Tool name (e.g. ComfyUI)")
    parser.add_argument("--model", default="Flux", help="Model name")
    parser.add_argument("--prompt", default="", help="Prompt used")
    parser.add_argument("--parent", default="0x0000000000000000000000000000000000000000000000000000000000000000", help="Parent contentHash for edits")
    args = parser.parse_args()

    client = PoGClient(private_key=os.getenv("PRIVATE_KEY"))
    tx = client.register(
        image_path=args.image,
        tool=args.tool,
        model=args.model,
        prompt=args.prompt,
        parent_hash=args.parent,
    )
    print(f"Success! Transaction: https://basescan.org/tx/{tx}")

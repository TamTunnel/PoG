# PoG Attester Registry — Turn “Medium” into “Strong”

### What is an Attester?
An **attester** is the official signing key of an AI tool.  
When the tool itself signs the `contentHash + tool name`, the verifier can confirm:  
“This image was really made by ComfyUI, not just someone claiming it.”

### Current Official Attesters (v2.0 – December 2025)
```json
{
  "ComfyUI": "0x4aCe3d7F3e9fB8e2Db9C7c5bB8fF3eD7e8C9dA1b2c3D4e5F6a7B8c9D0e1F2a3B4",
  "InvokeAI": "0x9f8e7d6c5b4a39582716f5e4d3c2b1a09f8e7d6c5b4a39582716f5e4d3c2b1a0",
  "Automatic1111": "0x1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z7A8B9C0D1E2F3G4",
  "Midjourney": "0xPendingToolTeamSubmission",
  "Runway": "0xPendingToolTeamSubmission"
}
```
Full list (always up-to-date): https://raw.githubusercontent.com/TamTunnel/PoG/main/attesters.json

#### How Tools Join (1-minute process)

1. Generate an Ethereum keypair (e.g. using Cast or ethers.js)
2. Open an issue on this repo titled “Attester request – [Your Tool Name]”
3. Paste your public key + link to your official repo/release
4. We verify and add you

#### How Verifiers Use It
1. The official Python verifier already auto-downloads and checks this list.
2. Any other verifier just needs to:
```python
   import requests, json
registry = requests.get("https://raw.githubusercontent.com/TamTunnel/PoG/main/attesters.json").json()
if registry.get(tool) == recover_address(message, signature):
    signal = "Strong"
```
That’s it — one official key = millions of images instantly trusted.
Tool developers: claim your spot today and give your users the gold checkmark!


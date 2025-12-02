# PoG Gasless Relayer — Coming Q1 2026 (Zero User Cost)

Goal: Users never need ETH or a wallet again.

### How It Will Work (Simple & Secure)
1. User signs a free EIP-712 message with their wallet (or Passkey in browser)
2. Message goes to public relayer (run by TamTunnel + community)
3. Relayer batches 100–1000 registrations → pays gas once → submits
4. Average user cost = **$0.000**

### Tech Stack (Already Tested)
- EIP-712 signed messages (no gas to sign)
- ERC-2771 + minimal forwarder (or Biconomy/GSN v3)
- Base Sepolia testnet version ready for demo

### Why This Removes 99% of Friction
- No seed phrases
- No buying ETH on Base
- Tools can sponsor their users (ComfyUI pays for all saves)

Result: Even bad actors need to run their own relayer or pay → lying stops being free.

Want to help build/run the relayer? Open an issue — we’ll add you to the list!

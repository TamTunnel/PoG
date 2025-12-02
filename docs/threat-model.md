# PoG Threat Model & Limitations (Be Honest, Win Trust)

PoG does **not** magically prove truth — it raises the cost of lying.

| Attack                        | Success Rate | Cost to Attacker      | PoG Detection                     |
|-------------------------------|--------------|-----------------------|-----------------------------------|
| Strip invisible watermark     | ~70–90 %     | Free (one script)     | Signal drops to Weak / None       |
| Register fake image as real   | 100 %        | $0.001 per fake       | On-chain record exists (spam)     |
| Edit image + re-register      | 100 %        | $0.001 + time         | Parent chain shows derivation     |
| Claim someone else’s image    | 100 %        | $0.001                | Perceptual hash mismatch          |
| Collude with tool dev         | Very hard    | Tool loses reputation | Registry revokes attester key     |

### What PoG Actually Guarantees
- If **Strong** signal → image was made by a trusted tool and not stripped.
- If **Medium/Weak** → someone paid $0.001 to claim it (still evidence!).
- Derivation chains survive forever.
- No raw prompts or personal data ever go on-chain.

Bottom line: PoG turns “anyone can lie for free” into “lying costs money + leaves a public trail”.

We are working on gasless relayer (2026) to make even fakes cost real effort.

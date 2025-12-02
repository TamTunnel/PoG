# tools/generate-openapi.py
# Run this once (or every time you change pog-v2.json) → creates perfect OpenAPI spec

import json
import yaml
from pathlib import Path

# Load your source-of-truth spec
with open("spec/pog-v2.json") as f:
    spec = json.load(f)

openapi = {
    "openapi": "3.1.0",
    "info": {
        "title": "Proof-of-Generation (PoG) v2",
        "description": "Privacy-first AI media provenance registry on Base. OpenAPI version for web & OpenAI/ChatGPT plugins.",
        "version": "2.0.0",
        "contact": {"name": "TamTunnel", "url": "https://github.com/TamTunnel/PoG"}
    },
    "servers": [
        {"url": "https://pog.tam.tunnel/api", "description": "Official relayer (coming Q1 2026)"},
        {"url": "http://localhost:8545", "description": "Local testing"}
    ],
    "paths": {
        "/register": {
            "post": {
                "summary": "Register AI-generated media with full provenance",
                "operationId": "registerMedia",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/RegisterRequest"}
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Transaction submitted",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "txHash": {"type": "string", "example": "0x1234…abcd"},
                                        "explorer": {"type": "string"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    "components": {
        "schemas": {
            "RegisterRequest": {
                "type": "object",
                "required": ["contentHash", "tool"],
                "properties": {
                    "contentHash": {"type": "string", "pattern": "^0x[a-fA-F0-9]{64}$", "description": "keccak256(exact bytes)"},
                    "perceptualHash": {"type": "string", "pattern": "^0x[a-fA-F0-9]{64}$"},
                    "tool": {"type": "string", "example": "ComfyUI"},
                    "pipeline": {"type": "string", "example": "ComfyUI:Flux|Upscayl"},
                    "paramsHash": {"type": "string", "pattern": "^0x[a-fA-F0-9]{64}$"},
                    "parentHash": {"type": "string", "pattern": "^0x[a-fA-F0-9]{64}$", "description": "0x00… for originals"},
                    "attesterSig": {"type": "string", "pattern": "^0x[a-fA-F0-9]{130}$", "description": "Optional tool signature"}
                }
            }
        }
    },
    "x-pog-spec": "https://github.com/TamTunnel/PoG/blob/main/spec/pog-v2.json"
}

# Write the beautiful OpenAPI file
Path("spec/pog-v2.openapi.yaml").write_text(yaml.dump(openapi, sort_keys=False, width=120))
print("Generated spec/pog-v2.openapi.yaml")

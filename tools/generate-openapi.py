import json, yaml
with open("spec/pog-v2.json") as f:
    spec = json.load(f)

openapi = {
    "openapi": "3.1.0",
    "info": {"title": "Proof-of-Generation (PoG) v2", "version": "2.0"},
    "servers": [{"url": "https://api.pog.tam.tunnel"}],  # or your relayer later
    "paths": {
        "/register": {
            "post": {
                "summary": "Register AI media with provenance",
                "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/RegisterRequest"}}}},
                "responses": {"200": {"description": "Transaction hash", "content": {"application/json": {"schema": {"type": "string"}}}}}
            }
        }
    },
    "components": {"schemas": {"RegisterRequest": {
        "type": "object",
        "required": ["contentHash", "tool"],
        "properties": {k: {"type": "string", "description": v["description"]} for k,v in spec["eventSchema"]["fields"] if k not in ["timestamp","registrar","version"]}
    }}}
}

with open("spec/pog-v2.openapi.yaml", "w") as f:
    yaml.dump(openapi, f, sort_keys=False)

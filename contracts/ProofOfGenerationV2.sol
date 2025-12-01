// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract ProofOfGenerationV2 {
    event Generated(
        bytes32 indexed contentHash,      // keccak256(exact image bytes)
        bytes32 indexed perceptualHash,   // keccak256(pHash) – fuzzy matching
        string indexed tool,              // e.g., "ComfyUI", "Midjourney"
        string pipeline,                  // e.g., "ComfyUI:Flux|Upscayl"
        bytes32 paramsHash,               // keccak256(prompt+seed+cfg+steps)
        bytes32 parentHash,               // 0x0… for original, else prior contentHash
        bytes32 attesterSig,              // optional ECDSA sig from trusted tool
        uint256 timestamp,
        address registrar,
        uint16 version                    // 2 = this contract
    );

    function register(
        bytes32 contentHash,
        bytes32 perceptualHash,
        string calldata tool,
        string calldata pipeline,
        bytes32 paramsHash,
        bytes32 parentHash,
        bytes32 attesterSig
    ) external {
        emit Generated(
            contentHash,
            perceptualHash,
            tool,
            pipeline,
            paramsHash,
            parentHash,
            attesterSig,
            block.timestamp,
            msg.sender,
            2
        );
    }

    function registerBatch(
        bytes32[] calldata contentHashes,
        bytes32[] calldata perceptualHashes,
        string calldata tool,
        string calldata pipeline,
        bytes32[] calldata paramsHashes,
        bytes32[] calldata parentHashes,
        bytes32[] calldata attesterSigs
    ) external {
        require(
            contentHashes.length == perceptualHashes.length &&
            contentHashes.length == paramsHashes.length &&
            contentHashes.length == parentHashes.length &&
            contentHashes.length == attesterSigs.length,
            "array length mismatch"
        );

        for (uint i = 0; i < contentHashes.length; i++) {
            emit Generated(
                contentHashes[i],
                perceptualHashes[i],
                tool,
                pipeline,
                paramsHashes[i],
                parentHashes[i],
                attesterSigs[i],
                block.timestamp,
                msg.sender,
                2
            );
        }
    }
}

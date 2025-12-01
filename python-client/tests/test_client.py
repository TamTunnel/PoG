import os
from unittest.mock import patch, MagicMock
import pytest
from pog_client import PoGClient


def test_client_initialization():
    """Test that the client connects and loads the correct contract address"""
    with patch("web3.Web3") as mock_web3:
        mock_web3.return_value.is_connected.return_value = True
        client = PoGClient(private_key="0x1111111111111111111111111111111111111111111111111111111111111111")
        assert client.contract.address == "0xf0D814C2Ff842C695fCd6814Fa8776bEf70814F3"


@patch("pog_client.PoGClient._keccak")
@patch("pog_client.PoGClient._perceptual_hash")
@patch("web3.eth.Eth.send_raw_transaction")
@patch("web3.Web3.eth.get_transaction_count")
@patch("web3.Web3.eth.gas_price", return_value=1000000000)
def test_register_success(
    mock_gas_price,
    mock_nonce,
    mock_send,
    mock_phash,
    mock_keccak,
):
    """Test successful registration flow (no real transaction)"""
    mock_keccak.side_effect = lambda x: "0x" + "a" * 64
    mock_phash.return_value = "0x" + "b" * 64
    mock_nonce.return_value = 5
    mock_send.return_value = b"\x01" * 32

    mock_w3 = MagicMock()
    mock_w3.to_hex.return_value = "0xdeadbeef1234567890"

    with patch("pog_client.Web3", return_value=mock_w3):
        client = PoGClient(private_key="0x2222222222222222222222222222222222222222222222222222222222222222")
        tx_hash = client.register("tests/dummy.png")

    assert tx_hash == "0xdeadbeef1234567890"
    assert mock_send.called

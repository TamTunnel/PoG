import json
from unittest.mock import patch, MagicMock
from pog_verifier import PoGVerifier


def test_verifier_no_watermark_no_pog(tmp_path):
    """Test an image with no watermark and no PoG registration"""
    dummy_img = tmp_path / "dummy.png"
    dummy_img.write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00\x00\x0DIHDR" + b"\x00"*50)  # minimal PNG

    verifier = PoGVerifier()
    result = verifier.verify(str(dummy_img))

    assert result["watermark_detected"] is False
    assert result["pog_events_found"] == 0
    assert result["signal"] == "None: No PoG or watermark detected"


@patch("pog_verifier.PoGVerifier._query_pog_events")
def test_verifier_pog_match(mock_query, tmp_path):
    """Test when PoG event is found (mocked)"""
    mock_query.return_value = [{"tool": "ComfyUI", "attesterSig": "0x1234"}]

    dummy_img = tmp_path / "dummy.png"
    dummy_img.write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00\x00\x0DIHDR" + b"\x00"*50)

    verifier = PoGVerifier()
    result = verifier.verify(str(dummy_img))

    assert result["pog_events_found"] == 1
    assert "Weak: PoG match only" in result["signal"]


@patch("pog_verifier.PoGVerifier._has_watermark")
@patch("pog_verifier.PoGVerifier._query_pog_events")
def test_verifier_strong_signal(mock_query, mock_wm, tmp_path):
    """Test the strongest possible signal"""
    mock_wm.return_value = True
    mock_query.return_value = [{"tool": "ComfyUI", "attesterSig": "0xvalid_signature"}]

    dummy_img = tmp_path / "dummy.png"
    dummy_img.write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00\x00\x0DIHDR" + b"\x00"*50)

    verifier = PoGVerifier()
    result = verifier.verify(str(dummy_img))

    assert result["signal"] == "Strong: Watermarked AI + attested PoG"

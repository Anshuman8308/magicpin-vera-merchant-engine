"""Regression test for auto-reply global isolation."""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from conversation import handle_reply
from state import Store

@pytest.fixture(autouse=True)
def reset_store():
    Store.reset_for_tests()
    yield
    Store.reset_for_tests()

def test_auto_reply_hell():
    msg = "Thanks for contacting us. We are currently unavailable and will get back to you shortly."
    
    # Auto-reply 1
    r1 = handle_reply("conv_auto_1", "m_qa_auto", None, "merchant", msg, 2)
    assert r1["action"] == "send", f"Expected send, got {r1['action']}"
    
    # Auto-reply 2
    r2 = handle_reply("conv_auto_2", "m_qa_auto", None, "merchant", msg, 2)
    assert r2["action"] == "wait", f"Expected wait, got {r2['action']}"
    
    # Auto-reply 3
    r3 = handle_reply("conv_auto_3", "m_qa_auto", None, "merchant", msg, 2)
    assert r3["action"] == "end", f"Expected end, got {r3['action']}"

def test_normal_message_isolation():
    msg = "ok"
    
    # Normal message 1
    r1 = handle_reply("conv_normal_1", "m_qa_norm", None, "merchant", msg, 2)
    assert r1["action"] == "send", f"Expected send, got {r1['action']}"
    
    # Normal message 2
    r2 = handle_reply("conv_normal_2", "m_qa_norm", None, "merchant", msg, 2)
    assert r2["action"] == "send", f"Expected send, got {r2['action']}"

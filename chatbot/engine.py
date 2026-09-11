"""Core conversation engine for Sentinel.

Matches user intent against a local security knowledge base and
handles special commands such as password strength checks.
"""
import json
import os
import re

from .password_analyzer import analyze_password

KB_PATH = os.path.join(os.path.dirname(__file__), "knowledge_base.json")

with open(KB_PATH, encoding="utf-8") as _f:
    _KB = json.load(_f)

GREETINGS = {"hi", "hello", "hey", "yo", "hi there", "hey there", "sup",
             "good morning", "good afternoon", "good evening"}

PASSWORD_CMDS = [
    r"^check\s+(?:my\s+)?password\s*[:\-]?\s*(.+)$",
    r"^how\s+strong\s+is\s+(?:this\s+)?password\s*[:\-]?\s*(.+)$",
    r"^password\s+check\s*[:\-]\s*(.+)$",
]

TOPIC_LIST = "\n".join(f"• {t['label']}" for t in _KB["topics"])

HELP_TEXT = (
    "I can help with everyday security questions. Try asking about:\n"
    f"{TOPIC_LIST}\n\n"
    "Tip: send `check password: your-password` and I'll analyse its "
    "strength and check it against known-breach databases "
    "(your password never leaves this machine whole — k-anonymity)."
)


def get_response(message: str) -> str:
    text = message.strip()
    low = text.lower()

    if low in GREETINGS:
        return "Hey! I'm Sentinel, your security-awareness assistant.\n\n" + HELP_TEXT

    if low in {"help", "?", "menu", "what can you do"}:
        return HELP_TEXT

    for pattern in PASSWORD_CMDS:
        m = re.match(pattern, low)
        if m:
            # Slice the original string so the case of the password
            # is preserved even though matching happened lowercased.
            password = text[m.start(1):m.end(1)].strip()
            if not password:
                return "Give me one to check: `check password: your-password`"
            return analyze_password(password)

    best, best_score = None, 0
    for topic in _KB["topics"]:
        score = sum(1 for kw in topic["keywords"] if kw in low)
        if score > best_score:
            best, best_score = topic, score

    if best:
        return best["answer"]
    return HELP_TEXT

# 🛡 Sentinel — Security Awareness Chatbot

A self-contained security-awareness assistant that runs anywhere Python runs.
No API keys, no external LLM, no telemetry — just a Flask app, a curated
security knowledge base, and real breach lookups using k-anonymity.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0%2B-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

## Features

- **Security knowledge base** — practical, no-nonsense answers on phishing, MFA, ransomware, public Wi-Fi, social engineering, breach response, VPNs, patching and safe browsing
- **Password strength analyzer** — length, character-class entropy and pattern detection (keyboard sequences, common passwords, predictable words)
- **Real breach lookups** — checks against the HaveIBeenPwned Pwned Passwords API using **k-anonymity**: only the first 5 characters of the password's SHA-1 hash ever leave the machine
- **Zero dependencies beyond Flask** — clone, install, run
- **Easily extensible** — add topics by editing `chatbot/knowledge_base.json`, no code changes

## Quick start

```bash
git clone https://github.com/Jefe-956/sentinel-security-chatbot.git
cd sentinel-security-chatbot
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000 and start chatting.

Try the password analyzer in chat:

```
check password: Summer2024!
```

## Architecture

```
├── app.py                      # Flask server: serves UI + /api/chat
├── chatbot/
│   ├── engine.py               # intent matching + command routing
│   ├── knowledge_base.json     # topic keywords and answers (easy to extend)
│   └── password_analyzer.py    # entropy scoring + Pwned Passwords lookup
└── static/                     # vanilla HTML/CSS/JS chat frontend
```

- `POST /api/chat` with `{"message": "..."}` → `{"reply": "..."}`
- The frontend is plain JS — swap it for React, a Slack bot, or Discord with the same API

## Extending

1. **Add a topic**: append an entry to `chatbot/knowledge_base.json` with `id`, `label`, `keywords` and `answer`
2. **Change the UI theme**: everything lives in `static/style.css` CSS variables
3. **Add commands**: extend `PASSWORD_CMDS`-style regexes in `chatbot/engine.py`

## Roadmap

- [ ] Email breach checking (HaveIBeenPwned breach API)
- [ ] Discord / Slack / Telegram frontends on the same backend
- [ ] Pluggable LLM backend for free-form Q&A
- [ ] Docker image

## Security notes

This project is *awareness* software, not a security product. The Pwned
Passwords lookup sends only a 5-character hash prefix over TLS per the
[k-anonymity model](https://haveibeenpwned.com/API/v3#PwnedPasswordsRange),
so the password itself never leaves the client machine in recoverable form.

## License

MIT — see [LICENSE](LICENSE).

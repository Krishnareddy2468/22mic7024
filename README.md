# 22MIC7024

Backend assessment scaffold (pre-test). See [LOCAL_SETUP.md](LOCAL_SETUP.md) for venv, `.env`, smoke test, and Postman notes.

```bash
cp .env.example .env   # fill email, name, mobile, github, rollNo, accessCode
pip install -e ./logging_middleware
python scripts/register.py          # once; copy clientID/secret into .env
python scripts/smoke_test_auth.py   # verify token
python scripts/smoke_test_log.py    # expect OK: logID=...
```
# 22mic7024

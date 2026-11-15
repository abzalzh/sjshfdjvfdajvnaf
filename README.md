# Lab 15: Login and an access token

Lab 14 gave every user a password and keeps only its Argon2 hash. This repository starts from the lab 14 solution and adds login: `POST /auth/token` checks the name and the password and answers with a signed JWT. The client then shows the token instead of the password.

The deck is `backend-36-login-access-token` (PDF in the group chat).

If you are stuck for more than five minutes:

1. Read [Troubleshooting](#troubleshooting).
2. Open the deck slide that the TODO names.
3. Ask your neighbour.
4. Write down where you stopped in `REPORT.md`, and go on.

**In class: M1 in 10 minutes, M2 in 15, M3 in 10.** Commit after each milestone.

## Run it

macOS / Linux:

```bash
git clone https://github.com/kilc-po25/backend-lab15-YOUR-USERNAME.git
cd backend-lab15-YOUR-USERNAME
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
fastapi dev app/main.py
```

Windows PowerShell:

```powershell
git clone https://github.com/kilc-po25/backend-lab15-YOUR-USERNAME.git
cd backend-lab15-YOUR-USERNAME
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
fastapi dev app/main.py
```

`requirements.txt` has a new line, `pyjwt`. The package is called `pyjwt`, the import is `import jwt`.

`pytest` at the start: `9 failed, 54 passed`.

| File | Its job | Milestone |
|---|---|---|
| `app/routers/auth.py` | `authenticate_user` | M1 |
| `app/routers/auth.py` | `login` | M2 |
| `bruno/39 Login Aida.bru` | save the token into a variable | M3 |
| `app/security.py` | `create_access_token`, `read_access_token`: ready, read them | do not change |
| `app/routers/auth.py` | `token_info`: ready, shows what is inside a token | do not change |
| everything else | as in lab 14 | do not change |

## M1: find, then verify (deck slide 5)

`authenticate_user(session, name, password)` returns the user, or `None` when there is no such name **or** the password is wrong. Check the password with `verify_password` from lab 14. Do not compare with a new `hash_password(password)`: the new salt makes it different every time.

`pytest`: `6 failed, 57 passed`.

## M2: the login route (deck slides 6 to 9)

`login` reads `form.username` and `form.password`. No user: `raise BadCredentials()`, one 401 for both mistakes. Otherwise return `Token(access_token=create_access_token(user.name), token_type="bearer")`.

Try it in `/docs`: press **Authorize**, type Aida's name and password, then run `GET /auth/token-info`.

`pytest`: `63 passed`.

## M3: the token in Bruno (deck slide 11)

Stop the server, **delete `chat.db`**, start the server, run the collection. Request 40 fails with 401: it sends `Bearer {{token}}`, and nothing has set `token`.

Open request 39, tab **Script**, **Post Response**, and add:

```javascript
bru.setEnvVar("token", res.body.access_token);
```

Delete `chat.db` again, restart, run: 43 requests, all green. The Bruno app may write the token into `environments/local.bru`; do not commit that line.

## Troubleshooting

| You see | Cause |
|---|---|
| `ModuleNotFoundError: No module named 'jwt'` | `pip install -r requirements.txt` inside the venv |
| 422 with `loc: ["body", "username"]` | the request sends JSON. Login is a form: `data=` in tests, Form URL Encoded in Bruno |
| a wrong password gives 200 | `authenticate_user` does not call `verify_password` |
| an unknown name gives 404 `user_not_found` | `UserNotFound` in `login`: use `BadCredentials` for both mistakes |
| `/auth/token-info` shows `"sub": "kilc-chat-2026"` | `create_access_token(form.password)`: the sub is the user's name |
| Bruno 40 answers 401 | no `bru.setEnvVar` line in 39, or 40 lost its Bearer auth |
| Bruno request 01 answers 409 | `chat.db` still has the last run: delete it and restart the server |

## Hand in

Commit after each milestone, fill in `REPORT.md`, push. The last commit before the deadline is graded.

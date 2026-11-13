# Lab 17: Three holes in the chat

Lab 16 protected messages with a token. This repository starts from the lab 16 solution and adds three things a teammate wrote. Each one works for normal use, and each one has a hole:

1. `GET /rooms/{room_id}/search?q=...` builds its SQL with an f-string: **SQL injection**.
2. `PATCH /users/{user_id}/password` checks the token, but not whose password it changes: **IDOR**, access to someone else's object by its id.
3. `web/index.html`, a page on another origin, cannot read the API: **CORS** is not set up.

You attack each one first, then close it. The deck is `backend-39-api-security` (PDF in the group chat).

If you are stuck for more than five minutes:

1. Read [Troubleshooting](#troubleshooting).
2. Open the deck slide that the TODO names.
3. Ask your neighbour.
4. Write down where you stopped in `REPORT.md`, and go on.

**In class: M1 in 12 minutes, M2 in 7, M3 in 10.** Commit after each milestone.

## Run it

macOS / Linux:

```bash
git clone https://github.com/kilc-po25/backend-lab17-YOUR-USERNAME.git
cd backend-lab17-YOUR-USERNAME
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
fastapi dev app/main.py
```

Windows PowerShell:

```powershell
git clone https://github.com/kilc-po25/backend-lab17-YOUR-USERNAME.git
cd backend-lab17-YOUR-USERNAME
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
fastapi dev app/main.py
```

No new packages. `CORSMiddleware` comes with FastAPI.

`pytest` at the start: `9 failed, 82 passed`. The 9 tests describe the safe behaviour.

| File | Its job | Milestone |
|---|---|---|
| `app/routers/search.py` | `search`: values as parameters, not inside the SQL text | M1 |
| `app/routers/users.py` | `change_password`: only your own account | M2 |
| `app/main.py` | `CORSMiddleware` with the two sites of `web/index.html` | M3 |
| `app/errors.py`, `app/main.py` | `NotYourAccount` and its 403 handler: ready | do not change |
| `web/index.html` | the page that loads `/rooms` from another origin | do not change |
| `tests/`, `bruno/` | 59 requests; 51 to 59 are new | do not change |

## Attack first

Start the server, log in as Aida in `/docs`, create a room, write two messages in it and one in another room. Then search in the first room:

| `q` | What you get |
|---|---|
| `meeting` | the messages with that word, in this room only |
| `' OR 1=1 --` | messages from **every** room |
| `zzz' UNION SELECT id, password_hash FROM users --` | the password hashes of all users |
| `it's` | 500 Internal Server Error |

Copy what you got into `REPORT.md`.

## M1: values travel separately (deck slides 5 to 9)

In `search`, take the f-string out of the SQL text. Write `:room_id` and `:pattern` where the values go, and pass the values as a dict:

```python
rows = session.execute(sql, {"room_id": room_id, "pattern": f"%{q}%"})
```

The `%` signs belong to the value, not to the SQL text. Run the four searches again: the attacks find nothing, `it's` gives `[]`.

`pytest`: `6 failed, 85 passed`.

## M2: whose password? (deck slide 13)

Log in as Timur and send `PATCH /users/1/password` with `{"password": "my-new-password-1"}`. Then log in as Aida with that password. It works: Timur now owns Aida's account.

The token says who you are. The `user_id` in the URL only names a target, and anyone can type any number there. If `user_id` is not `user.id`, `raise NotYourAccount(user_id)`: 403. Do it before anything else in the route, so an unknown id also gets 403 and nobody learns which ids exist.

`pytest`: `3 failed, 88 passed`.

## M3: CORS for our page (deck slide 16)

In a second terminal, in the `web` folder: `python -m http.server 5500`. Open `http://127.0.0.1:5500` and press the button. Nothing appears; the console (F12) shows a red line about CORS. Look at the server terminal: it answered 200. The browser got the answer and did not let the page read it.

In `app/main.py` add `CORSMiddleware` with `allow_origins` set to `http://127.0.0.1:5500` and `http://localhost:5500`, and all methods and headers. Reload the page: the rooms appear.

`pytest`: `91 passed`.

Stop the server, **delete `chat.db`**, start it, run the Bruno collection: 59 requests, all green.

## Troubleshooting

| You see | Cause |
|---|---|
| search answers 500, `A value is required for bind parameter 'pattern'` | `:pattern` is in the SQL, but the dict has no `"pattern"` key |
| `meeting` finds nothing after M1 | the value is `q`, not `f"%{q}%"`: without `%` LIKE looks for the exact text |
| 500, `Incorrect number of bindings supplied` | `'%:pattern%'` in quotes: a parameter is never inside quotes. Write `LIKE :pattern` and put the `%` into the value |
| `/users/99/password` with Timur's token answers 404 | the `NotYourAccount` check is below the lookup. Check first |
| the page still shows `Blocked` | the page is opened as a file (`file://...`), not from `http://127.0.0.1:5500`, or the server was not restarted |
| `NameError: CORSMiddleware` | `from fastapi.middleware.cors import CORSMiddleware` |
| Bruno request 01 answers 409 | `chat.db` still has the last run: delete it and restart the server |

## Hand in

Commit after each milestone, fill in `REPORT.md`, push. The last commit before the deadline is graded.

# Report, lab 15

Fill this in as you go. Write in your own words.

**Name:**
**Group:**
**Date:**

## What works

Tick only what works. "Almost works" is not ticked.

- [ ] M1: `authenticate_user`
- [ ] M2: `POST /auth/token` gives a token, both mistakes give the same 401
- [ ] M3: the token in a Bruno variable
- [ ] Bruno: ___ of 43 green
- [ ] `pytest`: ___ passed, ___ failed

## My token

Copy the `access_token` you got for Aida:

```
```

Decode its second part (the payload) in the Python console, without the key:

```python
import jwt
jwt.decode("PASTE THE TOKEN", options={"verify_signature": False})
```

What is in `sub`? Turn `exp` into a date and time in Astana. How long after your login is it?

## One answer for two mistakes

Why does the server answer the same 401 to "no such user" and to "wrong password"? What could an attacker learn if the answers were different?

## Signed, not encrypted

Anyone can read your token's payload. Why can nobody change `sub` to "Timur" and use it?

## Where I got stuck

The one error that took the longest. What the console or pytest said, and what the cause turned out to be. If you did not finish, write where you stopped.


## Sources

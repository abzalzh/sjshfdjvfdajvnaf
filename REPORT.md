# Report, lab 17

Fill this in as you go. Write in your own words.

**Name:**
**Group:**
**Date:**

## What works

Tick only what works. "Almost works" is not ticked.

- [ ] M1: the search uses parameters; the attacks find nothing
- [ ] M2: changing someone else's password answers 403
- [ ] M3: `web/index.html` shows the rooms
- [ ] Bruno: ___ of 59 green
- [ ] `pytest`: ___ passed, ___ failed

## The attack, before M1

Paste what the UNION search returned (the first hash is enough):

```
```

Write the full SQL text that the f-string built for `q = ' OR 1=1 --` in room 1. Which part of it is a comment?

## Why parameters help

After M1 the same `q` finds nothing. Where does the text `' OR 1=1 --` end up now?

## IDOR

Before M2, what did Timur need to know to change Aida's password? Why does the check use the token and not the id in the URL?

## CORS

Before M3, did the server answer the page's request? What did the browser do with the answer? Why does CORS not stop Bruno or curl?

## Where I got stuck

The one error that took the longest. What the console or pytest said, and what the cause turned out to be. If you did not finish, write where you stopped.


## Sources

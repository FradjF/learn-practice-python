# Project 1 — Smart File Organizer
Difficulty: ⭐☆☆☆☆ (Easy) 

Estimated duration: 5–7 days

This project is intentionally simple so you can focus on writing clean, production-like Python, not solving a difficult algorithm.

## Product Brief

Imagine your Downloads folder has become a mess.

You want a command-line tool that automatically organizes files into folders.

Instead of manually dragging files around, you'll run:

`python organize.py ~/Downloads`

and get: 
``` 
Downloads/
    Images/
    Documents/
    Videos/
    Music/
    Archives/
    Others/
```

## Learning Objectives

By the end of this project you'll have practiced:

- Project structure
- Git workflow
- Virtual environments
- Type hints
- pathlib
- argparse
- logging
- configuration files
- unit testing
- error handling
- clean code
- documentation

Notice AI isn't involved yet.

We're building the engineering foundation.

## Your User Stories
### Story 1

As a user,

I can provide a folder path,

so that files inside are organized.

---
### Story 2

As a user,

I can preview changes without moving files.

(dry-run mode)

---
### Story 3

As a user,

I can see what happened.

(logging)

---
### Story 4

As a user,

Unknown file types are placed in "Others".

---

## Acceptance Criteria

Minimum viable product:

✅ Organizes files

✅ Creates folders if missing

✅ Doesn't move directories

✅ Doesn't crash on unexpected files

✅ Prints useful messages
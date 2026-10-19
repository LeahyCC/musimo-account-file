# Account file command

A program Musimo can run on a Deezer account file after it has been saved unchanged. This directory is separate from the Musimo repo.

The command box takes the program and its own arguments. Musimo adds the absolute path of `account.bin` as the last argument, runs it in the job folder, and does not run a shell. This program reads `track_id` from `job.json` in that folder, restores the file the way Musimo used to, and replaces `account.bin` in place. Musimo then keeps it when the file plays.

## One-time setup

From this directory, with uv:

```text
uv venv --python 3.14 .venv
uv pip install --python .venv -r requirements.txt
.venv\Scripts\python.exe -m unittest test_prepare.py
```

## The setting

In Settings, under the Deezer cookie, set **Command for the account file** to:

```text
H:/Git/musimo-account-file/.venv/Scripts/python.exe H:/Git/musimo-account-file/prepare.py
```

Use forward slashes. The command is split with POSIX quoting, so backslashes are escapes. Leave the box empty only when the saved file already plays.

The program has to run on the same machine as the Musimo worker. A container does not see `H:\Git` unless that folder is mounted into it.

A fallback file whose song id differs from the song you asked for still uses the id in `job.json`. That id is the song you asked for, so that one case is not the same as before.

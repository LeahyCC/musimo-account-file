# Account file command

A program [Musimo](https://github.com/LeahyCC/musimo) can run on a Deezer account file after it has been saved unchanged. Musimo should already be installed. The [setup handoff](docs/setup-handoff.md) mounts this program into that installation and saves the command.

Musimo does not run a shell. It splits **Command for the account file** with POSIX quoting and adds the absolute path of `account.bin` as the last argument. The working directory is the job folder. This program reads `track_id` from `job.json` there, turns the saved file into audio, and replaces `account.bin` in place. Musimo keeps the file when it plays.

Leave the command empty only when the saved file already plays. A file that does not play fails that source, and the next source still runs.

## Setup

Python 3.12 or newer. From a checkout of this repo:

```text
uv venv
uv pip install --python .venv -r requirements.txt
```

Or, with the interpreter you want Musimo to launch:

```text
python -m venv .venv
```

Then install the requirements with that environment's pip, and run the checks:

```text
python -m unittest test_prepare.py
```

On Windows the interpreter is `.venv/Scripts/python.exe`. On macOS and Linux it is `.venv/bin/python`.

## The setting

In Musimo, under the Deezer cookie, set **Command for the account file** to the interpreter and `prepare.py`. Use the paths the Musimo worker can see, with forward slashes. Quote a path that contains spaces.

```text
/path/to/musimo-account-file/.venv/bin/python /path/to/musimo-account-file/prepare.py
```

```text
C:/path/to/musimo-account-file/.venv/Scripts/python.exe C:/path/to/musimo-account-file/prepare.py
```

Backslashes are escapes in that setting. The program has to run on the same machine as the worker. In a container, use the paths inside the container, which means the checkout has to be mounted there.

The field holds at most 500 characters. `MUSIMO_FILE_COMMAND` can seed it on first start, the same way as Musimo's other settings, and then the row is locked.

A fallback file whose song id differs from the song you asked for still uses the id in `job.json`. That id is the song you asked for.

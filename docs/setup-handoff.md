# Set up the account file command

Copy the prompt below into an assistant that can run commands on the computer where Musimo is already installed. A chat-only assistant can guide you through the same steps. Leave anything you do not know blank.

Run the [Musimo setup handoff](https://github.com/LeahyCC/musimo/blob/main/docs/setup-handoff.md) first. This prompt does not install Musimo again.

## Copy this prompt

```text
Musimo is already installed and running. Set up the account file command so a Deezer account download can keep a file that did not already play.

Repository: https://github.com/LeahyCC/musimo-account-file
Musimo repository: https://github.com/LeahyCC/musimo

My details, if known:
- Path of the existing Musimo checkout:
- Musimo URL:
- Where the account-file checkout should live:

Take the hookup through to a verified command. Run commands and make the necessary local configuration changes if your tools allow it. If you cannot access the host, give me a few exact commands at a time for my shell and wait for their results. Never imply you ran something you only described.

Keep explanations short and use plain words. Discover the existing installation before asking questions. Do not reinstall Musimo, replace the music mount, reset the database, delete volumes, or prune Docker. Do not print the Deezer cookie, client secrets, or the contents of account files.

1. Inspect the installation from the first handoff.

Find the Musimo checkout, Compose project, files, enabled profiles, container name, published URL, data volume, and host-to-container mounts. Read this repository's README.md. Read Musimo's docs/downloads.md and docs/settings.md sections for the Deezer account and file_command. Confirm the running app has the Command for the account file setting. If that field is missing, the running image is older than the account-file work: update Musimo from its own checkout with the same Compose project and profiles, then continue. Record both revisions.

2. Check out this program.

Clone https://github.com/LeahyCC/musimo-account-file if it is not already present. Reuse an existing checkout when one is there. Record its path and revision. Do not commit local secrets, a virtual environment, or an e2e folder.

3. Mount it where the Musimo worker can run it.

For Docker, add a read-only long-form bind to the existing ignored compose.override.yaml, beside the music mount. Do not change the music mount. Inside the container the program should be at /musimo-account-file/prepare.py. Check the merged Compose configuration before recreating, and do not publish its private values.

Recreate with the same Compose project, files, and profiles already in use. Do not rebuild the image unless the setting was missing. Example only when that profile is already enabled:

docker compose --profile youtube up -d

Confirm inside the container that /musimo-account-file/prepare.py exists and that python can import Cryptodome.Cipher. The image's python is the interpreter. Do not point the command at a Windows or macOS virtual environment from inside the container.

Without Docker, the worker and this program run on the same machine. Create a virtual environment from this checkout with Python 3.12 or newer, install requirements.txt, and run python -m unittest test_prepare.py. The command uses that interpreter and prepare.py.

4. Save the command.

The setting is Command for the account file, under the Deezer cookie. For Docker, the value is:

python /musimo-account-file/prepare.py

Without Docker, it is the absolute path of the virtual environment's python, then the absolute path of prepare.py. Use forward slashes. Quote a path that contains spaces. Backslashes are escapes. The field holds at most 500 characters.

Save it through Settings or PATCH /api/settings. Do not set MUSIMO_FILE_COMMAND when the row already exists. That variable only seeds a missing key, and then the row is locked. If the row is locked, stop and ask before changing it.

5. Verify.

Confirm the saved value and that it is the value you intended. If a Deezer cookie is already saved, download one recording the person has permission to obtain and confirm that source stays on Deezer and the finished file plays. A queued job or a 30-second preview is not that check. If no cookie is saved, stop after the command is saved and ask them to add it in Settings. Do not ask them to paste the cookie into the chat.

A fallback file whose song id differs from the song they asked for still uses the track id in job.json. Say that this case was not the one you tested, unless the download you observed was that case.

6. Update the private note.

Add the checkout path, revision, host-to-container mount, and saved command to the Musimo private note from the first handoff, usually runtime/setup-notes.md in the Musimo checkout. Do not commit compose.override.yaml or that note.

Finish with the Musimo URL, the command that was saved, and what the download check did. Call this setup complete only when the command is saved and, if a cookie was already present, one permitted account download played. If a provider refusal blocks that download, say so and leave the command in place.
```

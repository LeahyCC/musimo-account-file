"""Turn one saved account file into audio Musimo can keep.

Musimo passes the file path as the last argument and does not run a shell. The track id is read
from job.json in the same folder. On success the file is replaced in place, so Musimo can see
that it plays.
"""

import json
import sys
from pathlib import Path

from Cryptodome.Cipher import Blowfish
from Cryptodome.Hash import MD5

BLOCK = 2048


def key_for(song_id: str) -> bytes:
    secret = b"g4el58wc0zvf9na1"
    hashed = MD5.new(song_id.encode()).hexdigest().encode("ascii")
    chars = "".join(chr(hashed[i] ^ hashed[i + 16] ^ secret[i]) for i in range(16))
    return chars.encode()


def prepare_bytes(raw: bytes, song_id: str) -> bytes:
    """The account body, with every third 2048-byte block restored."""
    key = key_for(song_id)
    out = bytearray()
    index = 0
    for start in range(0, len(raw) - BLOCK + 1, BLOCK):
        block = raw[start : start + BLOCK]
        if index % 3 == 0:
            cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv=bytes(range(8)))
            block = cipher.decrypt(block)
        out.extend(block)
        index += 1
    out.extend(raw[index * BLOCK :])
    return bytes(out)


def track_id(folder: Path) -> str:
    job = json.loads((folder / "job.json").read_text(encoding="utf-8"))
    value = job.get("track_id")
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError("The job folder has no track id")
    return str(value)


def prepare_file(path: Path) -> None:
    song_id = track_id(path.parent)
    raw = path.read_bytes()
    if not raw:
        raise ValueError("The account file is empty")
    prepared = prepare_bytes(raw, song_id)
    temporary = path.with_name(path.name + ".prepared")
    temporary.write_bytes(prepared)
    temporary.replace(path)


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("The account file path is missing", file=sys.stderr)
        return 1
    try:
        prepare_file(Path(argv[-1]))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

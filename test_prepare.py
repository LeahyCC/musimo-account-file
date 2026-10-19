"""The prepared bytes match the account file Musimo used to keep."""

import json
import tempfile
import unittest
from pathlib import Path

from Cryptodome.Cipher import Blowfish

import prepare


class PrepareTests(unittest.TestCase):
    def test_a_striped_body_comes_back_as_the_plain_audio(self) -> None:
        song_id = "3135556"
        key = prepare.key_for(song_id)
        plain = bytes((index * 17) % 256 for index in range(prepare.BLOCK * 4 + 10))
        raw = bytearray(plain)
        for index, start in enumerate(range(0, len(raw) - prepare.BLOCK + 1, prepare.BLOCK)):
            if index % 3 == 0:
                cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv=bytes(range(8)))
                raw[start : start + prepare.BLOCK] = cipher.encrypt(raw[start : start + prepare.BLOCK])
        self.assertEqual(prepare.prepare_bytes(bytes(raw), song_id), plain)

    def test_the_file_is_replaced_using_the_track_id_beside_it(self) -> None:
        song_id = "42"
        plain = b"\x01" * (prepare.BLOCK * 3)
        key = prepare.key_for(song_id)
        raw = bytearray(plain)
        cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv=bytes(range(8)))
        raw[: prepare.BLOCK] = cipher.encrypt(bytes(raw[: prepare.BLOCK]))
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            (folder / "job.json").write_text(json.dumps({"track_id": int(song_id)}), encoding="utf-8")
            path = folder / "account.bin"
            path.write_bytes(raw)
            self.assertEqual(prepare.main(["prepare.py", str(path)]), 0)
            self.assertEqual(path.read_bytes(), plain)
            self.assertFalse(path.with_name(path.name + ".prepared").exists())

    def test_a_missing_track_id_leaves_the_file_alone(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            (folder / "job.json").write_text("{}", encoding="utf-8")
            path = folder / "account.bin"
            path.write_bytes(b"saved")
            self.assertEqual(prepare.main(["prepare.py", str(path)]), 1)
            self.assertEqual(path.read_bytes(), b"saved")


if __name__ == "__main__":
    unittest.main()

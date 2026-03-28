import tempfile
import unittest
from pathlib import Path

from _support import configure_src_path

configure_src_path()

from mina_repl_core import TranscriptRecorder


class TranscriptTests(unittest.TestCase):
    def test_export_jsonl_and_markdown(self) -> None:
        recorder = TranscriptRecorder()
        recorder.add("user", "chat", "hello")
        recorder.add("assistant", "chat", "world")

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            jsonl = recorder.export_jsonl(tmp_path / "session.jsonl")
            md = recorder.export_markdown(tmp_path / "session.md")

            self.assertTrue(jsonl.exists())
            self.assertTrue(md.exists())
            self.assertIn("hello", jsonl.read_text(encoding="utf-8"))
            self.assertIn("world", md.read_text(encoding="utf-8"))
            self.assertIn("# REPL Transcript", md.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

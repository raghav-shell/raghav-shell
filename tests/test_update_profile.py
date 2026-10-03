import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
import xml.etree.ElementTree as ET

spec = importlib.util.spec_from_file_location("profile", Path(__file__).resolve().parents[1] / "scripts/update_profile.py")
profile = importlib.util.module_from_spec(spec)
spec.loader.exec_module(profile)


class ProfileRefreshTests(unittest.TestCase):
    def payload(self, message="fix: preserve source pages", authored="2026-09-22T10:00:00Z"):
        return [{"sha": "a" * 40, "commit": {"message": message, "author": {"date": authored}}}]

    def snapshot(self, payload):
        return {"updated_at": "2026-10-03T12:00:00Z", "projects": [profile.normalize(profile.PROJECTS[0], payload)]}

    def test_commit_text_cannot_inject_svg(self):
        snapshot = self.snapshot(self.payload('<script>alert("x")</script> & details'))
        document = ET.fromstring(profile.render_activity(snapshot))
        self.assertFalse(document.findall(".//{http://www.w3.org/2000/svg}script"))
        self.assertIn("&lt;script&gt;", profile.render_activity(snapshot))

    def test_missing_commits_are_not_reported_as_recent_activity(self):
        snapshot = self.snapshot([])
        self.assertIn("No public authored commits found", profile.render_activity(snapshot))
        self.assertIn("not found", profile.render_badge(snapshot["projects"][0]))

    def test_malformed_response_is_rejected(self):
        with self.assertRaises(ValueError):
            profile.normalize(profile.PROJECTS[0], {"message": "rate limited"})
        bad = self.payload()
        bad[0]["sha"] = '<script>'
        with self.assertRaises(ValueError):
            profile.normalize(profile.PROJECTS[0], bad)

    def test_badge_uses_actual_authored_date(self):
        snapshot = self.snapshot(self.payload())
        self.assertIn("22 Sep 2026", profile.render_badge(snapshot["projects"][0]))
        self.assertIn("03 Oct 2026 · 17:30 IST", profile.render_activity(snapshot))

    def test_theme_variants_preserve_commit_text_and_dates(self):
        snapshot = self.snapshot(self.payload('style: use #c4b5fd & #131728'))
        files = profile.render_files(snapshot)
        for light, dark in [("activity.svg", "activity-dark.svg"), ("activity-mobile.svg", "activity-mobile-dark.svg")]:
            self.assertNotEqual(files[light], files[dark])
            def visible_text(source):
                return [n.text for n in ET.fromstring(source).iter() if n.tag.endswith('}text')]
            self.assertEqual(visible_text(files[light]), visible_text(files[dark]))
            self.assertIn('style: use #c4b5fd &amp; #131728', files[dark])
            self.assertIn('22 Sep 2026', files[dark])
            self.assertIn('#101e2b', files[dark])

    def test_api_failure_preserves_last_good_snapshot(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            (output / "activity.svg").write_text("last good snapshot")
            with patch.object(profile, "fetch_project", side_effect=HTTPError("https://api.github.com", 403, "rate limit", {}, None)):
                with self.assertRaises(HTTPError):
                    profile.refresh(output)
            self.assertEqual((output / "activity.svg").read_text(), "last good snapshot")
            self.assertEqual(len(list(output.iterdir())), 1)


if __name__ == "__main__":
    unittest.main()

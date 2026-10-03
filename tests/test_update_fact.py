import json
from pathlib import Path
import sys
import tempfile
import unittest
from datetime import date, datetime, timedelta, timezone
import xml.etree.ElementTree as ET
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import update_fact as facts


class DailyFactTests(unittest.TestCase):
    def test_every_joke_appears_once_per_cycle_and_tomorrow_changes(self):
        bank = facts.load_facts(facts.ROOT / 'data' / 'raghav-facts.json')
        cycle = [facts.choose_fact(bank, facts.EPOCH + timedelta(days=i)) for i in range(len(bank))]
        self.assertEqual(set(cycle), set(bank))
        self.assertEqual(len(set(cycle)), len(bank))
        self.assertNotEqual(cycle[-1], facts.choose_fact(bank, facts.EPOCH + timedelta(days=len(bank))))

    def test_same_date_is_stable_and_previous_dates_work(self):
        bank = ['a', 'b', 'c']
        self.assertEqual(facts.choose_fact(bank, facts.EPOCH), facts.choose_fact(bank, facts.EPOCH))
        self.assertIn(facts.choose_fact(bank, facts.EPOCH - timedelta(days=30)), bank)
        self.assertEqual(facts.ZONE.key, 'Asia/Kolkata')

    def test_utc_evening_uses_the_next_indian_calendar_day(self):
        instant = datetime(2026, 10, 3, 19, 0, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); readme = root / 'README.md'
            readme.write_text(facts.START + '\n' + facts.END)
            with patch.object(facts, 'datetime') as clock:
                clock.now.return_value = instant.astimezone(facts.ZONE)
                snapshot = facts.refresh(readme, root / 'facts')
                clock.now.assert_called_once_with(facts.ZONE)
            self.assertEqual(snapshot['date'], '2026-10-04')

    def test_quote_is_escaped_in_all_themes_mobile_and_alt_text(self):
        quote = 'Raghav said "<script>alert(1)</script>" & the bug fled.'
        for theme in ['light', 'dark']:
            for mobile in [False, True]:
                svg = facts.render_card(quote, date(2026, 10, 4), theme, mobile)
                root = ET.fromstring(svg)
                self.assertFalse(any(n.tag.split('}')[-1] == 'script' for n in root.iter()))
                self.assertIn(quote, ''.join(root.itertext()))
        self.assertIn('&quot;', facts.readme_block(quote, facts.EPOCH))
        self.assertNotIn('<script>', facts.readme_block(quote, facts.EPOCH))
        self.assertEqual(facts.readme_block(quote, facts.EPOCH).count('?day=2026-10-04'), 4)

    def test_refresh_preserves_other_readme_content_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); readme = root / 'README.md'; output = root / 'facts'
            readme.write_text('BEFORE\n' + facts.START + '\nold\n' + facts.END + '\nAFTER\n')
            snapshot = facts.refresh(readme, output, day=facts.EPOCH)
            first = {path.name: path.read_bytes() for path in output.iterdir()}
            body = readme.read_bytes()
            facts.refresh(readme, output, day=facts.EPOCH)
            self.assertEqual(first, {path.name: path.read_bytes() for path in output.iterdir()})
            self.assertEqual(body, readme.read_bytes())
            self.assertTrue(body.startswith(b'BEFORE\n'))
            self.assertTrue(body.endswith(b'\nAFTER\n'))
            self.assertEqual(json.loads((output / 'fact.json').read_text()), snapshot)
            self.assertEqual(len(first), 5)

    def test_invalid_bank_or_markers_preserve_last_published_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); readme = root / 'README.md'; output = root / 'facts'; bank = root / 'bank.json'
            readme.write_text('No markers here.'); output.mkdir(); (output / 'fact.json').write_text('last good snapshot')
            with self.assertRaises(ValueError): facts.refresh(readme, output, day=facts.EPOCH)
            self.assertEqual(readme.read_text(), 'No markers here.')
            self.assertEqual((output / 'fact.json').read_text(), 'last good snapshot')
            bank.write_text('["same", "same"]')
            with self.assertRaises(ValueError): facts.refresh(readme, output, bank, facts.EPOCH)
            self.assertEqual((output / 'fact.json').read_text(), 'last good snapshot')


if __name__ == '__main__':
    unittest.main()

from datetime import date, timedelta
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import update_garden as garden


def calendar(year, active=None):
    """The public calendar's real cell/tooltip structure, with controllable data."""
    active = active or {}
    current, stop, cells, tips = date(year, 1, 1), date(year+1, 1, 1), [], []
    while current < stop:
        count, level = active.get(current, (0, 0))
        key = f'day-{current.isoformat()}'
        cells.append(f'<td data-date="{current}" id="{key}" data-level="{level}"></td>')
        number = format(count, ',') if count else 'No'
        tips.append(f'<tool-tip for="{key}">{number} contribution{"s" if count != 1 else ""} on {current:%B} 1st.</tool-tip>')
        current += timedelta(days=1)
    # Tooltips may follow the table instead of immediately following each cell.
    return '<table>' + ''.join(cells) + '</table>' + ''.join(tips)


class FireflyGardenTests(unittest.TestCase):
    DAY = date(2026, 10, 4)

    def documents(self):
        return {2025: calendar(2025, {date(2025, 10, 5): (1, 1)}),
                2026: calendar(2026, {date(2026, 10, 4): (1234, 4), date(2026, 10, 5): (99, 3)})}

    def test_rolling_year_counts_leap_days_and_excludes_future(self):
        snapshot = garden.collect(self.DAY, self.documents())
        self.assertEqual(snapshot['from'], '2025-10-05')
        self.assertEqual(snapshot['total'], 1235)
        self.assertEqual(len(snapshot['days']), 365)
        self.assertEqual(snapshot['days'][-1]['date'], '2026-10-04')
        leap = garden.collect(date(2024, 3, 1), {2023: calendar(2023), 2024: calendar(2024)})
        self.assertIn('2024-02-29', [item['date'] for item in leap['days']])

    def test_missing_tooltips_inconsistent_levels_duplicates_and_bad_html_fail(self):
        valid = calendar(2026)
        for invalid in ['<html>Rate limited</html>', valid.replace('No contributions', 'Unexpected', 1),
                        valid.replace('data-level="0"', 'data-level="5"', 1),
                        valid.replace('No contributions', '9 contributions', 1), valid + valid]:
            with self.subTest(invalid=invalid[:60]), self.assertRaises(ValueError):
                garden.parse_calendar(invalid)
        with self.assertRaises(ValueError):
            garden.collect(self.DAY, {2025: calendar(2025), 2026: calendar(2026).replace('data-date="2026-10-04"', 'data-date="2026-12-31"')})

    def test_mobile_is_recent_13_calendar_weeks_with_its_own_total(self):
        snapshot = garden.collect(self.DAY, self.documents())
        days, cells, route, metrics, first = garden.layout(snapshot, True)
        self.assertEqual(metrics[-1], 13)
        self.assertEqual(sum(item['count'] for item in days), 1234)
        self.assertEqual(len(route), 13)
        self.assertTrue(all(first <= date.fromisoformat(item['date']) <= self.DAY for item in days))
        self.assertTrue(all(0 < x < 380 and 0 < y < 345 for x, y in route))

    def test_all_themes_safe_and_quiet_year_has_no_invented_sparks(self):
        quiet = garden.collect(self.DAY, {2025: calendar(2025), 2026: calendar(2026)})
        for theme in ['light', 'dark']:
            for mobile in [False, True]:
                document = garden.render(quiet, theme, mobile)
                root = ET.fromstring(document)
                self.assertIn('0 contributions', ''.join(root.itertext()))
                self.assertNotIn('class="bloom"', document)
                self.assertIn('prefers-reduced-motion:reduce', document)
                self.assertFalse(any(node.tag.split('}')[-1] in ['script', 'foreignObject', 'image'] for node in root.iter()))
                chart = [node for node in root.iter() if node.tag.endswith('rect') and any(child.tag.endswith('title') for child in node)]
                self.assertEqual(len(chart), len(garden.layout(quiet, mobile)[0]))

    def test_fetch_failure_leaves_previous_readme_and_artwork(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); readme = root/'README.md'; output = root/'art'; output.mkdir()
            readme.write_text(garden.START + '\nOLD\n' + garden.END)
            (output/'snapshot.json').write_text('last good')
            with patch.object(garden, 'fetch_calendar', side_effect=OSError('offline')):
                with self.assertRaises(OSError): garden.refresh(readme, output, self.DAY)
            self.assertIn('OLD', readme.read_text())
            self.assertEqual((output/'snapshot.json').read_text(), 'last good')

    def test_refresh_preserves_fact_and_other_sections_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); readme = root/'README.md'; output = root/'art'
            readme.write_text('FACT UNCHANGED\n' + garden.START + '\nold\n' + garden.END + '\nTOOLS UNCHANGED\n')
            garden.refresh(readme, output, self.DAY, self.documents())
            first = {path.name: path.read_bytes() for path in output.iterdir()}
            body = readme.read_bytes()
            garden.refresh(readme, output, self.DAY, self.documents())
            self.assertEqual(first, {path.name: path.read_bytes() for path in output.iterdir()})
            self.assertEqual(body, readme.read_bytes())
            self.assertTrue(body.startswith(b'FACT UNCHANGED\n'))
            self.assertTrue(body.endswith(b'\nTOOLS UNCHANGED\n'))
            self.assertEqual(readme.read_text().count('?day=2026-10-04'), 4)
            readme.write_text(garden.END + garden.START)
            with self.assertRaises(ValueError): garden.refresh(readme, output, self.DAY, self.documents())
            self.assertEqual(first, {path.name: path.read_bytes() for path in output.iterdir()})


if __name__ == '__main__':
    unittest.main()

import datetime as dt
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
source = ROOT / 'skills/jp-stock-move-reason/scripts/stock_move_sources.py'
spec = importlib.util.spec_from_file_location('forum_source', source)
forum = importlib.util.module_from_spec(spec)
spec.loader.exec_module(forum)
NOW = dt.datetime(2026, 9, 21, 12)


def post(hours, likes=10, text='業績予想の上方修正と増配について確認する投稿です', **extra):
    return dict(date=(NOW - dt.timedelta(hours=hours)).strftime('%Y/%m/%d %H:%M'),
                likes=likes, text=text, **extra)


class ForumFilterTests(unittest.TestCase):
    def test_raw_count_decides_window_before_quality_filters(self):
        posts = [post(1, likes=0) for _ in range(100)] + [post(30)]
        result = forum.select_yahoo_comments(posts, current=NOW)
        self.assertEqual((result['count'], result['comment_window_hours'], result['ai_input_count']), (100, 24, 0))
        result = forum.select_yahoo_comments(posts[:99] + [post(30)], current=NOW)
        self.assertEqual((result['recent_24h_raw_count'], result['comment_window_hours'], result['ai_input_count']), (99, 72, 1))

    def test_rejects_bad_time_old_posts_likes_and_short_text(self):
        result = forum.select_yahoo_comments([
            post(73), post(-1), post(1, likes=4), post(1, text='買い'),
            dict(date='unknown', likes=99, text='業績予想の上方修正について'), post(72),
        ], current=NOW)
        self.assertEqual(result['eligible_comment_count'], 1)
        self.assertEqual(result['comments'][0]['date'], post(72)['date'])

    def test_score_shortlist_then_latest_five_and_exact_prefix_dedup(self):
        posts = [post(i, likes=100, text=f'{i:02d} 業績予想の上方修正と増配について確認する投稿です') for i in range(25)]
        posts += [dict(posts[0], text=posts[0]['text'] + '！')]
        result = forum.select_yahoo_comments(posts, current=NOW)
        self.assertEqual(result['shortlist_count'], 20)
        self.assertEqual(result['comments'], posts[:5])
        prefix = '業績の確認を続ける' * 10
        self.assertEqual(len(forum.dedupe_comments([post(1, text=prefix+'A'), post(1, text=prefix+'B')], 20)), 1)
        self.assertEqual(len(forum.dedupe_comments([post(1, text='A'+prefix), post(1, text='Ｂ'+prefix)], 20)), 2)

    def test_yearless_dates_use_supplied_reference_year(self):
        result = forum.select_yahoo_comments([dict(post(1), date='12/31 23:30')], current=dt.datetime(2025, 1, 1, 0, 30))
        self.assertEqual(result['ai_input_count'], 1)

    def test_live_collection_exposes_selected_comments_only(self):
        args = forum.build_arg_parser().parse_args(['7203', '--forum-only'])
        args.sources = set(args.sources.split(','))
        posts = [post(i, text=f'{i:02d} 業績予想の上方修正と増配について確認する投稿です') for i in range(20)]
        selected = forum.select_yahoo_comments(posts, current=NOW)
        with patch.object(forum, 'fetch_yahoo_bbs', return_value=selected):
            data = forum.collect_sources(args)
        self.assertEqual(len(data['bbs']['comments']), 5)
        self.assertEqual(data['bbs']['count'], 20)
        self.assertIn('heat', data['bbs'])
        self.assertNotIn('cached_comments', data['bbs'])

    def test_packaged_offline_command_runs_without_network(self):
        sys.path.insert(0, str(ROOT / 'plugin'))
        import build
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            files = build.package_files()
            for name, content in files.items():
                dest = root / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(content)
            packet = root / 'comments.json'
            packet.write_text(json.dumps(dict(as_of='2026-09-21T12:00:00+09:00', comments=[post(1)])))
            # Deny socket use in the subprocess, so importing succeeds but any network access fails.
            (root / 'sitecustomize.py').write_text('import socket\ndef denied(*a, **k): raise RuntimeError("network forbidden")\nsocket.socket.connect = denied\nsocket.create_connection = denied\n')
            import os
            env = dict(os.environ, PYTHONPATH=str(root))
            result = subprocess.run([sys.executable, str(root / 'skills/jp-stock-move-reason/scripts/filter_forum.py'), str(packet)],
                                    env=env, check=True, text=True, capture_output=True)
            data = json.loads(result.stdout)
            self.assertFalse(data['network_used'])
            self.assertEqual(data['ai_input_count'], 1)
            self.assertNotIn('cached_comments', data)


if __name__ == '__main__':
    unittest.main()

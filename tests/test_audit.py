import importlib.util
import json
import pathlib
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / 'tools' / 'audit_export.py'
spec = importlib.util.spec_from_file_location('audit_export', SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.file = pathlib.Path(self.tmp.name) / 'conversations.json'
        self.thread = 't1'
        self.data = [{
            'id': self.thread, 'title': 'fixture', 'create_time': 1,
            'current_node': 'b', 'mapping': {
                'root': {'parent': None, 'message': None},
                'a': {'parent': 'root', 'message': {'author': {'role': 'user'}, 'metadata': {'model_slug': 'bidi', 'bidi_voice_mode_message': True}}},
                'b': {'parent': 'a', 'message': {'author': {'role': 'assistant'}, 'metadata': {'model_slug': 'gpt-6-thinking'}}},
                'fork': {'parent': 'a', 'message': {'author': {'role': 'assistant'}, 'metadata': {'model_slug': 'gpt-6-thinking'}}}
            }
        }]
        self.file.write_text(json.dumps(self.data))

    def test_counts_and_branch(self):
        got = mod.audit(self.file, self.thread)
        self.assertEqual(got['node_count'], 4)
        self.assertEqual(got['roles'], {'assistant': 2, 'no_message': 1, 'user': 1})
        self.assertEqual(got['branch_points_in_export'], 1)
        self.assertEqual(got['current_path_nodes'], 3)

    def test_original_bytes_are_committed_by_hash(self):
        before = mod.audit(self.file, self.thread)['input_sha256']
        self.file.write_text(self.file.read_text() + ' ')
        after = mod.audit(self.file, self.thread)['input_sha256']
        self.assertNotEqual(before, after)

    def test_missing_id(self):
        with self.assertRaises(ValueError):
            mod.audit(self.file, 'wrong')


if __name__ == '__main__':
    unittest.main()

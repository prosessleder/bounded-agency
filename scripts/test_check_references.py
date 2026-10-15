#!/usr/bin/env python3
"""Offline regression checks for export fidelity and the build's audit gate."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

import check_references as audit


class ReferenceAuditTests(unittest.TestCase):
    def test_all_selected_metadata_survives_export(self):
        _, entries = audit.export_bibliography((audit.ROOT / 'references.md').read_text())
        self.assertEqual(len(entries), 28)
        self.assertEqual(len(entries[4]['authors']), 14)
        self.assertEqual(len(entries[6]['authors']), 15)
        self.assertEqual(entries[8]['authors'], ['Renato Iannella', 'Serena Villata'])
        self.assertEqual(entries[24]['authors'], ['Andrew J. I. Jones', 'Marek Sergot'])
        self.assertEqual(entries[11]['fields']['year'], '2017')
        self.assertEqual(entries[16]['fields']['eprint'], '2606.03895v3')
        for index in (7, 21, 27):
            self.assertNotIn('year', entries[index]['fields'])
        self.assertTrue(all(e['fields']['title'] and e['fields']['url'] for e in entries))

    def test_malformed_or_missing_entries_fail_closed(self):
        for source in ('', '[2] A. 2020. “Title.” [link](https://example.org)',
                       '[1] A. 2020. No delimited title. [link](https://example.org)'):
            with self.subTest(source=source), self.assertRaises(ValueError):
                audit.export_bibliography(source)

    def run_gate(self, summary, *, strict=False, process_exit=0, write_report=True, change_source=False):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'paper.md').write_text('Manuscript')
            (root / 'references.md').write_text('[1] A. 2020. “Title.” [link](https://example.org)')
            output = root / 'reports'
            output.mkdir()
            # Ensure a failed new run cannot accidentally reuse a prior report.
            (output / 'report.json').write_text('{"summary":{"total_references_processed":1}}')
            argv = ['check_references.py', '--python', sys.executable, '--output-dir', str(output)]
            if strict:
                argv.append('--strict')
            installed = {'version': '3.1.6', 'origin': {'vcs_info': {'commit_id': audit.REVISION}}}

            def fake_run(command, **kwargs):
                self.assertEqual(kwargs['env']['REFCHECKER_USE_LLM'], 'false')
                self.assertNotIn('OPENAI_API_KEY', kwargs['env'])
                self.assertNotIn('ANTHROPIC_API_KEY', kwargs['env'])
                if write_report:
                    (output / 'report.json').write_text(json.dumps({'summary': summary}))
                if change_source:
                    (root / 'references.md').write_text('Changed during online verification')
                return types.SimpleNamespace(returncode=process_exit)

            with patch.object(audit, 'ROOT', root), patch.object(sys, 'argv', argv), \
                 patch.object(audit.subprocess, 'check_output', return_value=json.dumps(installed)), \
                 patch.object(audit.subprocess, 'run', side_effect=fake_run), \
                 patch.dict(audit.os.environ, {'OPENAI_API_KEY': 'fake', 'ANTHROPIC_API_KEY': 'fake'}), \
                 contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                result = audit.main()
            return result, json.loads((output / 'provenance.json').read_text())

    def test_complete_report_passes(self):
        code, provenance = self.run_gate({'total_papers_processed': 1, 'total_references_processed': 1})
        self.assertEqual(code, 0)
        self.assertTrue(provenance['complete'])

    def test_findings_are_advisory_unless_strict(self):
        summary = {'total_papers_processed': 1, 'total_references_processed': 1, 'total_unverified_refs': 1}
        self.assertEqual(self.run_gate(summary)[0], 0)
        self.assertEqual(self.run_gate(summary, strict=True)[0], 1)

    def test_incomplete_report_blocks_build(self):
        for summary in ({}, {'total_papers_processed': 1, 'total_references_processed': 0}):
            self.assertEqual(self.run_gate(summary)[0], 2)

    def test_process_failure_or_missing_report_cannot_pass(self):
        summary = {'total_papers_processed': 1, 'total_references_processed': 1}
        self.assertEqual(self.run_gate(summary, process_exit=1)[0], 2)
        self.assertEqual(self.run_gate(summary, write_report=False)[0], 2)

    def test_source_change_during_scan_blocks_build(self):
        summary = {'total_papers_processed': 1, 'total_references_processed': 1}
        code, provenance = self.run_gate(summary, change_source=True)
        self.assertEqual(code, 2)
        self.assertFalse(provenance['source_unchanged'])


if __name__ == '__main__':
    unittest.main()

"""Regression: a committed STATUS snapshot cannot truthfully embed its own HEAD.

The commit that stores STATUS.md necessarily changes HEAD, so output must
identify the result-code fingerprint and generation time rather than claim
to describe the repository's current revision or worktree cleanliness.
"""
import unittest

from mind.status import render


class StatusSnapshotProvenance(unittest.TestCase):
    def test_generated_header_is_an_historical_snapshot(self):
        output = render({}, {}, [], "example-result-fingerprint")
        header = "\n".join(output.splitlines()[:6])
        self.assertIn("# MIND — computed knowledge snapshot", header)
        self.assertIn("**Generated snapshot**", header)
        self.assertIn(
            "Result-code fingerprint `example-result-fingerprint` · snapshot generated ",
            header,
        )
        self.assertIn("It reflects the last generation, not current Git HEAD.", header)
        self.assertNotIn(" · git `", header)
        self.assertNotIn(" + uncommitted changes", header)


if __name__ == "__main__":
    unittest.main()

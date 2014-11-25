from itertools import islice
import json
from models.bmat_work import BmatWork

__author__ = 'borja'
import unittest
from work_matcher import WorkMatcher


class MatcherTest(unittest.TestCase):
    def setUp(self):
        self.matcher = WorkMatcher()
        self.file = 'files/bmat2heaven11_20141008.tsv'

    def test_direct_match_file(self):
        matched_works = []

        with open(self.file) as f:
            # Jump the first line
            f.readline()

            while True:
                works = []
                next_lines = list(islice(f, 5000))

                if not next_lines:
                    break

                for line in next_lines:
                    bmat_work = BmatWork(line)
                    works.append(bmat_work.__dict__)

                matched_works.extend(self.matcher.direct_match_works_by_titles(works))
                matched_works = [self.matcher.refine_by_artists(work) for work in matched_works]
                matched_works = [self.matcher.refine_by_writers(work) for work in matched_works]

        with open('direct-matching-results.txt', 'w') as outfile:
            json.dump(matched_works, outfile, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def test_token_match_file(self):
        matched_works = []

        with open(self.file) as f:
            # Jump the first line
            f.readline()

            while True:
                works = []
                next_lines = list(islice(f, 5000))

                if not next_lines:
                    break

                for line in next_lines:
                    bmat_work = BmatWork(line, True)
                    works.append(bmat_work.__dict__)

                matched_works.extend(self.matcher.tokens_match_works_by_titles(works))
                matched_works = [self.matcher.refine_by_artists_tokens(work) for work in matched_works]
                matched_works = [self.matcher.refine_by_writers_tokens(work) for work in matched_works]

        with open('token-matching-results.txt', 'w') as outfile:
            json.dump(matched_works, outfile, default=lambda o: o.__dict__, sort_keys=True, indent=4)
from itertools import islice
import json
import gc
import os
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
            iterarions = 0
            while True:
                works = []
                next_lines = list(islice(f, 5000))

                if not next_lines:
                    break

                for line in next_lines:
                    bmat_work = BmatWork(line, True)
                    works.append(bmat_work.__dict__)

                matched_works = self.matcher.tokens_match_works_by_titles(works)
                matched_works = [self.matcher.refine_by_artists_tokens(work)
                                          for work in matched_works]
                matched_works = [self.matcher.refine_by_writers_tokens(work)
                                          for work in matched_works]

                file_name = 'results/token-matching-results-{}-.json'.format(iterarions)
                with open(file_name, 'w') as outfile:
                    json.dump(matched_works, outfile, default=lambda o: o.__dict__, sort_keys=True, indent=4)

                del matched_works
                iterarions += 1
                gc.collect()

    def test_filter_by_threshold(self):
        threshold = 0.8
        header = 'title,bmat_artists,bmat_creators,cwr_artists,cwr_creators,max_artist_threshold,max_creator_threshold'
        with open('filtered-results.csv', 'w') as output:
            output.write(header + '\n')

            for file_name in os.listdir('results'):
                with open('results/{}'.format(file_name)) as results_file:
                    json_file = json.load(results_file)

                    for match in json_file:
                        best_artist_match_threshold = 0
                        for artist in match['artist_thresholds']:
                            artist_threshold = match['artist_thresholds'][artist]
                            if artist_threshold > best_artist_match_threshold:
                                best_artist_match_threshold = artist_threshold

                        best_creator_match_threshold = 0
                        for creator in match['creator_thresholds']:
                            creator_threshold = match['creator_thresholds'][creator]
                            if creator_threshold > best_creator_match_threshold:
                                best_creator_match_threshold = creator_threshold

                        if best_artist_match_threshold > threshold or best_creator_match_threshold > threshold:
                            work_title = match['work']['title']
                            bmat_artists = [artist for artist in match['bmat_info']['artists']]
                            bmat_creators = [creator for creator in match['bmat_info']['creators']]
                            cwr_artists = [performer['last_name'] + ' ' + performer['first_name']
                                           if performer['first_name'] is not None else performer['last_name']
                                           for performer in match['work']['performers']]
                            cwr_writers = [writer['first_name'] + ' ' + writer['last_name']
                                           if writer['first_name'] is not None else writer['last_name']
                                           for writer in match['work']['writers']]

                            line = '{},{},{},{},{},{},{}{}'.format(work_title, '||'.join(bmat_artists),
                                                                   '||'.join(bmat_creators), '||'.join(cwr_artists),
                                                                   '||'.join(cwr_writers), best_artist_match_threshold,
                                                                   best_creator_match_threshold, '\n')
                            output.write(line)
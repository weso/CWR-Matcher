from bmat.wolf.utils.string_utils import StringUtils
from models.matched_work import MatchedWork

__author__ = 'borja'
from database_client import DatabaseClient


class WorkMatcher(object):
    def __init__(self):
        self.database = DatabaseClient()

    def direct_match_work_by_title(self, title):
        return self.database.get_works_by_title(title.upper())

    def direct_match_works_by_titles(self, works):
        matched_works = []
        temporal_works = {work['title']: work for work in works}

        retrieved_works = self.database.get_works_by_titles(works)

        for match in retrieved_works:
            matched_work = MatchedWork(temporal_works[match['title']])

            matched_work.title_threshold = 1
            matched_work.work = match
            matched_works.append(matched_work)

        return matched_works

    def tokens_match_works_by_titles(self, works):
        matched_works = []
        temporal_works = {work['title']: work for work in works}

        retrieved_works = self.database.get_works_by_titles(works)

        for match in retrieved_works:
            matched_work = MatchedWork(temporal_works[match['title']])

            matched_work.title_threshold = 1
            matched_work.work = match
            matched_works.append(matched_work)

        return matched_works

    @staticmethod
    def refine_by_artists(work):
        bmat_artists = work.bmat_info['artists']
        cwr_artists = [performer['last_name'] for performer in work.work['performers']]

        for bmat_artist in bmat_artists:
            best_match = -1
            for cwr_artist in cwr_artists:
                best_match = max(best_match, StringUtils.compare(str(bmat_artist), str(cwr_artist)))

            work.add_artist_threshold(bmat_artist, best_match)

        return work

    @staticmethod
    def refine_by_artists_tokens(work):
        bmat_entities = work.bmat_info['artists'] + work.bmat_info['creators']
        cwr_artists = [performer['last_name'] + ' ' + performer['first_name'] if performer['first_name'] is not None else performer['last_name']
                       for performer in work.work['performers']]

        for bmat_entity in bmat_entities:
            best_match = -1
            bmat_tokens = bmat_entity.split(' ')
            total_tokens_match = 0
            for cwr_artist in cwr_artists:
                cwr_tokens = cwr_artist.split(' ')
                total_tokens_match = 0

                for bmat_token in bmat_tokens:
                    token_match = 0

                    for cwr_token in cwr_tokens:
                        token_match = max(token_match, StringUtils.compare(str(bmat_token), str(cwr_token)))
                    total_tokens_match += token_match
                total_tokens_match /= len(bmat_tokens)
            best_match = max(best_match, total_tokens_match)

            if best_match >= 0:
                work.add_artist_threshold(bmat_entity, best_match)

        return work

    @staticmethod
    def refine_by_writers(work):
        bmat_creators = work.bmat_info['creators']
        cwr_writers = [writer['first_name'] for writer in work.work['writers']]

        for bmat_creator in bmat_creators:
            best_match = -1
            for cwr_writer in cwr_writers:
                best_match = max(best_match, StringUtils.compare(str(bmat_creator), str(cwr_writer)))
            work.add_creator_threshold(bmat_creator, best_match)

        return work

    @staticmethod
    def refine_by_writers_tokens(work):
        bmat_entities = work.bmat_info['artists'] + work.bmat_info['creators']
        cwr_writers = [writer['first_name'] + ' ' + writer['last_name'] if writer['first_name'] is not None else
                       writer['last_name'] for writer in work.work['writers']]

        for bmat_entity in bmat_entities:
            best_match = -1
            bmat_tokens = bmat_entity.split(' ')
            total_tokens_match = 0
            for cwr_writer in cwr_writers:
                cwr_tokens = cwr_writer.split(' ')
                total_tokens_match = 0

                for bmat_token in bmat_tokens:
                    token_match = 0

                    for cwr_token in cwr_tokens:
                        token_match = max(token_match, StringUtils.compare(str(bmat_token), str(cwr_token)))
                    total_tokens_match += token_match
                total_tokens_match /= len(bmat_tokens)
            best_match = max(best_match, total_tokens_match)

            if best_match >= 0:
                work.add_creator_threshold(bmat_entity, best_match)

        return work
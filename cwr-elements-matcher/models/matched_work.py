__author__ = 'borja'


class MatchedWork(object):
    def __init__(self, bmat_info):
        self.bmat_info = bmat_info
        self.work = None
        self.title_threshold = None
        self.artist_thresholds = {}
        self.creator_thresholds = {}

    def add_artist_threshold(self, artist_name, threshold):
        self.artist_thresholds[artist_name] = threshold

    def add_creator_threshold(self, creator_name, threshold):
        self.creator_thresholds[creator_name] = threshold
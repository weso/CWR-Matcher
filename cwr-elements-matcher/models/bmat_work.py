import re

__author__ = 'borja'


class BmatWork(object):
    def __init__(self, work_line, tokens=False):
        slices = self.clear_line(work_line).split('\t')

        self.id = slices[0]
        self.title = slices[2].upper()
        self.isrc = slices[3]

        self._populate_artists(slices[1])
        self._populate_creators(slices[4])
        self.labels = [label.upper() for label in slices[5].split(',')]
        self.albums = [album.upper() for album in slices[6].split('||')]

        if tokens:
            self.tokens = self.title.split(' ')

    def _populate_artists(self, artists):
        self.artists = [artist.upper().strip() for artist in artists.split('||')]

    def _populate_creators(self, creators):
        creators = re.sub(r'[^a-zA-Z\d\s\.]', ',', creators)
        self.creators = filter(None, set([creator.upper().strip() for creator in creators.split(',')]))
        self.creators = list(self.creators)

    @staticmethod
    def clear_line(line):
        return line.replace('\n', '')

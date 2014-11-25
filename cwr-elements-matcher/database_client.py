import json
import urllib2
from pip._vendor import requests

__author__ = 'borja'

from config import DATABASE_API


class DatabaseClient(object):
    def __init__(self):
        self.endpoint = DATABASE_API

    def get_works_by_title(self, work_title):
        works = urllib2.urlopen(self.endpoint + 'works/title/' + urllib2.quote(work_title)).read()

        return works

    def get_works_by_titles(self, works):
        url = self.endpoint + 'works/title/'
        data = json.dumps(works)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

        r = requests.post(url, data=data, headers=headers)

        return  r.json()
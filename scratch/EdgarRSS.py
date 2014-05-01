__author__ = 'rochak'

import urllib.parse
import feedparser
import datetime
from pymongo import MongoClient

mongo = MongoClient('localhost', 27017)
db = mongo.edgar

class RecentFiling(object):
    raw_title = None
    sec_link = None
    filed = None
    accession = None
    updated = None
    form_type = None
    is_issuer = False

    def __init__(self, sec_entry):
        super(RecentFiling, self).__init__()

        self.set_accession(sec_entry['id'])
        self.raw_title = sec_entry['title']
        self.set_is_issuer()
        self.set_updated(sec_entry['updated'])
        self.sec_link = sec_entry['link']

        if sec_entry['tags'][0]['label'] == 'form type':
            self.form_type = sec_entry['tags'][0]['term']
        else:
            # get the form type from the raw_title
            self.form_type = self.raw_title.split('-')[0].strip()

    def get_mongo_dict(self):
        # TODO: need to get the object as a dict key and use that.
        obj = {}
        obj['raw_title'] = self.raw_title
        obj['sec_link'] = self.sec_link
        obj['accession'] = self.accession
        obj['updated'] = self.updated
        obj['form_type'] = self.form_type
        obj['is_issuer'] = self.is_issuer

        return obj

    def save(self):
        # this will save the current entry to mongo collection.
        recent_filings = db.recent_filings
        recent_filings.insert(self.get_mongo_dict)

    def set_updated(self, updated):
        # date is in format: 2013-12-31T20:48:11-05:00
        # parse it the stupid way.
        data = updated.split('T')
        u_date = data[0]
        u_time = data[1].split('-')[0]

        (year, month, day) = u_date.split('-')
        (hour, minute, sec) = u_time.split(':')

        #ignore time zone
        dt = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(sec))
        self.updated = dt

    def set_is_issuer(self):
        if "issuer" in self.raw_title:
            self.is_issuer = True
            return True
        else:
            self.is_issuer = False
            return False

    def set_accession(self, acc):
        self.accession = acc.rstrip().split("=")[1]


class EdgarRSSReader(object):
    edgar_rss_url = "http://www.sec.gov/cgi-bin/browse-edgar"
    last_params_used = None
    default_params = {'action': 'getcurrent',
                      'type': '',
                      'company': '',
                      'dateb': '',
                      'owner': 'include',
                      'start': '0',
                      'count': '100',
                      'output': 'atom'
                      }

    def __init__(self):
        super(EdgarRSSReader, self).__init__()

    def get_default_params(self, call_type=None):
        if call_type is None:
            return self.default_params

        if call_type == 'company':
            params = self.default_params
            params['action'] = 'getcompany'
            params['CIK'] = ''
            return params

        return self.default_params


    def get_rss_url(self):
        return self.edgar_rss_url

    # extending classes should implement this method.
    # by default this returns the getcurrent.
    def get_feed(self, params):

        edgar_url = self.edgar_rss_url + "?action=" + params['action'] + "&" + urllib.parse.urlencode(params)
        feed = feedparser.parse(edgar_url)

        # make sure there are entries in feed.
        if len(feed['entries']) <= 0:
            raise Exception('No entries')

        return feed

    def get_current(self, params=None):
        if params is None:
            params = self.get_default_params()

        feed = self.get_feed(params)
        recent_filings = []
        most_recent_filing = db.most_recent_filing.findOne()

        for entry in feed['entries']:
            recent_entry = RecentFiling(entry)

            if most_recent_filing is None:
                db.most_recent_filing.insert(recent_entry.get_mongo_dict())

            recent_filings.append(recent_entry)
            # save it in the mongodb
            db.recent_filings.insert(recent_entry.get_mongo_dict())

        return recent_filings

    def get_company(self, cik=None):
        params = self.get_default_params('company')
        if cik is not None:
            params['CIK'] = cik

        return self.get_feed(params)

    def get_insider_trades(self, params=None):
        # only support form 4 for now.
        if params is None:
            params = self.get_default_params()

        params['type'] = '4'
        feed = self.get_feed(params)

        recent_filings = []

        for entry in feed['entries']:
            recent_filings.append(RecentFiling(entry))

        return recent_filings


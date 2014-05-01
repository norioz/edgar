__author__ = 'rochak'

import time
import pprint
import feedparser

pp = pprint.PrettyPrinter(indent=4)

last_updated = None


class RecentEntry:
    form_type = None  # can be any form
    raw_title = None
    title = None
    sec_link = None
    summary = None
    updated = None
    category = None
    id = None  # there are 2 transactions per id. issuing and reporting. assuming reporting is the beneficiary
    is_issuer = None  # is the company that is issuing


    def __init__(self, sec_entry):
        super(Entry, self).__init__()
        self.set_id(sec_entry['id'])
        self.raw_title = sec_entry['title']
        self.set_title()
        if self.set_is_issuer():
            pass

        self.summary = sec_entry['summary']
        self.updated = sec_entry['updated_parsed']

        self.sec_link = sec_entry['link']
        self.category = sec_entry['category']

        if sec_entry['tags']['label'] == 'form type':
            self.form_type = sec_entry['tags']['term']

    # title is in the format
    # <title>10-K - MOHEGAN TRIBAL GAMING AUTHORITY (0001005276) (Filer)</title>
    # "Form" - Company/entity (CIK) (who)
    def parse_title(self):
        pass

    def set_is_issuer(self):
        if "issuer" in self.title:
            self.is_issuer = True
            return True
        else:
            self.is_issuer = False
            return False

    def set_id(self, acc):
        self.id = acc.rstrip().split("=")[1]



def get_specific():
    sec_url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001263508&type=&dateb=&owner=include&start=0&count=100&output=atom"

    track_companies = []
    track_forms = ['3', '4', '5', 'SC 13D/A', '13F-HR', 'SC 13D', 'SC 13G/A', 'SC 13G']

    feed = feedparser.parse(sec_url)
    # feed has the following: dict_keys(['entries', 'encoding', 'href', 'version', 'feed', 'namespaces', 'headers', 'bozo', 'status'])
    #pp.pprint(feed['feed'])
    pp.pprint(feed['entries'])
    exit()

    entries = feed['entries']
    # entries is list of enty.
    # entry has the following
    # dict_keys(['accession-nunber_detail', 'size_detail', 'updated_parsed', 'updated', 'amend_detail',
    # 'filing-type_detail', 'tags', 'amend', 'content', 'title_detail', 'links', 'summary', 'summary_detail',
    # 'filing-date', 'id', 'filing-type', 'link', 'form-name_detail', 'title', 'filing-href_detail', 'filing-href',
    # 'accession-nunber', 'form-name', 'filing-date_detail', 'guidislink', 'size'])

    # care about the track_forms and
    for entry in entries:
        print(entry['filing-type'], entry['form-name'])


def get_recent():
    start = 0
    sec_url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=&company=&dateb=&owner=include&start=0&count=100&output=atom"

    feed = feedparser.parse(sec_url)

    global last_updated

    # print(feed['feed']['updated'])
    # print(feed['feed']['updated_parsed'])
    if len(feed['entries']) > 0:
        entries = feed['entries']
        if last_updated is None:
            # must be the first time run!
            pp.pprint(entries[0])
            last_updated = RecentEntry(entries[0])
        pp.pprint(last_updated)


    time.sleep(15)
    #entries = feed['entries']
    #most_recent_entry = entries[0]
    #print(most_recent_entry)
    # print(most_recent_entry['filing-type'], most_recent_entry['form-name'])

#while True:
#    get_recent()

#get_recent()

get_specific()
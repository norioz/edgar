pyEDGAR
=====

EDGAR is the SEC's "electronic data gathering analysis and retrieval" system.
It publishes RSS feeds that indicate documents filed with the SEC for various activities.
https://www.sec.gov/about/secrss.shtml

Basic EDGAR feeds provide information about...

* Companies
* Mutual funds
* Recent SEC filings
* Historical filings

PyEDGAR is a RSS+Atom spider for the EDGAR feeds written in python that...

* fetches the SEC recent filings RSS
* converts the RSS data into JSON records
* checks for new filings
* stores records for new filings in a DB

Available data can be viewed by querying the DB.


## Requirements

* Python 2.6 or later
* mongoDB


## How to Run

TBD

## Seeing the Data

TBD

## Links

https://www.sec.gov/about/secrss.shtml
https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000896878&type=&dateb=&owner=exclude&start=0&count=40&output=atom
https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000896878&owner=exclude&count=40&hidefilings=0
https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&CIK=0000896878&type=&dateb=&owner=exclude&start=0&count=40&output=atom

CIK - unique company identifier
company - ???
type - form type
dateb - yyyymmdd  filings prior to this date
owner - [include, exclude, only]
count - how many results (max 200)
start - offset within all results
hidefilings - [1,0]
output - output type [atom]




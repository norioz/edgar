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

* Python 2.4 or later
* mongoDB


## How to Run

TBD

## Seeing the Data

TBD
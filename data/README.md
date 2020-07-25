Two scripts for gathering data from [2milesurf.com/surfreport](https://2milesurf.com/surfreport):
* `crawl_squarespace_site.py` crawls pages of surf reports and saves raw HTML for offline processing
* `clean_squarespace_posts.py` uses BeautifulSoup to clean the aforementioned HTML files, producing a single txt corpus

An attempt is made to split channel and patch reports so that separate Markov chains can be built from each.

A pretty clean but definitely not perfect dataset can be found in [2Mile_reports.txt.gz](2Mile_reports.txt.gz).

Enjoy!
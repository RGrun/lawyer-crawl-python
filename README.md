# lawyer-crawl-python
The same as my other lawyercrawl project, but written in Python and using Scrapy.

## Why does this exist?

One day at work I built [lawyer-crawl-clojure](https://github.com/RGrun/lawyer-crawl-clojure) so we could
scrape thousands of lawyer records from [Cornell University's lawyer directory](https://lawyers.law.cornell.edu/),
but my boss stopped me halfway through and told me to write it in Python using Scrapy instead.

What you see here is the result of that. We used this small program to scrape the names, emails,
phone numbers, websites and photos of around 8000 personal injury attorneys from around the US.
Unlike the one written in Clojure, this webscraper sticks the results into a MongoDB database.

Enjoy.

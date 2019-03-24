# ePetitions Activity tracker

This is a small web app that tracks signatures on petitions to the [UK Government & Parliament][p.par.uk] over time.

## Quickstart

1.  Clone the repository, and `docker-compose up`.
2.  Create the database schema with `docker-compose run app flask init_db`
3.  The Flask app is available at http://localhost:3000/petition
4.  Fetch petition data with `docker-compose run app flask track_petition`

## Preamble

This was created initially to track the [largest and fastest-growing petition][art50], and to keep a counter available
while the main website struggled to cope with the load. It's being expanded to cover all petitions on the site, and
allow export of data for analysis.

This app is also an attempt to create a website with a dynamic backend that only serves static content, while feeling
dynamic with AJAX, etc.

[p.par.uk]: https://petition.parliament.uk/
[art50]: https://petition.parliament.uk/petitions/241584

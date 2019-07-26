=======
Scrapyd
=======

.. image:: https://secure.travis-ci.org/scrapy/scrapyd.svg?branch=master
    :target: http://travis-ci.org/scrapy/scrapyd

.. image:: https://codecov.io/gh/scrapy/scrapyd/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/scrapy/scrapyd

Scrapyd is a service for running `Scrapy`_ spiders.

It allows you to deploy your Scrapy projects and control their spiders using an
HTTP JSON API.

The documentation (including installation and usage) can be found at:
http://scrapyd.readthedocs.org/

.. _Scrapy: https://github.com/scrapy/scrapy

---

### Forked Verions Notes

This forked version writes the job information to mongodb. In order to use it simply add
the mongo db connection information to you config file: 

```
mongodb_host = 0.0.0.0
mongodb_port = 27017
mongodb_user = admin
mongodb_pass = pass
```

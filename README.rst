python-nytcongressapi
==================

A Python wrapper for The New York Times Congress API, which provides information about members, roles and votes for the United States Congress. (http://developer.nytimes.com/docs/congress_api). This wrapper borrows heavily in its design from the python-sunlightapi project by James Turk.
(http://github.com/sunlightlabs/python-sunlightapi)

python-nytcongressapi is a project of Derek Willis <dwillis@gmail.com> (c) 2009.

All code is under the MIT License, see LICENSE for details.


Requirements
============

python >= 2.4

simplejson >= 1.8 (not required with python 2.6, will use built in json module)


Installation
============
To install run

    ``python setup.py install``

which will install the bindings into python's site-packages directory.

Usage
=====

To initialize the api, all that is required is for it to be imported and for an
API key to be defined.

(If you do not have an API key visit http://developer.nytimes.com/ to
register for one.)

Import ``nytcongress`` from ``nytcongressapi``:
    
    >>> from nytcongressapi import nytcongress, NYTCongressApiError
    
And set your API key:
    
    >>> nytcongress.apikey = 'nytcongress-api-key'

-------------------
member methods
-------------------

    * member.get                          - get a single member
    * members.for_congress_and_chamber    - get zero or more member
    

get
---------------
    
member.get takes a single parameter to lookup a single member of the House or Senate.

The parameter is:
    * id (the official ID from http://bioguide.congress.gov)

for_congress_and_chamber
---------------

members.for_congress_and_chamber works much the same way, but returns a list. Congress and chamber
are required parameters, with state and district being optional.

    >>> for member in nytcongressapi.members.for_congress_and_chamber(111, 'house', 'PA'):
    ...     print member.name
    Jason Altmire
    Robert Brady

A call to members.for_congress_and_chamber that has no state or district will return all members who have served
in that congress and chamber. A call that includes district but not state will return an error.
python-nytcongressapi
=====================

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
    
    >>> nytcongress.api_key = 'nytcongress-api-key'

-------------------
member methods
-------------------

Member methods are done in a style vaguely reminiscent of Django's ORM: get retrieves a single object 
while filter retrieves multiple objects.

    * members.get                   - returns a single member
    * members.filter                - returns zero or more members
    

get
---------------
    
members.get takes a single parameter to lookup a single member of the House or Senate.

The parameter is:
    * id (the official ID from http://bioguide.congress.gov)

    >>> member = nytcongress.members.get(id="G000555")
    >>> print member.name
    Kirsten Gillibrand


filter
------------------------

members.filter works much the same way, but returns a list. Congress and chamber
are required parameters, with state and district being optional.

    >>> for member in nytcongress.members.filter(congress=111, chamber='house', state='PA'):
    ...     print member.name
    Jason Altmire
    Robert Brady

A call to members.filter that has no state or district will return all members who have served
in that congress and chamber. A call that includes district but not state will return an error.

-------------------
votes methods
-------------------

The only votes methods currently supported are get, which returns information about a single vote in either
the House or the Senate, and nominations, which retrieves Senate nomination votes for a given congress. 
Forthcoming methods will include the latest votes in a chamber.

get
---------------

votes.get takes four parameters: the congress, chamber, session and roll call numbers.

    >>> vote = nytcongress.votes.get(congress=111, chamber='house', session=1, roll_call=74)
    >>> print vote.question
    On Motion to Suspend the Rules and Pass

nominations
---------------
votes.nominations takes a single parameter, congress.

    >>> for vote in nytcongress.votes.nominations(congress=111):
    ...     print vote.description
    Confirmation Hilda L. Solis of California, to be Secretary of Labor

-------------------
committee methods
-------------------

Committee methods are done in a style vaguely reminiscent of Django's ORM: get retrieves a single object 
while filter retrieves multiple objects.

    * committees.get                   - returns a single committees
    * committees.filter                - returns zero or more committees


get
---------------
    
committees.get takes three parameters to lookup a single committee of the House or Senate.

The parameters are, in order:
    * the congress (an integer)
    * the chamber (a string)
    * the four-letter committee code (a string)

    >>> committee = nytcongress.committees.get(111,'senate', 'SSAF')
    >>> print committee.committee
    Committee on Agriculture


filter
------------------------

committees.filter works much the same way, but returns a list. Congress and chamber
are required parameters.

    >>> for committee in nytcongress.committees.filter(congress=111, chamber='house'):
    ...     print committee.name
    Committee on Agriculture
    Committee on Appropriations
    ...
    Committee on Ways and Means

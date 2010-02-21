python-nytcongressapi
=====================

A Python wrapper for The New York Times Congress API, which provides information about members, roles and votes for the United States Congress. (http://developer.nytimes.com/docs/congress_api). This wrapper borrows heavily in its design from the python-sunlightapi project by James Turk.
(http://github.com/sunlightlabs/python-sunlightapi)

python-nytcongressapi is a project of Derek Willis <dwillis@gmail.com> (c) 2010.

Contributors: Chris Amico (http://github.com/eyeseast)

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
API key to be defined. At this time the library supports version 3 of the New York
Times Congress API.

(If you do not have an API key visit http://developer.nytimes.com/ to
register for one.)

Import ``nytcongress`` from ``nytcongressapi``:
    
    >>> from nytcongressapi import nytcongress, NYTCongressApiError
    
And set your API key:
    
    >>> nytcongress.api_key = YOUR_API_KEY

-------------------
member methods
-------------------

Member methods are done in a style vaguely reminiscent of Django's ORM: get retrieves a single object 
while filter retrieves multiple objects.

    * members.get                   - returns a single member
    * members.filter                - returns zero or more members
    * members.vote_type             - returns a list of members
    

get
---------------
    
members.get takes a single parameter to lookup a single member of the House or Senate.

The parameter is:
    * id (the official ID from http://bioguide.congress.gov)

    >>> member = nytcongress.members.get(id="G000555")
    >>> member
    <Member: Kirsten Gillibrand (D-NY)>


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

floor
------------------------
members.floor requires a single parameter - a member's bioguide id - and returns a list of floor appearances
as tracked by C-SPAN.

    >>> appearances = nytcongress.members.floor(id="G000555")
    >>> for appearance in appearances:
    ...     print appearance.date
    2009-04-30
    2009-04-28

bills
------------------------
members.bills requires two parameters - a member's bioguide id and either 'introduced' or 'updated' depending on which type of result is desired - and returns a list of bills sponsored by that member. Passing 'introduced' returns the 20 most recently introduced bills and 'updated' returns the 20 most recently updated bills.

    >>> bills = bills = nytcongress.members.bills(id="G000555", bill_type="introduced")
    >>> for bill in bills:
    ...     print bill.bill_number
    S.1438
    S.1394


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
bills methods
-------------------

The bill methods currently supported are get, which returns information about a single bill in a given chamber
and congress, filter, which returns information about the latest 20 bills in a given chamber and congress, with sort order determined by a third parameter (bill_type), and sponsor_compare, which takes two member ids, a congress and chamber and returns a list of bills that both members have co-sponsored.

get
---------------

bills.get takes two parameters: the congress and url_number (a slugified version of the bill number).

    >>> bill = nytcongress.bills.get(congress=111, bill_slug='hr2581')
    >>> print bill.title
    To amend the Public Health Service Act to provide for a health survey regarding Native Hawaiians and other Pacific Islanders.

filter
---------------
bills.filter takes three parameters: the congress, chamber and bill_type, which is either 'introduced' or 'updated'.

    >>> bills = nytcongress.bills.filter(111,'senate','introduced')
    >>> for bill in bills:
    ...     print bill.title
    A bill to amend the Public Health Service Act to improve the health of children and reduce the occurrence of sudden unexpected infant death and to enhance public health activities related to stillbirth.

member_compare
---------------
bills.member_compare takes four parameters: two member IDs (as represented by their Bioguide IDs), the congress and lower case chamber name.

	>>> bills = nytcongress.bills.sponsor_compare('G000555','A000360', 111,'senate')
	>>> len(bills)
	>>> 25

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
    
    
a committee response also provides lists of current and (if applicable) former members for that
committee during that congress:

    >>> committee = nytcongress.committees.get(111,'senate', 'SSAF')
    >>> for member in committee.current_members:
    ...     print member.name
    Tom Harkin
    Patrick Leahy

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
    

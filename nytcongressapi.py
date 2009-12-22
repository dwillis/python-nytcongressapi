""" Python library for interacting with The New York Times Congress API.
 
The New York Times Congress API provides information on members, roles and votes
in the U.S. House and U.S. Senate. More details at http://developer.nytimes.com/docs/congress_api.
This wrapper borrows heavily in its design from the python-sunlightapi project by James Turk.

Pre-requisites: simplejson (except if using Python > 2.6)
"""
 
__author__ = "Derek Willis (dwillis@gmail.com)"
__version__ = "0.2.0"
__copyright__ = "Copyright (c) 2009 Derek Willis"
__license__ = "MIT"
 
import urllib, urllib2
try:
    import json
except ImportError:
    import simplejson as json

class NYTCongressApiError(Exception):
    """ Exception for New York Times Congress API errors """

class NYTCongressApiObject(object):
    def __init__(self, d):
        self.__dict__ = d
    
    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.__str__())
    
    def __str__(self):
        return ''


class Member(NYTCongressApiObject):   
    def __str__(self):
        return "%s (%s-%s)" % (unicode(self.name).encode('utf-8'), self.roles[0]['party'], self.roles[0]['state'])

    @property
    def party(self):
        return self.roles[0]['party']

    @property
    def state(self):
        return self.roles[0]['state']

class MemberTotal(NYTCongressApiObject):
    def __str__(self):
        return '%s' % unicode(self.name).encode('utf-8')

class MemberRole(NYTCongressApiObject):
    def __str__(self):
        return '%s' % unicode(self.name).encode('utf-8')

class Vote(NYTCongressApiObject):
    def __str__(self):
        return 'Roll Call Vote %s in the %s Congress' % (self.roll_call, self.congress)

class Bill(NYTCongressApiObject):
    def __str__(self):
        return '%s' % unicode(self.number)

class Committee(NYTCongressApiObject):
    def __init__(self, d):
        self.__dict__ = d
        self.members = [MemberRole(m) for m in getattr(self, 'members', [])]
        
    def __str__(self):
        try:
            return '%s' % self.name
        except:
            return '%s' % self.committee

class Comparison(NYTCongressApiObject):
    """
    A comparison of how often two members of Congress voted
    in a given chamber and congress.
    """
    # storing these as attributes to save API requests
    _first_member = None
    _second_member = None

    def __init__(self, d):
        self.__dict__ = d

    @property
    def first_member(self):
        if self._first_member is not None:
            return self._first_member
        else:
            self._first_member = nytcongress.members.get(self.first_member_id)
            return self._first_member
    
    @property
    def second_member(self):
        if self._second_member is not None:
            return self._second_member
        else:
            self._second_member = nytcongress.members.get(self.second_member_id)
            return self._second_member

    def __str__(self):
        if self._first_member and self._second_member:
            return '%s and %s agree %s percent of the time' % (self.first_member, self.second_member, self.agree_percent)
        else:
            return '%s%% agreement' % (self.__class__.__name__, self.agree_percent)


# namespaces #
 
class nytcongress(object):
 
    api_key = None
    
    @staticmethod
    def _apicall(path, params):
        # fix to allow for keyword args
        if params:
            url = "http://api.nytimes.com/svc/politics/v2/us/legislative/congress/%s.json?api-key=%s&%s" % (path, nytcongress.api_key, urllib.urlencode(params))
        else:
            url = "http://api.nytimes.com/svc/politics/v2/us/legislative/congress/%s.json?api-key=%s" % (path, nytcongress.api_key)
        if nytcongress.api_key is None:
            raise NYTCongressApiError('You did not supply an API key')
        try:
            response = urllib2.urlopen(url).read()
            return json.loads(response)['results']
        except urllib2.HTTPError, e:
            raise NYTCongressApiError(e.read())
        except (ValueError, KeyError), e:
            raise NYTCongressApiError('Invalid Response')
 
    class members(object):
        @staticmethod
        def get(id):
            path = 'members/%s' % id
            result = nytcongress._apicall(path, None)[0]
            return Member(result)
        
        @staticmethod
        def filter(congress, chamber, state=None, district=None):
            path = '%s/%s/members' % (congress, chamber)
            if state and district:
                params = {'state': state, 'district': district }
            elif state:
                params = {'state': state}
            elif district:
                raise NYTCongressApiError('You must supply a state and district')
            else:
                params=None
            results = nytcongress._apicall(path, params)[0]
            return [MemberRole(m) for m in results['members']]
            
        @staticmethod
        def floor(id):
            path = 'members/%s/floor_appearances' % id
            results = nytcongress._apicall(path, None)[0]['appearances']
        
        @staticmethod
        def bills(id, bill_type):
            path = 'members/%s/bills/%s' % (id, bill_type)
            results = nytcongress._apicall(path, None)[0]['bills']
            return [Bill(b) for b in results]
        
        @staticmethod
        def totals(total, congress, chamber):
            path = '%s/%s/%s_votes' % (congress, chamber, total)
            results = nytcongress._apicall(path, None)[0]['members']
            return [MemberTotal(m) for m in results]

        @staticmethod
        def compare(first, second, congress, chamber):
            path = 'members/%s/compare/%s/%s/%s' % (first, second, congress, chamber)
            results = nytcongress._apicall(path, None)[0]
            return Comparison(results)
    
    class votes(object):
        @staticmethod
        def get(congress, chamber, session, roll_call):
            path = '%s/%s/sessions/%s/votes/%s' % (congress, chamber, session, roll_call)
            result = nytcongress._apicall(path, None)['votes']['vote']
            return Vote(result)
            
        @staticmethod
        def nominations(congress):
            path = '%s/nominations' % congress
            results = nytcongress._apicall(path, None)[0]['votes']
            return [Vote(r) for r in results]
    
    class committees(object):
        @staticmethod
        def get(congress, chamber, comm):
            path = "%s/%s/committees/%s" % (congress, chamber, comm)
            result = nytcongress._apicall(path, None)[0]
            return Committee(result)
        
        @staticmethod
        def filter(congress, chamber):
            path = "%s/%s/committees" % (congress, chamber)
            results = nytcongress._apicall(path, None)[0]
            ch = results['chamber']
            return [Committee(c) for c in results['committees']]
    
    class bills(object):
        @staticmethod
        def get(congress, bill_slug):
            path = "%s/bills/%s" % (congress, bill_slug)
            result = nytcongress._apicall(path, None)[0]
            return Bill(result)
        
        @staticmethod
        def filter(congress, chamber, bill_type):
            path = "%s/%s/bills/%s" % (congress, chamber, bill_type)
            results = nytcongress._apicall(path, None)[0]
            return [Bill(b) for b in results['bills']]
        
        

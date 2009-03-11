""" Python library for interacting with The New York Times Congress API.
 
The New York Times Congress API provides information on members, roles and votes
in the U.S. House and U.S. Senate. More details at http://developer.nytimes.com/docs/congress_api.
This wrapper borrows heavily in its design from the python-sunlightapi project by James Turk.

Pre-requisites: simplejson (except if using Python > 2.6)
"""
 
__author__ = "Derek Willis (dwillis@gmail.com)"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2009 Derek Willis"
__license__ = "BSD"
 
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
 
class Member(NYTCongressApiObject):
    def __repr__(self):
        return u'%s' % self.name

class MemberRole(NYTCongressApiObject):
    def __repr__(self):
        return u'%s' % self.name

class Vote(NYTCongressApiObject):
    def __repr__(self):
        return u'Roll Call Vote %s in the %s Congress' % (self.roll_call, self.congress)

class Committee(NYTCongressApiObject):
    def __unicode__(self):
        return u'%s' % self.name

class Committees(NYTCongressApiObject):
    def __init__(self, d):
        self.__dict__ = d

    def __unicode__(self):
        return u'%s - %s for %s' % (self.congress_id, self.chamber)


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
            results = nytcongress._apicall(path, params)[0]
            return [MemberRole(m) for m in results['members']]
    
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
import re
import urllib
import urllib2
import httplib
import socket
import unicodedata
from xml.etree import ElementTree

__author__ = "Michael Stephens <mstephens@sunlightfoundation.com>"
__copyright__ = "Copyright (c) 2011 Sunlight Labs"
__license__ = "BSD"
__version__ = '0.3.4'

# Timeout in seconds to wait for response from API
TIMEOUT = None

class NimspApiError(Exception):
    pass


class NimspApiObject(object):

    def __init__(self, xml):
        for key, value in xml.items():
            setattr(self, key, value)

        # Convert dollar/year/numeric attrs from strings to ints
        for key, value in self.__dict__.items():
            if re.match('^percent_', key):
                setattr(self, key, value)
            elif re.match('^.*_(dollars|records|recipients)$|year', key):
                setattr(self, key, int(value))

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.__dict__)


class Candidate(NimspApiObject):

    def __str__(self):
        return '%s (%s)' % (self.candidate_name, self.state_postal_code)

    def sectors(self, **params):
        return nimsp.candidates.sectors(self.imsp_candidate_id, **params)

    def businesses(self, **params):
        return nimsp.candidates.businesses(self.imsp_candidate_id, **params)

    def industries(self, **params):
        return nimsp.candidates.industries(self.imsp_candidate_id, **params)

    def top_contributors(self, **params):
        return nimsp.candidates.top_contributor(self.imsp_candidate_id,
                                                **params)


class Sector(NimspApiObject):

    def __str__(self):
        return self.sector_name


class Business(NimspApiObject):

    def __str__(self):
        return self.business_name


class Industry(NimspApiObject):

    def __str__(self):
        return self.industry_name


class Contributor(NimspApiObject):

    def __str__(self):
        return self.contributor_name


class Office(NimspApiObject):

    def __str__(self):
        return self.office


class State(NimspApiObject):

    def __str__(self):
        return self.state_name


class District(NimspApiObject):

    def __str__(self):
        return "%s %s" % (self.state_name, self.district)


def strip_accents(s):
    if isinstance(s, unicode):
        return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
    return s


class nimsp(object):

    apikey = None
    useragent = 'python-nimsp ' + __version__

    @staticmethod
    def _apicall(method, params):
        if nimsp.apikey is None:
            pass

        cleaned = {}
        for key, param in params.items():
            cleaned[key] = strip_accents(param)

        url = 'http://api.followthemoney.org/%s.php?key=%s&%s' % (
            method, nimsp.apikey, urllib.urlencode(cleaned))

        try:
            request = urllib2.Request(url,
                                      headers={'User-Agent': nimsp.useragent})
            response = urllib2.urlopen(request, None, TIMEOUT)
            xml = ElementTree.fromstring(response.read())

            if xml.tag == 'error':
                raise NimspApiError(xml.attrib['text'])

            return xml
        except urllib2.HTTPError, e:
            raise NimspApiError(e.read())
        except urllib2.URLError, e:
            raise NimspApiError(e.reason)
        except ValueError, e:
            raise NimspApiError('Invalid Response')
        except httplib.BadStatusLine, e:
            raise NimspApiError('Invalid HTTP status response')
        except socket.timeout, e:
            raise NimspApiError('Request timed out')

    class candidates(object):

        @staticmethod
        def list(**params):
            xml = nimsp._apicall('candidates.list', params)
            return [Candidate(c) for c in xml.findall('candidate')]

        @staticmethod
        def sectors(candidate_id, **params):
            params['imsp_candidate_id'] = candidate_id
            xml = nimsp._apicall('candidates.sectors', params)
            return [Sector(s) for s in xml.findall('candidate_sector')]

        @staticmethod
        def businesses(candidate_id, **params):
            params['imsp_candidate_id'] = candidate_id
            xml = nimsp._apicall('candidates.businesses', params)
            return [Business(b) for b in xml.findall('candidate_business')]

        @staticmethod
        def industries(candidate_id, **params):
            params['imsp_candidate_id'] = candidate_id
            xml = nimsp._apicall('candidates.industries', params)
            return [Industry(i) for i in xml.findall('candidate_industry')]

        @staticmethod
        def top_contributors(candidate_id, **params):
            params['imsp_candidate_id'] = candidate_id
            xml = nimsp._apicall('candidates.top_contributors', params)
            return [Contributor(c) for c in xml.findall('top_contributor')]

    class states(object):
        class offices(object):

            @staticmethod
            def list(**params):
                xml = nimsp._apicall('states.offices', params)
                return [Office(o) for o in xml.findall('state_office')]

            @staticmethod
            def businesses(**params):
                xml = nimsp._apicall('states.offices.businesses', params)
                return [Business(s) for s in
                        xml.findall('state_offices_business')]

            @staticmethod
            def industries(**params):
                xml = nimsp._apicall('states.offices.industries', params)
                return [Industry(i) for i in
                        xml.findall('state_offices_industry')]

            @staticmethod
            def districts(state, year, **params):
                params['state'] = state
                params['year'] = year
                xml = nimsp._apicall('states.offices.districts', params)
                return [District(d) for d in
                        xml.findall('state_office_district')]

            @staticmethod
            def sectors(**params):
                xml = nimsp._apicall('states.offices.sectors', params)
                return [Sector(s) for s in
                        xml.findall('state_offices_sector')]

        @staticmethod
        def top_contributors(state, year, **params):
            params['state'] = state
            params['year'] = year
            xml = nimsp._apicall('states.top_contributors', params)
            return [Contributor(c) for c in xml.findall('top_contributor')]

    class elections(object):
        class state(object):

            @staticmethod
            def list(**params):
                xml = nimsp._apicall('base_level.elections.state.list',
                                     params)
                return [State(s) for s in xml.findall('state_list')]

        class year(object):

            @staticmethod
            def list(**params):
                xml = nimsp._apicall('base_level.elections.year.list',
                                     params)
                return [int(y.attrib['year']) for y in
                        xml.findall('year_list')]

        class industries(object):

            @staticmethod
            def list(**params):
                xml = nimsp._apicall('base_level.industries.list',
                                     params)
                return [Industry(i) for i in xml.findall('business_detail')]

# coding: utf-8
import requests
from BeautifulSoup import BeautifulSoup, SoupStrainer
from urlparse import urlparse

blacklist=[
           '/acl_users/',
           '/search_rss',
           '/login_form',
           '/login',
           '/request_login_pre',
           '/search.html',
           '/request_login',
           '/search.json',
           '/RSS',
           '/search',
           '/@@flexijson_view',
           '/@@usergroup-userprefs',
           '/awstats_hitcounter_view',
           '/portal_kss/',
           '/login_failed',
           '/search_form',
           '/contact-info',
           '/@@user',
           '/@@user-information',
          ]


def counter(path, pattern, hits=False):
    """ usage
    counter(path, pattern)
    # returns the number of views for a given path
    counter(path, pattern, hits=True)
    # returns the number of hits for a given path
    """
    url = pattern.format(path)
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text)

    # scrape the bold text which contains the path on the page
    scrape_pattern_b = soup.find('b', text=path)

    # Get all rows after the matched path
    # in the interface
    trs = scrape_pattern_b.findAllNext('tr')
    hit_count = 0 # only used when tracking hits

    for tr in trs:
        tds = tr.findAll('td')
        attrs_ = getattr(tds[0].a,'attrs',None)
        # if there is no a tag or it has no attr
        # then just move on
        if attrs_:
            attrs = dict(attrs_)
            href = attrs['href']
            url = urlparse(href)                                                                                                                                     
            # return the count in the next column
            # but only if the url matches the 
            # path we're working with
            if url.path == path and hits == False:
                return int(tds[1].text)
            
            if hits == True:
                hit_count = hit_count + int(tds[1].text)

    if hits == True:
        return hit_count

    return 0

def get_urls(url,blacklist=blacklist):
    r = requests.get(url)
    _links = []
    # Get the links
    for link in BeautifulSoup(r.text, parseOnlyThese=SoupStrainer('a')):
        if link.get('target') in ['url',]:
           _links.append(link['href'])
    # Filter links 
    for blacklistitem in blacklist:
        _links = [linkitem for linkitem in _links 
               if blacklistitem not in linkitem]
    return _links[:10]

# keep this code here so we can do standalone testing
if __name__ == '__main__':
    pattern = 'http://rmportal.net/awstats/awstats.pl?urlfilter={0}&urlfilterex=&output=urldetail&config=www.rmportal.net'
    path = '/news-events/news-usaid-rmp/farming-gender-neutral-q-a-ann-tutwiler'
    url = 'http://rmportal.net/awstats/awstats.pl?urlfilterex=&config=www.rmportal.net&framename=mainright&output=urldetail'
#    print "views:",counter(path,pattern)
#   print "hits:",counter(path,pattern,hits=True)
    print get_urls(url) 


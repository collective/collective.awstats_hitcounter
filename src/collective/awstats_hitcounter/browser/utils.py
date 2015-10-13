# coding: utf-8
import requests
from os import getenv
from AccessControl import Unauthorized
from BeautifulSoup import BeautifulSoup, SoupStrainer
from urlparse import urlparse
from plone import api

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

type_whitelist = ['News Item','Page','Link','File']

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

def get_urls(url,blacklist=blacklist,limit=10):
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
    if limit:
        return _links[:limit]


def filter_urls(urls,type_white_list=type_whitelist,items_to_show=None,
              prevent_direct_downloads=True,read_from_the_global_registry=True):

        # The following values are available via the global registry:
        # url_of_popular_page,prevent_direct_downloads
        # black_list,type_white_list

    if read_from_the_global_registry:
           prevent_direct_downloads = api.portal.get_registry_record(
                            'awstats_hitcounter.prevent_direct_downloads')
           black_list = api.portal.get_registry_record(
                            'awstats_hitcounter.black_list')
           type_white_list = api.portal.get_registry_record(
                            'awstats_hitcounter.type_white_list')
 

    if prevent_direct_downloads:
        popular_urls_no_downloads = []
        for p_url in urls:
            if p_url.endswith('/at_download/file'):
                p_url = p_url.replace('at_download/file', "")
                popular_urls_no_downloads.append(p_url)
            else:
                popular_urls_no_downloads.append(p_url)
        urls = popular_urls_no_downloads  

    popular_urls_remove_imagethumbs = []
    for p_url in urls:
        if p_url.endswith('/image_thumb'):
            p_url = p_url.replace('image_thumb', "")
            popular_urls_remove_imagethumbs.append(p_url)
        else:
            popular_urls_remove_imagethumbs.append(p_url)
    urls = popular_urls_remove_imagethumbs  

    if getenv('DUMP_RAW_AWSTATS_URLS',None):
        return [{'title':url,'url':url} for url in urls]
    popular_urls_ = [(get_content_by_path(urlparse(p_url).path),p_url) 
                         for p_url in urls
                             if get_content_by_path(
                                  urlparse(p_url).path
                                  )]



    popular_urls = []
    for p_url in popular_urls_:
        if p_url[0]:
        # Check against white list while filtering out objects which
        # don't have titles
            try:
                if p_url[0].Type() in type_white_list:
                    popular_urls.append({'title':p_url[0].Title(),
                                 'url':p_url[1]})

            except AttributeError:
                print "bad url: %s" % p_url[1]
                
    # if needed limit by the number of "items to show" parameter
    if items_to_show:
        if len(popular_urls) > items_to_show:
            return popular_urls[:items_to_show]
    return popular_urls

   # return urls


def get_content_by_path(path):
    output = None
    print "path:",path
    try:
        output = api.content.get(path)
    except Unauthorized:
        pass
    return output

# keep this code here so we can do standalone testing
if __name__ == '__main__':
    pattern = 'http://example.net/awstats/awstats.pl?urlfilter={0}&urlfilterex=&output=urldetail&config=www.example.net'
    path = '/news-events/news-usaid-rmp/farming-gender-neutral-q-a-ann-tutwiler'
    path = '/'
    print "views:",counter(path,pattern)
    print "hits:",counter(path,pattern,hits=True)
    url = 'http://example.net/awstats/awstats.pl?urlfilterex=&config=www.example.net&framename=mainright&output=urldetail'
#    print "views:",counter(path,pattern)
#   print "hits:",counter(path,pattern,hits=True)
    print get_urls(url) 

"""
Bundles functions needed to target text content and validate the input.
"""


## This file is available from https://github.com/adbar/courlan
## under GNU GPL v3 license

import re

from urllib.parse import urlparse


# content filters
WORDPRESS_CONTENT_FILTER = re.compile(r'/(?:page|seite|user|search|gallery|gall?erie|labels|archives|uploads|modules|attachment)/', re.IGNORECASE)
WORDPRESS_CONTENT_FILTER_2 = re.compile(r'/(?:tags?|schlagwort|category|cat|kategorie|kat|auth?or)/[^/]+$', re.IGNORECASE)
PARAM_FILTER = re.compile(r'\.(atom|json|css|xml|js|jpg|jpeg|png|gif|tiff|pdf|ogg|mp3|m4a|aac|avi|mp4|mov|webm|flv|ico|pls|zip|tar|gz|iso|swf)\b', re.IGNORECASE)  # , re.IGNORECASE (?=[&?])
PATH_FILTER = re.compile(r'.{0,5}/(impressum|index)(\.[a-z]{3,4})?/?$', re.IGNORECASE)
ADULT_FILTER = re.compile(r'\b(?:adult|amateur|arsch|cams?|cash|fick|gangbang|incest|porn|sexyeroti[ck]|sexcam|swinger|xxx|bild\-?kontakte)\b', re.IGNORECASE) # live|sex|ass|orgasm|cams|

# language filter
URL_LANG_FILTER = re.compile(r'/([a-z]{2,3})([_-][A-Za-z]{2,3})?/', re.IGNORECASE)

# navigation/crawls
NAVIGATION_FILTER = re.compile(r'/(archives|auth?or|cat|category|kat|kategorie|page|schlagwort|seite|tags?|topics?|user)/', re.IGNORECASE) # ?p=[0-9]+$
NOTCRAWLABLE = re.compile(r'/(login|impressum|imprint)/?$|/login\?|/(javascript:|mailto:|tel\.?:|whatsapp:)', re.IGNORECASE)
# |/(www\.)?(facebook\.com|google\.com|instagram\.com|twitter\.com)/

# document types
WHITELISTED_EXTENSIONS = ('.amp', '.asp', '.aspx', '.cfm', '.cgi', '.htm', 'html', '.shtml', '.jsp', '.php', '.pl', '.txt')


def basic_filter(url):
    '''Filter URLs based on basic formal characteristics'''
    if not url.startswith('http') or len(url) >= 500 or len(url) < 10:
        return False
    return True


def extension_filter(urlpath):
    '''Filter based on file extension'''
    if re.search(r'\.[a-z]{2,5}$', urlpath) and not urlpath.endswith(WHITELISTED_EXTENSIONS):
        return False
    return True


def lang_filter(url, language):
    '''Heuristic targeting internationalization'''
    if language is not None:
        match = URL_LANG_FILTER.search(url)
        if match:
            if language == 'de' and match.group(1).lower() not in ('de', 'deu'):
                return False
            elif language == 'en' and match.group(1).lower() not in ('en', 'eng'):
                return False
            elif language != match.group(1).lower()[:2]:
                return False
    return True


def spam_filter(url):
    '''Try to filter out spam and adult websites'''
    # TODO: to improve!
    #for exp in (''):
    #    if exp in url:
    #        return False
    if ADULT_FILTER.search(url):
        return False
    # default
    return True


def type_filter(url, strict=False, with_nav=False):
    '''Make sure the target URL is from a suitable type (HTML page with primarily text)'''
    # directory
    #if url.endswith('/'):
    #    return False
    try:
        # feeds
        if url.endswith(('/feed', '/rss')):
            raise ValueError
        # embedded content
        if re.search(r'/oembed\b', url, re.IGNORECASE):
            raise ValueError
        # wordpress structure
        if WORDPRESS_CONTENT_FILTER.search(url) or WORDPRESS_CONTENT_FILTER_2.search(url):
            if with_nav is not True or not is_navigation_page(url):
                raise ValueError
        # hidden in parameters
        if strict is True and PARAM_FILTER.search(url):
            raise ValueError
        # not suitable
        if re.match(r'https?://banner\.|https?://add?s?\.', url, re.IGNORECASE):
            raise ValueError
        if re.search(r'\b(?:doubleclick|tradedoubler|livestream)\b|/(?:live|videos?)/', url, re.IGNORECASE):
            raise ValueError
        if strict is True and re.search(r'\b(?:live|videos?)\b', url, re.IGNORECASE):
            raise ValueError
    except ValueError:
        return False
    # default
    return True


def validate_url(url):
    '''Parse and validate the input'''
    try:
        parsed_url = urlparse(url)
    except ValueError:
        return False, None
    if bool(parsed_url.scheme) is False or parsed_url.scheme not in ('http', 'https'):
        return False, None
    if len(parsed_url.netloc) < 5 or \
       (parsed_url.netloc.startswith('www.') and len(parsed_url.netloc) < 8):
        return False, None
    # if validators.url(parsed_url.geturl(), public=True) is False:
    #    return False
    # default
    return True, parsed_url


def is_navigation_page(url):
    '''Determine if the URL is related to navigation and overview pages
       rather than content pages, e.g. /page/1 vs. article page.'''
    return bool(NAVIGATION_FILTER.search(url))


def is_not_crawlable(url):
    '''Run tests to check if the URL may lead to deep web or pages
       generally not usable in a crawling context.'''
    return bool(NOTCRAWLABLE.search(url))

"""Check how AI and search crawlers see a website.

Loads the page once without running JavaScript (the way crawlers first fetch it), reports whether a firewall
turned the request away, counts the visible words, lists the JSON-LD types and reads robots.txt
for the AI and search crawlers. Two GET requests per site, nothing else.

Usage: python3 check_site.py https://www.yoursite.com [https://another-site.com/agent/page ...]
Standard library only (Python 3.9+). If the package `protego` is installed (pip install protego),
robots.txt is read the way Google, Bing and RFC 9309 read it: the longest matching rule wins and
`*` and `$` work as wildcards. Python's built-in parser takes the first matching rule and does not
know wildcards, which can give a different answer for files that use them.
"""
import re
import ssl
import sys
import urllib.error
import urllib.request
import urllib.robotparser
from urllib.parse import urlparse

try:
    from protego import Protego
except ImportError:
    Protego = None

BROWSER = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
           '(KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36')

# (crawler, operator, what it is used for). The October 2026 study used the first ten.
CRAWLERS = [
    ('OAI-SearchBot', 'OpenAI', 'ChatGPT search'),
    ('ChatGPT-User', 'OpenAI', 'opens pages for a ChatGPT user; OpenAI: robots.txt may not apply'),
    ('GPTBot', 'OpenAI', 'model training'),
    ('PerplexityBot', 'Perplexity', 'Perplexity search'),
    ('ClaudeBot', 'Anthropic', 'model training'),
    ('bingbot', 'Microsoft', 'Bing search and Copilot'),
    ('Googlebot', 'Google', 'Google Search, AI Overviews, AI Mode'),
    ('Perplexity-User', 'Perplexity', 'opens pages for a Perplexity user; Perplexity: generally ignores robots.txt'),
    ('Claude-SearchBot', 'Anthropic', 'Claude search'),
    ('Claude-User', 'Anthropic', 'opens pages for a Claude user'),
    ('Google-Extended', 'Google', 'Gemini training and grounding in Gemini Apps, not Google Search'),
]

ORG_TYPES = {'Organization', 'LocalBusiness', 'RealEstateAgent', 'Person', 'ProfessionalService',
             'AccountingService', 'FinancialService', 'LegalService', 'Corporation'}

CHECK_PAGE = re.compile(r'Just a moment\.\.\.|Checking your browser|Vercel Security Checkpoint|'
                        r'Verify you are human|cf-chl|px-captcha', re.I)


def fetch(url, limit=1_500_000):
    req = urllib.request.Request(url, headers={'User-Agent': BROWSER, 'Accept': 'text/html,*/*',
                                               'Accept-Language': 'en-US'})
    try:
        with urllib.request.urlopen(req, timeout=20, context=ssl.create_default_context()) as r:
            return r.status, r.geturl(), r.read(limit).decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        try:
            body = e.read(200_000).decode('utf-8', 'replace')
        except Exception:
            body = ''
        return e.code, url, body
    except Exception as e:
        return None, url, type(e).__name__


def words_without_js(html):
    h = re.sub(r'(?is)<(script|style|noscript|template|svg|head)[^>]*>.*?</\1>', ' ', html)
    h = re.sub(r'(?s)<!--.*?-->', ' ', h)
    t = re.sub(r'<[^>]+>', ' ', h)
    t = re.sub(r'&[a-z#0-9]+;', ' ', t)
    return len(re.findall(r'[A-Za-z]{2,}', t))


def jsonld_types(html):
    blocks = re.findall(r'(?is)<script[^>]+ld\+json[^>]*>(.*?)</script>', html)
    return sorted(set(re.findall(r'"@type"\s*:\s*"([A-Za-z]+)"', ' '.join(blocks))))


def blocked_by_robots(robots, url):
    if Protego is not None:
        rp = Protego.parse(robots)
        return lambda bot: not rp.can_fetch(url, bot)
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(robots.splitlines())
    return lambda bot: not rp.can_fetch(bot, url)


def check(site):
    url = site if site.startswith('http') else 'https://' + site
    status, final, html = fetch(url)
    u = urlparse(final or url)
    base = f'{u.scheme}://{u.netloc}'
    rb_status, _, robots = fetch(base + '/robots.txt', 300_000)
    blocked = blocked_by_robots(robots if rb_status == 200 else '', final or url)

    print(f'\n{final or url}  (page HTTP {status}, robots.txt HTTP {rb_status}, '
          f'robots.txt rules read {"per RFC 9309" if Protego else "with Python’s built-in parser"})')
    if status is None:
        print(f'  No answer ({html}). Check that the site is live and the address in your listings is right.')
    elif status != 200 or (CHECK_PAGE.search(html[:50_000]) and words_without_js(html) < 50):
        print('  The request was turned away or got a check page instead of the site. Crawlers fetch the page '
              'without running JavaScript first, so they only get through if your firewall lets them. Ask whoever runs it whether '
              'OAI-SearchBot, ChatGPT-User, PerplexityBot, Perplexity-User, Claude-SearchBot and Claude-User pass.')
    if rb_status == 200:
        for name, operator, purpose in CRAWLERS:
            print(f'  {"BLOCKED" if blocked(name) else "allowed":8} {name:17} {operator:11} {purpose}')
    elif rb_status == 404:
        print('  No robots.txt (HTTP 404): every crawler may read the site.')
    else:
        print(f'  robots.txt could not be read (HTTP {rb_status}), so its rules are unknown from here.')
    if status == 200:
        words = words_without_js(html)
        types = jsonld_types(html)
        print(f'  Words on the page without JavaScript: {words}'
              + ('  <- AI crawlers that do not run JavaScript see an (almost) empty page' if words < 50 else ''))
        print(f'  JSON-LD types: {", ".join(types) or "none"}'
              + ('' if set(types) & ORG_TYPES else '  <- nothing names the agent or business'))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for s in sys.argv[1:]:
        check(s)

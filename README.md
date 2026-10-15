# Can ChatGPT and Perplexity read real estate agent websites? 197 US agents checked (October 2026)

Original data collected by [createwithlogic](https://createwithlogic.com) on October 13 and 14, 2026.
Full write-up with context and sources: **https://createwithlogic.com/ai-readiness-real-estate-agent-websites**

## What we checked

On October 14, 2026 we pulled businesses with a website from Google Maps for "real estate agent" in Austin, Dallas, Houston, Miami, Atlanta, Charlotte, Phoenix, Denver, Nashville and Seattle and kept agents, teams and agencies: 197 websites.

For each site we:

1. loaded the address from the Google listing with a common browser user agent and without running JavaScript, and recorded whether it answered with a page, a firewall check page or nothing,
2. read `robots.txt` for ten crawlers (OAI-SearchBot, ChatGPT-User, GPTBot, PerplexityBot, ClaudeBot, bingbot, Googlebot, Perplexity-User, Claude-SearchBot and Claude-User) with a parser that follows the robots.txt standard, RFC 9309 ([Protego](https://github.com/scrapy/protego)),
3. counted the visible words without JavaScript,
4. looked for structured data (JSON-LD) that names the agent or firm.

Every site that showed no page the first time was asked again about 20 minutes later, one site at a time. 4 sites on one website platform had first answered HTTP 429 (too many requests) and then showed their pages, so they count as answered. 8 sites on another platform answered both times with a notice page (HTTP 218) while two other sites on that platform showed their pages, so they count as not checked. That leaves 189 checked sites. Pages with fewer than 50 words were loaded again in a real browser.

## Results

| Check | Result |
|---|---|
| Sites that turned a request without JavaScript away | 23 of 189 (12.2%): 16 Cloudflare check pages, 3 Vercel check pages, 4 refusals |
| Sites that did not answer | 3 of 189 |
| Sites that block OAI-SearchBot (ChatGPT search) | 3 of 163 (1.8%), 2 of them not live |
| Sites that block PerplexityBot (Perplexity search) | 4 of 163 (2.5%) |
| Sites that block GPTBot (OpenAI training) | 10 of 163 (6.1%) |
| Home page with fewer than 50 words without JavaScript | 16 of 163 (9.8%) |
| Text only appears with JavaScript | 6 of 163 (3.7%) |
| No structured data naming the agent or firm | 80 of 163 (49%) |
| Structured data of type RealEstateAgent | 34 of 163 (21%) |

Files: [`data/reachability.csv`](data/reachability.csv) · [`data/robots_txt_blocks_by_crawler.csv`](data/robots_txt_blocks_by_crawler.csv) · [`data/near_empty_home_pages.csv`](data/near_empty_home_pages.csv) · [`data/summary.csv`](data/summary.csv)

**Robots.txt is rarely the problem.** 3 of the 163 sites that answered with a page block OAI-SearchBot, the crawler OpenAI documents for surfacing websites in ChatGPT search. Two of them are not live websites (a "coming soon" page and an error page) and block every crawler. One live site blocks ChatGPT's crawlers by name.

**One in eight sites turned the request away.** 16 answered with a Cloudflare page that asks the browser to run JavaScript, 3 with the same kind of check from Vercel, and 4 refused. Crawlers fetch a page without running JavaScript first, so they get past such a check only if the site's firewall lets them through. One brokerage that turned us away was a source in Google's AI answer for its city. For comparison, 13 of 200 CPA firm websites (6.5%) turned the same kind of request away a day earlier.

**16 home pages are almost empty without JavaScript.** 6 show their text only through JavaScript (334 to 1,282 words in a real browser, 4 of them on the same website platform), 4 showed a reCAPTCHA "Checking your browser" page with the same robots.txt template, 4 were not a working website (parked domain, "coming soon", error page, brokerage login page), 1 frames a site on another domain and 1 is a splash page with 20 words. Vercel and MERJ reported on December 17, 2024 that none of the major AI crawlers rendered JavaScript. In our own server logs on October 14, 2026, OpenAI's search crawler ran the JavaScript on 4 of the 7 pages it fetched, and ChatGPT-User, PerplexityBot and GPTBot showed no sign of it ([details and raw data](https://createwithlogic.com/do-ai-crawlers-render-javascript)).

**8 of the 197 Google listings link to a page the agent does not control**: 6 brokerage profile or office pages and 2 link-in-bio pages. 3 of those 8 turned the request away.

## What Google's AI cites for "best real estate agent in [city]"

On October 13, 2026 we asked Google, from the US, "best real estate agent in [city]" for 20 large US cities: 17 AI Overviews, 15 with sources. Counts: [`data/ai_overview_sources_real_estate.csv`](data/ai_overview_sources_real_estate.csv)

- Google cited its own business listings in 13 of 15 (87%), RealTrends rankings in 7 (47%) and the US News real estate agent directory in 3 (20%). Zillow and Redfin came up in 2 each.
- 14 of the 15 cited at least one agent's, team's or brokerage's own website.
- The 5 agents Google's AI named with a rating and a review count had a median of 1,136 reviews at 4.9 stars. The median across the 197 agents in our Google Maps sample was 81 reviews at 5.0 stars.

These are small samples from one day and one engine, so read the shares as a direction. The website checks follow fixed rules, and anyone can repeat them.

Same method for 200 US CPA firm websites (October 13, 2026): https://github.com/Timcreatewithlogic/ai-readiness-cpa-firm-websites

## Check your own site

```bash
pip install protego   # optional: reads robots.txt per RFC 9309, as Google and Bing do
python3 scan/check_site.py https://www.yoursite.com
```

The script loads the address once without JavaScript, says whether a firewall turned the request away, reads your robots.txt for eleven AI and search crawlers, counts the words a crawler sees and lists the JSON-LD types it finds. It sends two GET requests, nothing else. Use the address your Google listing links to, which may be a brokerage profile page rather than your home page.

Or by hand: open your site with JavaScript switched off in the browser settings and see how much text is left, then open `yourdomain.com/robots.txt` and look for `Disallow: /` under `User-agent: *` or under OAI-SearchBot, ChatGPT-User, PerplexityBot or Claude-SearchBot.

Without installing anything: paste your robots.txt into the free [AI crawler checker](https://createwithlogic.com/ai-crawler-checker). It reads the file the same way, in your browser, and shows the line that decides for each crawler.

## Free webinar, October 22, 2026

Free live webinar on Thursday, October 22, 2026, 12:00 PM ET, for US real estate agents and teams, accountants, CPA and tax firms: how ChatGPT and other AI search tools decide which agents and firms to recommend, and how to get found there. Every registered agent gets this check and an AI answer check before the session.
Details and registration: **https://createwithlogic.com/ai-visibility-webinar**

More: [AI visibility for real estate agents](https://createwithlogic.com/ai-visibility-for-real-estate-agents) · [How to get your business recommended by ChatGPT: the 2026 data](https://createwithlogic.com/how-to-get-recommended-by-chatgpt)

## Sources

- OpenAI: overview of OpenAI crawlers (OAI-SearchBot, ChatGPT-User, GPTBot): https://developers.openai.com/api/docs/bots
- Perplexity: Perplexity crawlers (PerplexityBot, Perplexity-User): https://docs.perplexity.ai/guides/bots
- Anthropic: how Anthropic crawls the web (ClaudeBot, Claude-User, Claude-SearchBot): https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler
- Vercel: The rise of the AI crawler, December 17, 2024: https://vercel.com/blog/the-rise-of-the-ai-crawler
- Cloudflare: AI crawlers blocked by default for new domains, press release, July 1, 2025: https://www.cloudflare.com/press/press-releases/2025/cloudflare-just-changed-how-ai-crawlers-scrape-the-internet-at-large/
- IETF: RFC 9309, Robots Exclusion Protocol, September 2022: https://www.rfc-editor.org/rfc/rfc9309
- schema.org: RealEstateAgent: https://schema.org/RealEstateAgent

## License

Data and text: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Please cite as "createwithlogic, AI readiness of US real estate agent websites, October 14, 2026" with a link to https://createwithlogic.com/ai-readiness-real-estate-agent-websites. Code in `scan/`: MIT, see [LICENSE](LICENSE).

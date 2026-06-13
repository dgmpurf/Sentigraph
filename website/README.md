# guixutech.com Static Website

This folder contains the static official website draft for 归墟科技 /
归墟舆情分析 / Sentigraph.

## Files

- `index.html` - homepage
- `product.html` - product page
- `data-authorization.html` - data authorization and evidence submission notice
- `privacy.html` - privacy policy
- `terms.html` - user agreement
- `contact.html` - contact and reviewer information
- `assets/site.css` - shared static CSS
- `assets/brand/guixu-logo.jpg` - current company/product logo used in the
  header and favicon

## Deployment

No build step is required. The folder can be served by any static web server,
for example Nginx, Caddy, object storage static hosting, or a cloud vendor's
static site service.

Before ICP filing or platform review, replace placeholders:

- company legal entity
- contact email
- contact phone
- company address
- ICP filing number
- public security filing number
- final privacy-policy and user-agreement effective dates
- platform OAuth callback URLs

If a vector or transparent-background logo becomes available later, replace
`assets/brand/guixu-logo.jpg` and keep the filename stable, or update the
header and favicon references across the HTML files.

## Boundaries

The site deliberately says:

- no unauthorized private data collection
- no cookie/login/captcha/anti-bot bypass
- no MediaCrawler production integration
- no automatic URL scraping
- uploaded/manual/vendor evidence is not automatically verified
- YouTube real data is optional local demo only
- Douyin/Bilibili/etc. real APIs are pending official permission

It includes no analytics scripts, no third-party trackers, no external CDN, and
no secrets.

# Risenup website preview

This folder contains a rebranded, responsive static website concept based on the public Risenup site. The core offer is clinic consulting focused on margin clarity, cost control, resource allocation, forecasting and client loyalty. The self-serve Margin Tracker is presented as the secondary product. A small tools and referrals area remains a supporting offer, with partner relationships disclosed as unconfirmed.

## Website content

- Editorial landing page with larger body text, clear navigation and prominent discovery-call and email actions.
- Published Risenup contact and booking paths: `https://risen-up.com/consulting` and `hello@risen-up.com`.
- Margin Tracker description, current published AUD price, and links to the public product and calculator pages.
- A browser-only capacity and margin scenario calculator for Australian appointment-led service businesses. It explains its assumptions and does not send or store visitor figures.
- Fourteen article pages under `insights/`, each with a unique meta description, descriptive article-specific image filename and alt text, Open Graph metadata, canonical URL, official sources and internal links. The library combines the original educational guides with two additional practical guides on staff-hour costing and owner capacity.
- Responsive styling for phone and desktop, a sitemap and robots file.

## Preview

Open `index.html` directly or run a local static server from this folder. No package installation or external script is needed. After editing article sources in `blog/posts/`, regenerate the pages with `python3 -B blog/build_blog.py`. The generator writes the existing public `/insights` path structure and leaves redirects from the prototype `/blog` paths. The supplied Lovable export was used as reference material; archive configuration files and credentials were not imported.

## Before replacement goes live

Confirm that the existing live Risenup URLs for consulting, the Margin Tracker and the leakage calculator remain the intended destinations after the site replacement. Verify the current product price and checkout terms at launch. Confirm the legal entity, ABN, GST status and public location before displaying them. Review the article topics and any generated illustrative photography against the final business scope. Add or retain current privacy, terms, returns and accessibility information, then verify the published routes, canonical URLs, sitemap and form/contact journey on the actual host.

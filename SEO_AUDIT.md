# Risenup website SEO and reader review

**Reviewed:** 10 November 2026  
**Scope:** Local static landing page, `/insights` hub and 14 article pages. The site was reviewed in source; deployed routing, Search Console, analytics and Core Web Vitals were not tested.

## Brand and offer alignment

The page now uses Risenup's published positioning: margin integrity and operational engineering for Australian clinics, salons and aesthetic practices. Consulting is presented first, the self-serve Margin Tracker second, and useful tools or referrals last. The speculative AI-app pitch was replaced with the published Margin Tracker details and its current publicly stated price of $49.99 AUD. The hero and consulting section link to the live discovery-call route; the email action uses the published `hello@risen-up.com` address.

## On-page SEO and reader experience

- The landing page declares `en-AU`, has a focused title and meta description, canonical URL, Open Graph URL/image, and a clear H1.
- The 14 static insights pages have unique titles, meta descriptions, Open Graph details, canonicals, source links and internal navigation. Each guide exceeds 2,500 words. Article topics from the supplied Risenup archive were screened for freshness, substantiation and duplication; useful concepts were consolidated into the educational library instead of copying dated claims or overlapping pages verbatim.
- The article pages are generated into `/insights/{slug}/`, matching the current public site's `/insights` information architecture. The former local `/blog` paths redirect to the new routes.
- Every article has a distinct local image file with a descriptive filename, subject-specific alt text and caption. These are illustrative editorial images, not customer results or testimonials.
- A sitemap and robots file are included. The host still needs to serve the `/insights` route structure as generated.
- Main copy is larger, mobile navigation links remain visible, and the booking/email actions are easy to identify.

## Published information and safeguards

The live homepage describes the service focus, ABN 42 674 304 726, Sydney location, nationwide engagements and prices in AUD including GST. The email and product price were also carried over. The local page omits the ABN, GST and specific location claims pending verification: an independent review flagged that the ABN Lookup record for the published number may identify a different legal entity and GST status. Confirm the correct legal entity, ABN, registration and location details before restoring those claims. The visible tracker price should be checked against the actual checkout after migration.

The website says Risenup does not provide marketing services. The insights section contains educational material; it should not be presented as a marketing consultancy. Accounting, tax, legal, employment and specialist safety work should be referred to suitably qualified professionals.

## Remaining launch checks

1. Confirm the public `/consulting`, `/margin-tracker`, `/calculator` and `/contact` routes remain active and function after replacement. The homepage's discovery-call link is visible, but this source review did not verify a live booking calendar.
2. Verify the legal entity, ABN, GST status and location. Keep unverified details out of the footer.
3. Check privacy, terms, returns/refund, accessibility and contact policies, and link the correct current versions.
4. Validate canonical and sitemap routes on the actual host, redirect old URLs where needed, then inspect indexing in Search Console.
5. Check mobile navigation, keyboard focus, contrast, text scaling, image delivery and page speed in the deployed site.
6. Review the 14 articles for scope fit. They are educational guides and do not imply Risenup provides marketing, tax, legal, accounting or specialist safety services.
7. Add structured data only after the legal entity, service scope, contact information and final routes are confirmed.

## Public sources

- [Risenup homepage](https://risen-up.com/)
- [Risenup contact](https://risen-up.com/contact)
- [ABN Lookup](https://abr.business.gov.au/ABN/View?abn=42674304726)

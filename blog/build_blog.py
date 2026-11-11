#!/usr/bin/env python3
"""Build self-contained, static Australian small-business learning pages."""
from html import escape
from pathlib import Path
from urllib.parse import urljoin
import re

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / 'blog'
POSTS = BLOG / 'posts'
OUT = ROOT / 'insights'
OUT.mkdir(parents=True, exist_ok=True)

CHARTS = {
 'staff-cost': ('Illustrative layers in an employer cost estimate', '<svg viewBox="0 0 720 290" role="img" aria-labelledby="chart-title chart-desc"><title id="chart-title">Illustrative layers in an employer cost estimate</title><desc id="chart-desc">Start with ordinary pay, then check super, award conditions, leave, state charges and role-specific costs separately.</desc><rect width="720" height="290" rx="14" fill="#f6f2ea"/><g font-family="Arial" fill="#402a1d"><text x="40" y="42" font-size="18">Build the estimate in visible layers</text><text x="40" y="94" font-size="13">Ordinary pay</text><rect x="210" y="72" width="390" height="32" rx="4" fill="#7b3023"/><text x="40" y="143" font-size="13">Super on qualifying earnings</text><rect x="210" y="121" width="130" height="32" rx="4" fill="#987d63"/><text x="40" y="192" font-size="13">Award, leave and allowances</text><rect x="210" y="170" width="180" height="32" rx="4" fill="#b59b7f"/><text x="40" y="241" font-size="13">State and role-specific costs</text><rect x="210" y="219" width="230" height="32" rx="4" fill="#65785a"/><text x="475" y="273" font-size="11" fill="#786e62">Check each rule and assumption separately.</text></g></svg>'),
 'scale-capacity': ('A practical sequence for freeing owner capacity', '<svg viewBox="0 0 760 290" role="img" aria-labelledby="chart-title chart-desc"><title id="chart-title">A practical sequence for freeing owner capacity</title><desc id="chart-desc">Observe the owner’s work, map a bottleneck, document a repeatable task, train a named owner, then review impact on time, team and clients.</desc><rect width="760" height="290" rx="14" fill="#f6f2ea"/><g font-family="Arial" text-anchor="middle"><g fill="#7b3023"><rect x="25" y="70" width="132" height="92" rx="9"/><rect x="177" y="70" width="132" height="92" rx="9"/><rect x="329" y="70" width="132" height="92" rx="9"/><rect x="481" y="70" width="132" height="92" rx="9"/><rect x="633" y="70" width="102" height="92" rx="9"/></g><g fill="white" font-size="12"><text x="91" y="106">Observe</text><text x="91" y="128">owner time</text><text x="243" y="106">Map one</text><text x="243" y="128">bottleneck</text><text x="395" y="106">Document</text><text x="395" y="128">the process</text><text x="547" y="106">Train and</text><text x="547" y="128">delegate</text><text x="684" y="106">Review</text><text x="684" y="128">the impact</text></g><path d="M158 116h17m132 0h17m132 0h17m132 0h17" stroke="#402a1d" stroke-width="2"/><g fill="#402a1d" font-size="11"><text x="91" y="190">Keep customer work</text><text x="243" y="190">Find the real cause</text><text x="395" y="190">Include exceptions</text><text x="547" y="190">Clarify authority</text><text x="684" y="190">Check workload too</text></g><text x="380" y="247" fill="#402a1d" font-size="13">Keep the process only if it works for the owner, team and clients.</text></g></svg>'),
 'service-margin': ('Illustrative service contribution waterfall', '<svg viewBox="0 0 720 310" role="img" aria-labelledby="chart-title chart-desc"><title id="chart-title">Illustrative service contribution waterfall</title><desc id="chart-desc">A service price is reduced by variable costs to show contribution before fixed costs.</desc><rect width="720" height="310" rx="14" fill="#f6f2ea"/><g font-family="Arial" fill="#402a1d"><text x="40" y="42" font-size="18">One service: example only</text><text x="40" y="84" font-size="13">Customer price</text><rect x="175" y="66" width="420" height="30" rx="5" fill="#7b3023"/><text x="610" y="87" font-size="14">$120</text><text x="40" y="135" font-size="13">Consumables</text><rect x="175" y="117" width="70" height="30" rx="5" fill="#b8a58e"/><text x="260" y="138" font-size="14">− $20</text><text x="40" y="186" font-size="13">Variable fees</text><rect x="175" y="168" width="35" height="30" rx="5" fill="#b8a58e"/><text x="225" y="189" font-size="14">− $10</text><text x="40" y="237" font-size="13">Contribution before fixed costs</text><rect x="280" y="219" width="245" height="30" rx="5" fill="#65785a"/><text x="540" y="240" font-size="14">$90</text><text x="40" y="283" font-size="11" fill="#786e62">Example figures demonstrate the method; they are not salon benchmarks.</text></g></svg>'),
 'cash-cycle': ('Illustrative weekly cash visibility cycle', '<svg viewBox="0 0 720 245" role="img" aria-labelledby="chart-title chart-desc"><title id="chart-title">Illustrative weekly cash visibility cycle</title><desc id="chart-desc">A repeating weekly sequence to compare opening cash, expected inflows, planned outflows and closing cash.</desc><rect width="720" height="245" rx="14" fill="#f6f2ea"/><g font-family="Arial" text-anchor="middle" fill="#402a1d"><g><circle cx="95" cy="105" r="42" fill="#7b3023"/><text x="95" y="101" font-size="12" fill="white">Opening</text><text x="95" y="118" font-size="12" fill="white">cash</text></g><g><circle cx="270" cy="105" r="42" fill="#987d63"/><text x="270" y="101" font-size="12" fill="white">Expected</text><text x="270" y="118" font-size="12" fill="white">inflows</text></g><g><circle cx="445" cy="105" r="42" fill="#987d63"/><text x="445" y="101" font-size="12" fill="white">Planned</text><text x="445" y="118" font-size="12" fill="white">outflows</text></g><g><circle cx="620" cy="105" r="42" fill="#65785a"/><text x="620" y="101" font-size="12" fill="white">Closing</text><text x="620" y="118" font-size="12" fill="white">cash</text></g><path d="M143 105h76m99 0h76m99 0h76" stroke="#402a1d" stroke-width="2"/><text x="360" y="202" font-size="13">Update assumptions each week; investigate timing gaps before they arrive.</text></g></svg>'),
 'local-journey': ('Local discovery to repeat booking journey', '<svg viewBox="0 0 760 270" role="img" aria-labelledby="chart-title chart-desc"><title id="chart-title">Local discovery to repeat booking journey</title><desc id="chart-desc">A measurable customer journey from local search to enquiry, first visit, rebooking and return.</desc><rect width="760" height="270" rx="14" fill="#f6f2ea"/><g font-family="Arial" text-anchor="middle"><g fill="#7b3023"><rect x="25" y="68" width="128" height="80" rx="10"/><rect x="177" y="68" width="128" height="80" rx="10"/><rect x="329" y="68" width="128" height="80" rx="10"/><rect x="481" y="68" width="128" height="80" rx="10"/><rect x="633" y="68" width="102" height="80" rx="10"/></g><g fill="white" font-size="13"><text x="89" y="103">Local</text><text x="89" y="123">discovery</text><text x="241" y="103">Enquiry /</text><text x="241" y="123">booking</text><text x="393" y="103">First</text><text x="393" y="123">visit</text><text x="545" y="103">Rebook</text><text x="545" y="123">invitation</text><text x="684" y="103">Return</text><text x="684" y="123">visit</text></g><g fill="#402a1d" font-size="11"><text x="89" y="178">Profile views</text><text x="241" y="178">Response time</text><text x="393" y="178">Experience</text><text x="545" y="178">Eligible consent</text><text x="684" y="178">Repeat rate</text></g><path d="M154 108h19m132 0h19m132 0h19m132 0h19" stroke="#402a1d" stroke-width="2"/></g></svg>'),
 'automation': ('Human-reviewed automation loop', '<svg viewBox="0 0 720 300" role="img" aria-labelledby="chart-title chart-desc"><title id="chart-title">Human-reviewed automation loop</title><desc id="chart-desc">A process is triggered, checked, automated, reviewed by a person when needed, and improved from exceptions.</desc><rect width="720" height="300" rx="14" fill="#f6f2ea"/><g font-family="Arial" text-anchor="middle"><g fill="#7b3023"><rect x="32" y="80" width="135" height="74" rx="10"/><rect x="205" y="80" width="135" height="74" rx="10"/><rect x="378" y="80" width="135" height="74" rx="10"/><rect x="551" y="80" width="135" height="74" rx="10"/></g><g fill="white" font-size="13"><text x="99" y="111">Trigger</text><text x="99" y="132">and owner</text><text x="272" y="111">Rules and</text><text x="272" y="132">data check</text><text x="445" y="111">Automated</text><text x="445" y="132">action</text><text x="618" y="111">Human review</text><text x="618" y="132">if exception</text></g><path d="M168 117h34m137 0h34m137 0h34" stroke="#402a1d" stroke-width="2"/><path d="M618 157v66H100v-65" fill="none" stroke="#65785a" stroke-width="2"/><text x="360" y="250" font-size="13" fill="#402a1d">Record exceptions; review accuracy, time saved and customer impact.</text></g></svg>'),
 'inventory': ('Illustrative stock reorder point', '<svg viewBox="0 0 720 300" role="img" aria-labelledby="chart-title chart-desc"><title id="chart-title">Illustrative stock reorder point</title><desc id="chart-desc">Stock falls over time as products are used; a reorder is placed before stock reaches zero, allowing for supplier lead time and a chosen buffer.</desc><rect width="720" height="300" rx="14" fill="#f6f2ea"/><path d="M90 50v190h560" fill="none" stroke="#402a1d" stroke-width="2"/><path d="M92 70 190 91 280 119 370 151 460 179 550 212 640 233" fill="none" stroke="#7b3023" stroke-width="5"/><path d="M90 155h550" stroke="#65785a" stroke-width="2" stroke-dasharray="8 7"/><g font-family="Arial" fill="#402a1d"><text x="110" y="142" font-size="13">Reorder point = expected use during lead time + chosen buffer</text><text x="305" y="274" font-size="12">Time</text><text x="26" y="155" transform="rotate(-90 26 155)" font-size="12">Usable stock</text><text x="555" y="224" font-size="11">Risk of stockout</text></g></svg>'),
 'continuity': ('Business continuity layers', '<svg viewBox="0 0 720 310" role="img" aria-labelledby="chart-title chart-desc"><title id="chart-title">Business continuity layers</title><desc id="chart-desc">Prepare before disruption, respond safely, communicate, restore essential work and review lessons.</desc><rect width="720" height="310" rx="14" fill="#f6f2ea"/><g font-family="Arial" text-anchor="middle"><path d="M360 42 620 250H100z" fill="#e4d8c8"/><path d="M360 82 540 220H180z" fill="#b59b7f"/><path d="M360 120 460 190H260z" fill="#7b3023"/><g fill="#402a1d" font-size="14"><text x="360" y="74">1 · Prepare and protect people</text><text x="360" y="142" fill="white">2 · Respond and communicate</text><text x="360" y="180" fill="white">3 · Restore critical work</text></g><text x="360" y="278" font-family="Arial" font-size="12" fill="#402a1d">Review, update contacts, practise, and learn after each disruption.</text></g></svg>')
}

def read_post(path):
    text = path.read_text(encoding='utf-8')
    meta, body = text.split('---BODY---', 1)
    fields = {}
    for line in meta.strip().splitlines():
        k, v = line.split(':', 1)
        fields[k.strip()] = v.strip()
    fields['body'] = body.strip()
    return fields

def inline(text):
    text = escape(text, quote=False)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>', text)
    return text

def slugify(value):
    value = re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-')
    return value or 'section'

def markdown(body):
    lines = body.splitlines()
    out, para, in_ul, in_ol = [], [], False, False
    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul: out.append('</ul>'); in_ul = False
        if in_ol: out.append('</ol>'); in_ol = False
    def flush_para():
        if para:
            out.append('<p>' + inline(' '.join(para)) + '</p>'); para.clear()
    for line in lines:
        s = line.strip()
        if not s:
            flush_para(); close_lists(); continue
        if s.startswith('{{CHART:') and s.endswith('}}'):
            flush_para(); close_lists(); key = s[8:-2]
            title, svg = CHARTS[key]
            out.append(f'<figure class="article-chart">{svg}<figcaption>{escape(title)}. Illustrative diagram; use your own records and assumptions.</figcaption></figure>')
        elif s.startswith('## '):
            flush_para(); close_lists(); heading = s[3:]; heading_id = slugify(heading); out.append(f'<h2 id="{heading_id}">{inline(heading)}</h2>')
        elif s.startswith('### '):
            flush_para(); close_lists(); out.append(f'<h3>{inline(s[4:])}</h3>')
        elif s.startswith('> '):
            flush_para(); close_lists(); out.append(f'<blockquote><p>{inline(s[2:])}</p></blockquote>')
        elif s.startswith('- '):
            flush_para()
            if in_ol: out.append('</ol>'); in_ol=False
            if not in_ul: out.append('<ul>'); in_ul=True
            out.append(f'<li>{inline(s[2:])}</li>')
        elif re.match(r'^\d+\. ', s):
            flush_para()
            if in_ul: out.append('</ul>'); in_ul=False
            if not in_ol: out.append('<ol>'); in_ol=True
            item = re.sub(r'^\d+\. ', '', s)
            out.append(f'<li>{inline(item)}</li>')
        else:
            close_lists(); para.append(s)
    flush_para(); close_lists()
    return '\n'.join(out)

posts = [read_post(p) for p in sorted(POSTS.glob('*.md'))]
categories = {
 'service-pricing-contribution': 'Profit & pricing', 'cash-flow-weekly-rhythm': 'Cash flow',
 'local-seo-service-businesses': 'Marketing', 'client-retention-with-consent': 'Client experience',
 'small-business-cyber-security-basics': 'Digital safety', 'choose-small-business-software': 'Technology',
 'stock-control-service-businesses': 'Operations', 'small-business-workflow-automation': 'Operations',
 'small-business-ai-privacy': 'Digital safety', 'employee-onboarding-studio-workflows': 'People & systems',
 'workplace-safety-service-studios': 'People & systems', 'small-business-continuity-plan': 'Resilience',
 'real-cost-staff-hour': 'People & systems', 'grow-clinic-without-more-owner-hours': 'Sustainable growth',
}
for p in posts:
    p['category'] = categories.get(p['slug'], 'Practical guide')
by_slug = {p['slug']: p for p in posts}
related_map = {
 'service-pricing-contribution': 'real-cost-staff-hour',
 'cash-flow-weekly-rhythm': 'small-business-continuity-plan',
 'employee-onboarding-studio-workflows': 'grow-clinic-without-more-owner-hours',
 'small-business-workflow-automation': 'grow-clinic-without-more-owner-hours',
 'real-cost-staff-hour': 'employee-onboarding-studio-workflows',
 'grow-clinic-without-more-owner-hours': 'small-business-workflow-automation',
}
nav = '<a href="../index.html">Home</a><a href="index.html">Insights</a><a href="../index.html#solutions">Consulting</a><a href="../index.html#platform">Margin Tracker</a>'
def shell(title, desc, content, path_prefix='../', nav_html=None, blog_index_href='index.html', canonical_url='https://risen-up.com/insights', image_url='https://risen-up.com/assets/risen-up-clinic-consulting.jpg'):
    if nav_html is None:
        nav_html = nav
    return f'''<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Risenup Insights | {escape(title)}</title><meta name="description" content="{escape(desc, quote=True)}"><meta property="og:type" content="article"><meta property="og:site_name" content="Risenup"><meta property="og:locale" content="en_AU"><meta property="og:title" content="{escape(title, quote=True)}"><meta property="og:description" content="{escape(desc, quote=True)}"><meta property="og:url" content="{escape(canonical_url, quote=True)}"><meta property="og:image" content="{escape(image_url, quote=True)}"><link rel="canonical" href="{escape(canonical_url, quote=True)}"><meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#402a1d"><link rel="icon" type="image/svg+xml" href="{path_prefix}favicon.svg"><link rel="stylesheet" href="{path_prefix}editorial.css"><link rel="stylesheet" href="{path_prefix}blog/blog.css"></head><body><div class="site-shell blog-shell"><header class="blog-header"><a class="blog-logo" href="{path_prefix}index.html">Risen<span>up</span></a><nav aria-label="Main navigation">{nav_html}</nav></header>{content}<footer class="blog-footer"><a href="{path_prefix}index.html">Risenup</a><span>Practical insights for Australian clinics</span><a href="{blog_index_href}">All insights</a></footer></div></body></html>'''

cards = []
for p in posts:
    count = len(re.findall(r"\b[\w’'-]+\b", p['body']))
    p['word_count'] = count
    card = f'''<article class="post-card" data-category="{escape(p['category'])}"><a class="post-image" href="{escape(p['slug'])}/"><img src="../assets/{escape(p['image'])}" alt="{escape(p['alt'], quote=True)}" loading="lazy" width="1200" height="800"></a><div class="post-card-copy"><span>{escape(p['category'])} · {count:,} words</span><h2><a href="{escape(p['slug'])}/">{escape(p['title'])}</a></h2><p>{escape(p['description'])}</p><a class="text-link" href="{escape(p['slug'])}/">Read the guide</a></div></article>'''
    cards.append(card)
    related_slug = related_map.get(p['slug'])
    related_link = f'<a href="../{escape(related_slug)}/">Related guide: {escape(by_slug[related_slug]["title"])}</a>' if related_slug else ''
    toc = ''.join(f'<li><a href="#{slugify(line[3:].strip())}">{escape(line[3:].strip())}</a></li>' for line in p['body'].splitlines() if line.startswith('## '))
    article = f'''<main><section class="article-hero"><a class="back-link" href="../index.html">Back to insights</a><span class="eyebrow">AUSTRALIAN SMALL BUSINESS · PRACTICAL GUIDE</span><h1>{escape(p['title'])}</h1><p class="article-deck">{escape(p['description'])}</p><div class="article-byline">Risenup learning library <span>·</span> {count:,} words <span>·</span> Updated 11 November 2026</div></section><figure class="article-cover"><img src="../../assets/{escape(p['image'])}" alt="{escape(p['alt'], quote=True)}" width="1200" height="800" fetchpriority="high"><figcaption>Illustrative editorial photography: {escape(p['alt'])} Not a customer case study.</figcaption></figure><article class="article-body"><aside class="key-points"><h2>What matters most</h2><ul><li>Use your own business records and write down assumptions.</li><li>Choose one manageable action, assign an owner and review a real measure.</li><li>Check Australian requirements with the relevant official source or qualified adviser.</li></ul></aside><nav class="article-toc" aria-label="On this page"><details><summary>On this page</summary><ol>{toc}</ol></details></nav>{markdown(p['body'])}<section class="article-sources"><h2>Official and further reading</h2><ul>{''.join(f'<li><a href="{escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">{escape(label)}</a></li>' for label,url in [tuple(item.split(' | ',1)) for item in p['sources'].split('; ')])}</ul><p>This educational guide provides general information, not financial, legal, tax, employment, privacy or safety advice. Check current rules and get qualified advice for your circumstances.</p></section></article><nav class="related-guides" aria-label="Related guides"><a href="../index.html">Browse all insights</a>{related_link}<a href="../../index.html#solutions">Explore clinic consulting</a></nav></main>'''
    article_nav = '<a href="../../index.html">Home</a><a href="../index.html">Insights</a><a href="../../index.html#solutions">Consulting</a><a href="../../index.html#platform">Margin Tracker</a>'
    article_dir = OUT / p['slug']
    article_dir.mkdir(parents=True, exist_ok=True)
    (article_dir / 'index.html').write_text(shell(p['title'], p['description'], article, path_prefix='../../', nav_html=article_nav, blog_index_href='../index.html', canonical_url=f"https://risen-up.com/insights/{p['slug']}/", image_url=f"https://risen-up.com/assets/{p['image']}"), encoding='utf-8')

filter_categories = ['All guides'] + list(dict.fromkeys(p['category'] for p in posts))
filter_buttons = ''.join('<button type="button" data-filter="{}" aria-pressed="{}">{}{}</button>'.format(escape(cat), 'true' if i == 0 else 'false', escape(cat), f' ({len(posts)})' if i == 0 else '') for i, cat in enumerate(filter_categories))
hub = f'''<main class="blog-home"><section class="blog-intro"><span class="eyebrow">RISENUP · CLINIC FIELD NOTES</span><h1>Build a better clinic<br><em>from the numbers up.</em></h1><p>A full diary measures activity. Clinic owners also need to understand what each service contributes after treatment time, products and operating costs. These practical guides bring that margin-first view to pricing, cash flow, client experience, team systems, technology and business resilience.</p></section><section class="insights-lens" aria-label="A practical clinic improvement lens"><article><span>01 · VISIBILITY</span><h2>See the real picture</h2><p>Organise the numbers and operating facts that help explain what is happening in the clinic.</p></article><article><span>02 · SERVICE ECONOMICS</span><h2>Understand contribution</h2><p>Consider price, team time, products and capacity together when reviewing services.</p></article><article><span>03 · OPERATING RHYTHM</span><h2>Make the work repeatable</h2><p>Use clear routines and systems to reduce avoidable friction and keep important checks visible.</p></article><article><span>04 · SUSTAINABLE GROWTH</span><h2>Choose the next move</h2><p>Set a practical priority, test it against your circumstances and review what changes.</p></article></section><div class="guide-filter" role="group" aria-label="Filter guides by topic">{filter_buttons}</div><p class="sr-only" id="filter-status" aria-live="polite">Showing all {len(posts)} guides.</p><section class="post-grid" aria-label="All {len(posts)} learning guides">{''.join(cards)}</section><section class="blog-cta"><div><span class="eyebrow">NEED HELP APPLYING IT?</span><h2>Turn a business question<br>into a practical plan.</h2><p>Risenup's core service is tailored clinic consulting. We work with your actual numbers and operating priorities.</p></div><a class="button dark" href="../index.html#solutions">Explore consulting</a></section></main>'''
filter_script = """<script>const filters=[...document.querySelectorAll('[data-filter]')],guides=[...document.querySelectorAll('.post-card')],status=document.getElementById('filter-status');filters.forEach(button=>button.addEventListener('click',()=>{const topic=button.dataset.filter;let shown=0;guides.forEach(card=>{const visible=topic==='All guides'||card.dataset.category===topic;card.hidden=!visible;if(visible)shown++});filters.forEach(item=>item.setAttribute('aria-pressed',String(item===button)));status.textContent=topic==='All guides'?`Showing all ${shown} guides.`:`Showing ${shown} ${topic.toLowerCase()} guides.`}));</script>"""
(OUT / 'index.html').write_text(shell('Australian Clinic Business Guides', 'Practical Australian clinic guides on service pricing, cash flow, client retention, staffing, software, safety, AI, operations and business continuity.', hub + filter_script), encoding='utf-8')
print(f'Built {len(posts)} guides; word counts: ' + ', '.join(f"{p['slug']}={p['word_count']}" for p in posts))

# Keep old prototype paths useful while canonicals and navigation point to the live /insights structure.
redirect = lambda title, target: f"<!doctype html><html lang=\"en-AU\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><title>{escape(title)}</title><meta name=\"robots\" content=\"noindex,follow\"><link rel=\"canonical\" href=\"{urljoin('https://risen-up.com/', target)}\"><meta http-equiv=\"refresh\" content=\"0; url={target}\"></head><body><p>This page has moved to <a href=\"{target}\">Risenup Insights</a>.</p></body></html>"
(BLOG / 'index.html').write_text(redirect('Risenup Insights', '../insights'), encoding='utf-8')
for post in posts:
    old = BLOG / 'articles' / f"{post['slug']}.html"
    old.parent.mkdir(parents=True, exist_ok=True)
    old.write_text(redirect(post['title'], f"../../insights/{post['slug']}/"), encoding='utf-8')

tool_guide_urls = [
    'https://risen-up.com/tools/',
    'https://risen-up.com/tools/payments-pos/',
    'https://risen-up.com/tools/booking-client-systems/',
    'https://risen-up.com/tools/accounting-business-apps/',
    'https://risen-up.com/tools/printers-studio-equipment/',
    'https://risen-up.com/tools/business-specialists/',
    'https://risen-up.com/tools/cyber-continuity/',
]
site_urls = ['https://risen-up.com/', 'https://risen-up.com/insights'] + tool_guide_urls + [f"https://risen-up.com/insights/{p['slug']}/" for p in posts]
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{escape(url)}</loc></url>\n' for url in site_urls) + '</urlset>\n'
(ROOT / 'sitemap.xml').write_text(sitemap, encoding='utf-8')

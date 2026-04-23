# Source
## AI Model
Claude Sonnet 4.6 High

## Used Prompts
### Setup Step 1
Can you setup a python project which:
- Which checking https://www.bundle.app/tr/gundem once every 5 minutes
- Filtering texts in "p" scopes with "mobile:font-bold font-semibold text-lg line-clamp-3 mobile:leading-[130%] leading-[20px]" class
- Dumps those texts and their links in a JSON file

Instructions:
- Write the code clean
- Use comments effectively
- Make the project modular and scalable
- Categorize modules as what their function does
- If you need me to clarify any multiple possibilities or chooses, just ask to me, don't generate the most possible option instead

### Setup Step 2
1. Link extraction

Links are in \<a\> scope with "flex flex-col font-barlow gap-y-5 min-w-[280px] w-[280px] bg-transparent " class

2. Scraping approach

Use playwright, because this would be a team project for a class. I need to have less conflict.

3. JSON file behavior

Append new results with 10 times history top-limit

4. Scheduler

Use a Python-internal scheduler (e.g., schedule or APScheduler)

### Logger and Error Handling
Can you add a logger which creates a log_{n}.txt in /logs folder with 10 files history limit, creating a new file on every run?

Log format:
[Current Date-Time] Data scrapped from [url]. [n] articles has found. Saved into [JSON path]

And also can log swallowed errors into the log.txt, and kill the process with corresponding error code/text in case of critical errors?

### v0.1 Version Description
- Can you make a GitHub version description?
- This is readme, I need a push description

### Multiple Sources - Part 1
...

2. Multiple sources — this directly affects your grade
So, we need to prepare custom engines for every source. Please make a clean categorize logic for source engines. I will add new sources in the next prompt.

...

### Multiple Sources - Part 2
Now, it's time to add new scrappers:

- BBC
Target URL: https://www.bbc.com/turkce
Parents: \<div\> scope, class: promo-text
Links: \<a\> scope, class: "css-1i4ie53 eq53xv90"
Titles: \<h3\> scope, class: css-kiiel0 ez3pb4d0 || \<h3\> scope, class: css-g0mr8l ez3pb4d0

- Independent
Target URL: https://www.indyturk.com
Title: \<div\> scope, class: article-item-title
Links: In the same scope as title, \<a\> scope (If multiple a scopes exists, ignore and log an error)

- Euronews
Target URL: https://tr.euronews.com/son-haberler
Parent: \<li\> scope, class: tc-justin-timeline__item
Title: In \<h2\> scope, class: tc-justin-timeline__article__title
Links: \<a\> scope, class: tc-justin-timeline__article__link

### JavaScript Fix for Euronews Page
Log: [2026-04-23 13:15:00] Data scrapped from https://tr.euronews.com/son-haberler. 0 articles has found. Saved into data\euronews_tr.json.

Can you try to use fetch_dynamic_html() for euronews?

### v0.2 Version Description
Can you write a change log for this snapshot of the project by checking git data?

### README.md
Can you make a README.md and dump it into root folder?

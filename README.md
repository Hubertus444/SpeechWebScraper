# SpeechWebScraper
Scrape central bankers speeches from the ECB and BIS website.

This module scrapes central bankers speeches from the ECB's and BIS's website.
First, it downloads metadata and urls. Second, it uses these urls to scrape the singular speeches.

Data features the speech, its author, the date, optionally subtitles, footnotes and related topics.


module structure:
- SpeechScraper
| \n
| - URLScraper
| |
| | - BisURLScraper
| |
| | - EcbURLScraper
|
| - PageScraper
| |
| | - BisPageScraper
| |
| | - EcbPageScraper

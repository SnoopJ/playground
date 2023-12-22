This is a small script for scraping the [Unicode Technical Committee (UTC) Document Register](https://www.unicode.org/L2/L-curdoc.htm)
and producing [an RSS feed](https://snoopj.dev/files/UTC_register.xml) with one entry per document in the register.

```
$ python3 scrape_UTC_register.py
Fetching register data
RSS feed output written to UTC_register.xml

$ head -48 UTC_register.xml
<?xml version='1.0' encoding='UTF-8'?>
<rss xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/" version="2.0">
  <channel>
    <title>UTC Document Register</title>
    <link>https://www.unicode.org/L2/L-curdoc.htm</link>
    <description>UTC Document Register</description>
    <docs>http://www.rssboard.org/rss-specification</docs>
    <generator>python-feedgen</generator>
    <lastBuildDate>Fri, 22 Dec 2023 02:22:44 +0000</lastBuildDate>
    <item>
      <title>Proposal to add one character used for one kind of Hakka snack to UAX #45</title>
      <link>https://www.unicode.org/L2/L2023/23285-uax45-hakka-snack.pdf</link>
      <guid isPermaLink="false">L2/23-285</guid>
      <pubDate>Tue, 19 Dec 2023 00:00:00 +0000</pubDate>
    </item>
    <item>
      <title>Proposal to encode two small form CJK characters for Chinese</title>
      <link>https://www.unicode.org/L2/L2023/23284-small-er-proposal.pdf</link>
      <guid isPermaLink="false">L2/23-284</guid>
      <pubDate>Wed, 13 Dec 2023 00:00:00 +0000</pubDate>
    </item>
```

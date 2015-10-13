Changelog
=========

0.1.6
------------

- add on listens for the existence of the env var DUMP_RAW_AWSTATS_URLS,
  useful for testing and troubleshooting
- @@popular_content_view can now be configured to say how many items should show
  on the page. This setting is managed in the registry. The default value is 150.
  
0.1.5
----------------

- added a popular content view
- added a popular content portlet
- added a content type whitelist to the portlet
- added a url black list to the portlet
- added an option to filter out direct downloads from the portlet

0.1.4
----------------

- added support for hits (not just page views)
  [pigeonflight]

0.1.3
----------------

- moved the stats viewlet to the top of the portal footer viewlet manager
  [pigeonflight]

0.1.2
----------------

- fixed a problem with the way the path was retrieved
  [pigeonflight]
- now counts downloaded attachments different from views
  [pigeonflight]

0.1.1
----------------

- moved the hitcounter viewlet to the viewlets.IPortalFooter
- added custom app.js which asynchronously pulls stats from the 'awstats_hitcounter_view'
- the stats view now returns the content type, creation date and number of views
  [pigeonflight]
- update to use BeautifulSoup for scraping awstats
  [pigeonflight]

0.1 
----------------

- Initial release.
  [pigeonflight]


==================================
collective.awstats_hitcounter
==================================

Grabs hits, views and popular content based on awstats data and presents
this information in the context of your Plone site.
Provides a "Popular Content" portlet for displaying popular content from
awstats.

Installation & Usage
------------------------

Add collective.awstats_hitcounter to your buildout
and re-run bin/buildout

Then install on your plone site under "Site Setup" > "Add-ons"

Once this is installed you know have the facility to dynamically pull in a counter.

Configuration
---------------------

After installation configure your awstats url.
You can do so by going to Site Setup > Awstats HitCounter Settings.

.. image:: https://raw.githubusercontent.com/collective/collective.awstats_hitcounter/master/sitesettings.png

Set the absolute url to look similar to this:

.. image:: https://raw.githubusercontent.com/collective/collective.awstats_hitcounter/master/configure_url.png
   :width: 800 px

Configuring the Popular Content settings for the popular_content_view
````````````````````````````````````````````````````````````````````````````

In order to make use of the built in @@popular_content_view you will need to register an "awstats popular page"


If you need to find the "awstats popular page" you will need to provide the url from your awstats installation that provides the full 
list of Page URLs then follow the link to the "Full list"
It will look something like this:

.. image:: https://raw.githubusercontent.com/collective/collective.awstats_hitcounter/master/awstats_fulllist_screenshot.png
   :width: 800 px

Add that url as the `awstats_hitcounter url_of_popular_page` value (see the image below).

.. image:: https://raw.githubusercontent.com/collective/collective.awstats_hitcounter/master/portal_registry.png
   :width: 800 px

Debugging with DUMP_RAW_AWSTATS_URLS
---------------------------------------

Sometimes you want to make sure things are working.
The following can be done on a non-production server. 

DO NOT DO THIS ON A PRODUCTION SERVER.

Launch the instance with the env var DUMP_RAW_AWSTATS_URLS as follows::

    DUMP_RAW_AWSTATS_URLS=1 bin/instance fg 

This tells the system to skip comparing awstats values to the site catalog.
Effectively you'll just get a 'raw' dump of the URLs returned from AWSTATS.
This is very useful for troubleshooting and diagnosing if scraping is working
at all.


Usage
---------

collective.awstats_hitcounter adds a viewlet with the id 'awstats_hitcounter' which pulls in the stats from awstats.

Add this javascript at the bottom of pages where you want the counter to show::

    $("#awstats_hitcounter").load(window.location.pathname + "/@@awstats_hitcounter_view")

The screenshot below illustrates the expected behaviour

.. image:: https://raw.githubusercontent.com/collective/collective.awstats_hitcounter/master/awstats_hitcounter_screenshot.png
   :width: 800 px

The Popular Content Portlet
````````````````````````````

This add-on provides a "Popular Content Portlet". It can either make use of the global settings or use settings
specific to the portlet.

The portlet is used to present the most popular content
on your website, based on awstats.


If you prefer to configure all settings in the context of the portlet, you will need to provide the url from your 
awstats installation that provides the full list of Page URLs then follow the link to the "Full list"
It will look something like this:

.. image:: https://raw.githubusercontent.com/collective/collective.awstats_hitcounter/master/awstats_fulllist_screenshot.png
   :width: 800 px

Copy the url associated with that page, you'll need it when adding the portlet.

Decide where in your site you want the portlet to be located and using the 'manage portlets' link add a new 'Popular Content Portlet'. You'll see a screen similar to this:


.. image:: https://raw.githubusercontent.com/collective/collective.awstats_hitcounter/master/configuring_the_portlet.png
   :width: 800 px

We recommend that you leave the "Read settings from the global registry" option selected, this has the effect of 
overriding the values of the settings highlighted in orange below.
(The global registry is also used for the Popular content view).

.. image:: https://raw.githubusercontent.com/collective/collective.awstats_hitcounter/master/configuring_the_portlet-global-registry.png
   :width: 800 px

Use the **Blacklist** to prevent particular URLs from showing up in popular content.

Use the **White list** to specify what content types are allowed in the portlet.

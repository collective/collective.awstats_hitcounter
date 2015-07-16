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

The popular content portlet is used to present the most popular content
on your website, based on awstats.

You will need to provide the url from your awstats installation that provides the full list of Page URLs then follow the link to the "Full list"
It will look something like this:

.. image:: https://raw.githubusercontent.com/collective/collective.awstats_hitcounter/master/awstats_fulllist_screenshot.png
   :width: 800 px

Make a note of the url associated with that page, you'll need it when adding the portlet.

Decide where in your site you want the portlet to be located and using the 'manage portlets' link add a new 'Popular Content Portlet'. You'll see a screen similar to this:


.. image:: https://raw.githubusercontent.com/collective/collective.awstats_hitcounter/master/configuring_the_portlet.png
   :width: 800 px

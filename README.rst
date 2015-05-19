==================================
collective.awstats_hitcounter
==================================

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
   :width: 800 px

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


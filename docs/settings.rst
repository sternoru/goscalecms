2. Configuration
====================

2.1. Plugins settings
---------------------

**GOSCALE_VIDEOS_CUSTOM_PLUGIN_TEMPLATES**

Additional templates list for goscale.plugins.videos. (default: ())

**GOSCALE_CALENDAR_CUSTOM_PLUGIN_TEMPLATES**

Additional templates list for goscale.plugins.calendar. (default: ())

**GOSCALE_FEEDS_CUSTOM_PLUGIN_TEMPLATES**

Additional templates list for goscale.plugins.feeds. (default: ())

**GOSCALE_FORMS_CUSTOM_PLUGIN_TEMPLATES**

Additional templates list for goscale.plugins.forms. (default: ())

**GOSCALE_PICTURES_CUSTOM_PLUGIN_TEMPLATES**

Additional templates list for goscale.plugins.pictures. (default: ())


2.2. Global settings
---------------------

**GOSCALE_DEFAULT_POST_PLUGIN**

Default template  to use for a single post. (default: 'post.html')

**GOSCALE_POSTS_UPDATE_FREQUENCY**

How often to update posts for plugins. (default: 60*30, 30 minutes)

**GOSCALE_UPDATE_FROM_ADMIN**

Should GoScale update posts right after saving the plugin in Django admin. (default: False)

**GOSCALE_CACHE_DURATION**

Cache duration for plugins content. (default: CMS_CACHE_DURATIONS['content'], the same as content cache duration in Django CMS)

**GOSCALE_POST_SUMMARY_LIMIT**

Where to trim post summary text. (default: 300)

**GOSCALE_DEFAULT_PAGE_SIZE**

Default number of posts per page. (default: 10)

**GOSCALE_DEFAULT_CONTENT_ORDER**

Default sorting for posts. (default: '-published')

2.3. Theme settings
---------------------

**SITE_ALIASES**

Allows to enable multiple hosts for one theme (for example local, dev, staging servers).

**THEME**

Sets currently enabled default theme (if not set by request).
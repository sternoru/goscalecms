Available plugins
====================

Contrary to Django CMS, GoScale plugins support multiple templates for one plugin. It's a powerful tool for customization.

All plugins have following optional fields by default:

* template - Plugin template to render
* title - Plugin title

And following system fields that never show up in Django admin:

* updated - time when content was updated last time
* posts - collection of posts associated with this plugin

Calendar
--------------------

Application: 'goscale.plugins.calendar'

Configuration options:

* url - Calendar feed URL (XML link from "Private Address" in your "Calendar Settings")
* page_size - Events per page (0 for unlimited)
* show_past - Show past events (If set past events will be shown)

Templates:

* events.html - Events list
* events_mini.html - Events mini list (for sidebar for example)
* datepicker.html - Date picker widget

Single post template: event.html

Additional templates can be added by setting GOSCALE_CALENDAR_CUSTOM_PLUGIN_TEMPLATES tuple in your settings.py

Feed
--------------------

Application: 'goscale.plugins.feeds'

Configuration options:

* url - Feed URL
* page_size - Posts per page (0 for unlimited)
* show_date - Show date in posts (If checked the date will be shown along with the post content)
* external_links - Open external links (If checked posts will link to the original source, otherwise will open internally)
* disqus - DICQUS shortname (Use it if you want to enable disqus.com comments)

Templates:

* posts.html - Posts
* posts_small.html - Small posts (for sidebar for example)

Single post template: post.html (default)

Additional templates can be added by setting GOSCALE_FEEDS_CUSTOM_PLUGIN_TEMPLATES tuple in your settings.py

Blogger and Tumblr
--------------------

Application: 'goscale.plugins.feeds'

Configuration options:

* url - Blog URL
* page_size - Posts per page (0 for unlimited)
* show_date - Show date in posts (If checked the date will be shown along with the post content)
* external_links - Open external links (If checked posts will link to the original source, otherwise will open internally)
* disqus - DICQUS shortname (Use it if you want to enable disqus.com comments)

Templates:

* posts.html - Posts
* posts_small.html - Small posts (for sidebar for example)

Single post template: post.html (default)

Additional templates can be added by setting GOSCALE_FEEDS_CUSTOM_PLUGIN_TEMPLATES tuple in your settings.py

Form
--------------------

Application: 'goscale.plugins.forms'

Configuration options:

* url - Google Form URL

Templates:

* form.html - Inline Form
* form_popup.html - Form in a lightbox

Additional templates can be added by setting GOSCALE_FORMS_CUSTOM_PLUGIN_TEMPLATES tuple in your settings.py

Picasa
--------------------

Application: 'goscale.plugins.pictures'

Configuration options:

* url - Picasa or Google+ user or album link
* width - Container width (Width of a slideshow container or a lightbox)
* height - Container height (Height of a slideshow container or a lightbox)
* thumbnail_width - Thumbnail width (Width of a thumbnail)
* thumbnail_height - Thumbnail height (Height of a thumbnail)
* autoplay  - Autoplay (If set slideshow will start automatically)

Templates:

* grid.html - Grid
* slideshow.html - Slideshow
* slideshow_with_thumbnails.html - Slideshow with thumbnails
* slideshow_mini.html - Mini slideshow (for sidebar for example)
* carousel_mini.html - Mini carousel

Additional templates can be added by setting GOSCALE_PICTURES_CUSTOM_PLUGIN_TEMPLATES tuple in your settings.py

YouKu
--------------------

Application: 'goscale.plugins.videos'

Configuration options:

* playlist - Youku playlist URL
* lightbox - Open videos in a lightbox (If checked videos will open in a lightbox, otherwise inline)

Templates:

* videos.html - Videos

Additional templates can be added by setting GOSCALE_VIDEOS_CUSTOM_PLUGIN_TEMPLATES tuple in your settings.py
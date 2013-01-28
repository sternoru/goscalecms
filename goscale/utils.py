# -*- coding: utf-8 -*-

import datetime
import urllib
import urllib2
import re
import os
import pytz

from goscale import conf
#from goscale import decorators
#from dynamicsettings import settings
#from goscale import feeds

from django.core.cache import cache #from google.appengine.api import memcache as cache

from django import http
from django.core import urlresolvers
from django.utils import html as html_utils
from django.utils import simplejson
from django.utils import translation
from django import template
from django.utils import importlib
from django.core import exceptions
from django.contrib.sites import models as site_models
from django.conf import settings
#
#
#def get_site(request):
#    if site_models.Site._meta.installed:
#        site = site_models.Site.objects.get_current()
#    else:
#        site = site_models.RequestSite(request)
#    return site
#
#def get_source_setting(source_name, setting_name):
#    return settings.GOSCALE_CONTENT_TYPES[source_name][setting_name]
#
#def get_template_setting(template_name, setting_name=None):
#    template = settings.GOSCALE_TEMPLATES[template_name]
#    if setting_name:
#        return template[setting_name]
#    return template
#
#def get_module_setting(module_name, setting_name):
#    return settings.GOSCALE_MODULES[module_name][setting_name]
#
##@decorators.cache_func
#def get_page_by_id(id):
#    try:
#        return models.Page.objects.get(id=id)
#    except models.Page.DoesNotExist:
#        return None
#
##@decorators.cache_func
#def get_all_pages():
#    ''' Caches DB request to models.Page.all().order('sort_id') '''
#    return list(models.Page.objects.all().order_by('sort_id'))
#
##@decorators.cache_func
#def get_page_by_absolute_url(url):
#    ''' Returns page object or raises raises HTTP404 if page not found'''
#    all_pages = get_all_pages()
#    if url=='/' or not url:
#        for page in all_pages:
#            if page.sort_id == 0:
#                return page
#    for page in all_pages:
#        if page.absolute_url == url:
#            return page
#    return None
#
##@decorators.cache_func
#def get_temporary_page(absolute_url, slug=None):
#    page_title = ''
#    if slug is not None:
#        try:
#            post = models.Post.objects.get(slug=slug)
#            page_title = post.title
#        except models.Post.DoesNotExist:
#            pass
#    page_titles = {}
#    for language_definition in settings.LANGUAGES:
#        page_titles[language_definition[0]] = page_title
#    page_attributes = {'title': page_titles}
#    return models.Page(
#        parent_page=None,
#        modules=None,
#        attributes=simplejson.dumps(page_attributes),
#        slug=slug,
#        template=None,
#        sort_id=1000,
#        visible=True,
#        login_required=False,
#        absolute_url=absolute_url,
#        languages=','.join([language_definition[0] for language_definition in settings.LANGUAGES]),
#    )
#
#def get_ajax_post(request, slug, format='html'):
#    posts_dir = settings.GOSCALE_POSTS_TEMPLATE_DIR
#    post = get_post_by_slug(slug)
#    post_type = post.content_type
#    post_json = post.json()
#    if format=='json':
#        ajax_content = post_json
#    elif format=='rss' or format=='atom':
#        self_link = 'http://%s%s' % (request.get_host(), request.get_full_path())
#        feed = feeds.XMLFeed(type=format,
#                          data=[post_json],
#                          title=post_json['title'] if post_json.get('title') is not None else '',
#                          description='',
#                          link=self_link)
#        ajax_content = feed.get_feed(object(), request).writeString(encoding='UTF-8')
#    else:
#        content_dict = {
#                    'data': post.json(),
#                   }
#        context_dict = dict(content=content_dict, request=request)
#        get_template = request.GET.get('template', None)
#        if get_template:
#            template_file = os.path.join(posts_dir, get_template)
#        else:
#            template_file = os.path.join(posts_dir, '%s.html' % post_type)
#        ajax_content = template.loader.render_to_string(template_file, context_dict)
#    return ajax_content
#
##@decorators.cache_func
#def get_breadcrumb(current_page, lang, def_lang, user):
#    breadcrumb_obj = []
#    while True:
#        breadcrumb_obj.append(single_page_menu_obj(current_page, lang, def_lang, user))
#        if not current_page.parent_page:
#            break
#        current_page = get_page_by_id(current_page.parent_page.pk)
#    breadcrumb_obj.reverse()
#    return breadcrumb_obj
#
##@decorators.cache_func
#def make_menu_obj(lang, def_lang, user, current_page=None):
#    """ Creates an object used to display menu. Object structure:
#    top level :  | * | * |-*-| * |
#    second lev:  |  *  |-*-|  *  |
#    current lev: |-*-| * | * | * | <--active page/parent nodes have attribute ['selected'] set
#    cur+1 lev:   etc.
#    ...
#    single node struct defined in single_page_menu_obj()
#
#    """
#    all_pages = get_all_pages()
#    menu_obj = []
#    children = []
#    """collect children - bottom level"""
#    for page in all_pages:
#        if current_page and page.parent_page and page.parent_page.id == current_page.id:
#            child = single_page_menu_obj(page, lang, def_lang, user)
#            if child:
#                children.append(child)
#    if children:
#        menu_obj.append(children)
#    """ collect siblings, parents and parent's siblings """
#    selected_page = current_page
#    while True:
#        sibling_pages = get_page_siblings(selected_page);
#        siblings = []
#        for sibling_page in sibling_pages:
#            sibling = single_page_menu_obj(sibling_page, lang, def_lang, user)
#            if not sibling:
#                continue
#            if selected_page and sibling_page.id == selected_page.id:
#                sibling['selected'] = True
#            siblings.append(sibling)
#        menu_obj.append(siblings)
#        if not selected_page:
#            break
#        if not selected_page.parent_page:
#            break
#        selected_page = get_page_by_id(selected_page.parent_page.id)
#    menu_obj.reverse()
#    return menu_obj
#
##@decorators.cache_func
#def single_page_menu_obj(page, lang, def_lang, user):
#    if page.visible is False or not lang in page.languages\
#    or (settings.GOSCALE_SHOW_PROTECTED_PAGES is False and page.login_required is True\
#        and user.is_anonymous() is True):
#        return None
#    ret_obj = {
#        'slug': page.slug,
#        'title': get_page_title(page, lang),
#        'url': page.absolute_url,
#    }
#    return ret_obj
#
##@decorators.cache_func
#def get_page_siblings(current_page):
#    all_pages = get_all_pages()
#    siblings = []
#    current_page_parent_key = None
#    if current_page and current_page.parent_page:
#        current_page_parent_key = current_page.parent_page.pk
#    for page in all_pages:
#        page_parent_key = None
#        if page.parent_page:
#            page_parent_key = page.parent_page.pk
#        if page_parent_key == current_page_parent_key:
#            siblings.append(page)
#    return siblings
#
#def get_page_title(page, lang):
#    return get_attribute_by_language(page, 'title', lang)
#
##@decorators.cache_func
#def get_language_from_path(url_path):
#    """
#    Returns language and url_path without language_prefix from the url
#    """
#    for language_definition in settings.LANGUAGES:
#        if url_path.startswith('/%s/' % language_definition[0]):
#            return language_definition[0]
#        if url_path=='/':
#            return conf.DEFAULT_LANGUAGE
#    return translation.get_language()
#
##@decorators.cache_func
#def get_absolute_url(url_path, lang):
#    if url_path.startswith('/%s/' % lang):
#        return url_path.replace('/%s' % lang, '', 1)
#    return url_path
#
##@decorators.cache_func
#def get_all_languages():
#    all_lang = []
#    for language_definition in settings.LANGUAGES:
#        all_lang.append([language_definition[0], language_definition[1]])
#    all_lang.sort(key=lambda language_tuple: language_tuple[1])
#    return all_lang
#
##@decorators.cache_func
#def get_languages(url_path):
#    return get_language_from_path(url_path), get_all_languages()
#
##@decorators.cache_func
#def get_language_redirect(url_path, lang, is_page=True):
#    user_lang = translation.get_language()
#    if user_lang != lang:
#        set_language_url = urlresolvers.reverse('set_language')
#        lang_prefix = get_language_prefix(lang, user_lang)
#        if user_lang == conf.DEFAULT_LANGUAGE:
#            url_path = url_path.replace(lang_prefix,'')
#        else:
#            url_path = url_path.replace(lang_prefix, '/%s' % user_lang)
#        redirect_url = '%s?%s=%s&language=%s' % (set_language_url,
#                                                 settings.REDIRECT_FIELD_NAME,
#                                                 url_path, user_lang)
#        if is_page is True:
#            redirect_url = '%s&is_page=1' % redirect_url
#        return redirect_url
#    return None
#
##@decorators.cache_func
#def get_language_prefix(lang, def_lang):
#    if lang==def_lang:
#        return ''
#    else:
#        return '/%s' % lang
#
def process_feed_tz_delta(date_string):
    date_match = re.findall('[\-\+]\d{2}:?\d{2}', date_string)
    if date_match:
        factor = 1
        tz_string = date_match[0].replace(':', '')
        if tz_string.startswith('-'):
            factor = -1
        tz_delta = ((int(tz_string[-4:-2]) * 3600) + (int(tz_string[-2:]) * 60)) * factor
        return tz_delta
    return 0

def get_datetime_now():
    """ Returns now() in UTC timezone

    More info: http://pytz.sourceforge.net/
    """
    return datetime.datetime.now(tz=pytz.utc)

def get_utc(dt):
    """ Converts datetime to UTC timezone

    More info: http://pytz.sourceforge.net/
    """
    return dt.replace(tzinfo=pytz.utc)

def get_datetime_by_parsed(pDate, tz_delta=0):
    if not pDate:
        return None
    dt = datetime.datetime(pDate[0], pDate[1],pDate[2], pDate[3], pDate[4], pDate[5]) + datetime.timedelta(seconds=tz_delta)
    return get_utc(dt)

##@decorators.cache_func
#def get_params(data_source_dict, data_source_obj):
#    """Intersect a data_source dict and a data_source_obj and returns a dict
#    """
#    ret_dict = data_source_dict
#    try:
#        ret_dict.update(simplejson.loads(data_source_obj.attributes))
#    except ValueError:
#        pass
#    ret_dict.update({
#                     'source_id': data_source_obj.source_id,
#                     'type': data_source_obj.type,
#                    })
#    return ret_dict
#
#def get_params_from_request(request, exclude=None):
#    """Returns additional datasource params from request
#    """
#    if exclude is None:
#        exclude = []
#    ret_dict = {}
#    for key, value in request.GET.iteritems():
#        if key not in exclude:
#            ret_dict[key] = value
#    return ret_dict

def get_short_summary(html):
    max_length_shortcontent = conf.GOSCALE_POST_SUMMARY_LIMIT
    content_temp = html_utils.strip_tags(html)
    if len(content_temp) < max_length_shortcontent:
        return content_temp
    shortcontent_temp = content_temp[:max_length_shortcontent]
    if shortcontent_temp.rfind('.') != -1:
        shortcontent_temp = shortcontent_temp[:shortcontent_temp.rfind('.')+1]
    else:
        shortcontent_temp = shortcontent_temp[:shortcontent_temp.rfind(' ')+1] + '...'
    return shortcontent_temp

##@decorators.cache_func
#def filter_content_types(content_type):
#    return [class_name for class_name in settings.GOSCALE_CONTENT_TYPES if settings.CONTENT_TYPES['class_name'].get('type') == content_type]
#
##@decorators.cache_func
#def get_source_by_url(url):
#    try:
#        return models.DataSource.objects.get(url=url)
#    except models.DataSource.DoesNotExist:
#        raise #for now
#        return None
#
##@decorators.cache_func
#def get_source_by_id(source_id):
#    try:
#        return models.DataSource.objects.get(source_id=source_id)
#    except models.DataSource.DoesNotExist:
#        raise #for now
#        return None
#
##@decorators.cache_func
#def get_attribute_by_language(page, attr_name, lang):
#    try:
#        attributes = simplejson.loads(page.attributes)
#    except ValueError:
#        #raise ValueError('Attribute "%s" for page "%s" and language "%s" could not be decoded.' % (attr_name, page, lang))
#        attributes = {}
#    attribute = attributes.get(attr_name)
#    if attribute:
#        return attribute.get(lang) or attribute.get(conf.DEFAULT_LANGUAGE) or attribute[attribute.keys()[0]] or None
#    return None
#
##@decorators.cache_func
#def get_all_modules():
#    return list(models.Module.objects.all())
#
##@decorators.cache_func
#def get_module_by_module_id(module_id):
#    try:
#        return models.Module.objects.get(module_id=module_id)
#    except models.Module.DoesNotExist:
#        raise #for now
#        return None
#
##@decorators.cache_func
#def get_modules_by_module_ids(module_ids):
#    #list() is evaluating the queryset, so the results are cached, not the queryset
#    return list(models.Module.objects.filter(module_id__in=module_ids))
#
##@decorators.cache_func
#def get_modules_for_page(page, language=conf.DEFAULT_LANGUAGE):
#    """Get the module objects for a given page,language
#    """
#    try:
#        page_modules = simplejson.loads(page.modules)
#    except ValueError:
#        page_modules = []
#    modules = []
#    for page_module in page_modules:
#        module_dict = {}
#        module = get_module_by_module_id(page_module['id'])
#        module_dict.update(page_module)
#        #try:
#        #    module_json = simplejson.loads(module.data_sources)
#        #except ValueError:
#        #    #raise ('Data sources for module "%s" on page "%s" and language "%s" could not be decoded.' % (module, page, lang))
#        #    module_json = {}
#        #if language in module_json:
#        module_dict.update(settings.GOSCALE_MODULES[module.type])
#        module_dict['title'] = simplejson.loads(module.title).get(language, "")
#        module_dict['attributes'] = simplejson.loads(module.attributes).get(language, None)
#        modules.append(module_dict)
#    return modules
#
##@decorators.cache_func
#def get_module_class(module_type):
#    module_name_parts = module_type.split('_')
#    return '%sModule' % (''.join([part.title().replace(' ','') for part in module_name_parts]))
#
##@decorators.cache_func
#def get_modules_for_panel(modules, panel):
#    modules_to_render = []
#    module_number = 0 #the module number (index) in the given panel
#    for module in modules:
#        try:
#            module_panel = module['panel']
#        except TypeError:
#            module_panel = module.panel
#        if panel==module_panel:
#            #add container and class to module
#            module['container'] = '%s-module%s' % (panel.replace(' ','_'), module_number)
#            module['class'] = get_module_class(module['type'])
#            modules_to_render.append(module)
#            module_number += 1
#    return modules_to_render
#
##@decorators.cache_func
#def get_post_by_slug(slug):
#    try:
#        return models.Post.objects.get(slug=slug)
#    except models.Module.DoesNotExist:
#        raise #for now
#        return None
#
#def get_unique_panels(page):
#    try:
#        page_panels = get_template_setting(page.template, 'panels')
#    except KeyError:
#        page_panels = []
#    for panel in settings.GOSCALE_COMMON_PANELS:
#        if panel not in page_panels:
#            page_panels.append(panel)
#    return page_panels
#
#def create_task(params):
#    try:
#        from google.appengine.api.labs import taskqueue
#        return taskqueue.add(url=urlresolvers.reverse('task_handler'), params=params, method='GET')
#    except ImportError:
#        pass #additional code for django only version later
#
##@decorators.cache_func
#def unpack_hash(hash_string):
#    if hash_string.startswith('#!'):
#        hash_string = hash_string.replace('#!', '')
#    hash_module_dict = {}
#    hash_modules = hash_string.split('|')
#    for hash_module in hash_modules:
#        module_hash_name = hash_module[0:hash_module.find('=')]
#        module_name = module_hash_name[hash_module.find('_')+1:]
#        module_hash_params = hash_module.replace('%s=' % module_hash_name, '')
#        module_params = {}
#        for hash_param in module_hash_params.split(';'):
#            param_module = hash_param.split('=')
#            if len(param_module)==1:
#                key = value = hash_param
#            elif len(param_module)==2:
#                key, value = hash_param.split('=')
#            else:
#                raise ValueError('Wrong hash formatting. To many  values separated by ``=`` for module parameters.')
#            module_params[key] = value
#        hash_module_dict[module_name] = module_params
#    return hash_module_dict
#
##@decorators.cache_func
#def pack_hash(hash_dict):
#    hash_list = []
#    for module_key in hash_dict.keys():
#        params_module_list = []
#        for param_key in hash_dict[module_key].keys():
#            param_value = hash_dict[module_key][param_key]
#            if param_key==param_value:
#                params_module_list.append(param_key)
#            else:
#                params_module_list.append('%s=%s' % (param_key, param_value))
#        hash_list.append('mod_%s=%s' % (module_key, ';'.join(params_module_list)))
#    return '#!%s' % '|'.join(hash_list)
#
#def modify_ajax_links(request, posts):
#    """Call this function only when you need to make content crawlable
#    """
#    url_path = request.path_info
#    get_dict = request.GET.copy()
#    if get_dict.get('_escaped_fragment_') is not None:
#        del get_dict['_escaped_fragment_']
#    full_url = '%s%s'
#    if len(get_dict)>0:
#        full_url = '%s?%s'
#    full_url = full_url % (url_path, '&'.join(['%s=%s' % (key, value) for key, value in get_dict.items()]))
#    for i, post in enumerate(posts):
#        posts[i]['ajax_link'] = '%s%s' % (full_url, post['ajax_link'])
#    return posts
#
#
##@decorators.cache_func
#def get_ajax_url(content_type, page, lang, data_source_index, output=None, offset=None, limit=None):
#    ajax_params = {
#        'type': content_type,
#        'page': page.absolute_url,
#        'language': lang,
#        'source': data_source_index,
#    }
#    if output:
#        ajax_params['output'] = output
#    if offset:
#        ajax_params['offset'] = offset
#    if limit:
#        ajax_params['limit'] = limit
#
#    join_at = '?' if ajax_params else ''
#    ajax_url = join_at.join([
#                '%s' % (urlresolvers.reverse('ajax')),
#                '&'.join(['%s=%s' % (param, ajax_params[param]) for param in ajax_params])
#    ])
#    return ajax_url
#
##@decorators.cache_func
#def get_data_sources_for_ids(source_ids):
#    return list(models.DataSource.objects.filter(source_id__in=source_ids))
#
##@decorators.cache_func
#def get_posts_for_data_sources(data_sources, **kwargs):
#    posts = models.Post.objects.filter(data_source__in=data_sources)
#    if 'order_by' in kwargs:
#        posts = posts.order_by(kwargs['order_by'])
#    if 'offset' in kwargs and 'limit' in kwargs:
#        return posts[kwargs['offset']:kwargs['limit']]
#    return list(posts)
#
#def read_cookie(request, cookie_name):
#    return request.COOKIES.get(cookie_name)
#
#def read_tz_delta_cookie(request):
#    tz_delta = read_cookie(request, 'user_tz_delta')
#    if tz_delta is None:
#        return settings.GOSCALE_STANDARD_TZ_DELTA*60
#    return int(tz_delta)
#
#def get_request_from_context(context):
#    request = context.get('request')
#    if not request:
#        raise template.TemplateSyntaxError('No template variable "request" in the context. Please add the ``django.core.context_processors.request`` context processors to your settings.TEMPLATE_CONTEXT_PROCESSORS set')
#    return request
#
def dict2obj(d):
    """A helper function which convert a dict to an object.
    """
    if isinstance(d, (list, tuple)):
        d = [dict2obj(x) for x in d]
    if not isinstance(d, dict):
        return d
    class ObjectFromDict(object):
        pass
    o = ObjectFromDict() #an object created from a dict
    for k in d:
        o.__dict__[k] = dict2obj(d[k])
    return o
#
def forge_request(url):
    """A helper function which forges a request for fetching json from vimeo and youku.
    """
    return urllib2.Request(url, None, { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' })
#
#
#def get_class_for_path(path):
#    i = path.rfind('.')
#    module, attr = path[:i], path[i+1:]
#    try:
#        mod = importlib.import_module(module)
#    except ImportError, e:
#        raise exceptions.ImproperlyConfigured('Error loading class %s: "%s"' % (module, e))
#    try:
#        module_class = getattr(mod, attr)
#    except AttributeError:
#        raise exceptions.ImproperlyConfigured('Module "%s" does not define a class named "%s"' % (module, attr))
#    return module_class
#
#def queue2tree(comments_queue, comments_tree):
#    while len(comments_queue)!=0:
#        comment = comments_queue.popleft()
#        if not recursively_parse_comment_tree(comment, comments_tree):
#            comments_queue.append(comment)
#
#
#def recursively_parse_comment_tree(comment, nested_comment_tree):
#    # if the comment does not have a parent comment, then append the node directly to the tree.
#    if not comment.parent_comment:
#        nested_comment_tree.append({
#            'comment': comment.dict(),
#            'children': []
#        })
#        return True
#    # else the comment has a parent.
#    for comment_node in nested_comment_tree:
#        # go through every node in the tree, if the comment's parent is there, then append the noce to the children of such commet.
#        # if not, check the children of this comment.
#        # whenever found one, this function will return True.
#        # if a true is cought inside of the for loop, exit the loop and return directly.
#        if comment.parent_comment.id == comment_node['comment']['id']:
#            comment_node['children'].append({
#                'comment': comment.dict(),
#                'children': []
#            })
#            return True
#        if recursively_parse_comment_tree(comment, comment_node['children']):
#            return True
#    return False
#
#def comment_is_prepend():
#    default_ordering = settings.GOSCALE_DEFAULT_COMMENTS_SORTING_ORDER
#    if default_ordering[:1] == '-':
#        return 'true'
#    return 'false'
#
#def nested_remove_comment(comment):
#    parent_comment = comment.parent_comment
#    if not parent_comment:
#        return remove_comment(comment)
#    if not parent_comment.is_removed:
#        return remove_comment(comment)
#    parent_sublings = models.Comment.objects.filter(parent_comment = parent_comment)
#    if len(parent_sublings)!=1:
#        # in this case, there are more children in this parent_comment, then just delete the comment.
#        return remove_comment(comment)
#    else:
#        # in this case, such parent has only one child and this child is being removed.
#        # check nested_removed_comment(parent_comment)
#        id_to_remove = nested_remove_comment(parent_comment)
#    return str(id_to_remove)
#
#def remove_comment(comment):
#    id_to_remove = comment.id
#    comment.delete()
#    return str(id_to_remove)
#
#def add_label_filter(query, label):
#    if label:
#        label = '[%s]' % label
#        query = query.filter(categories__contains=label)
#    return query
#
#def weighted_rating(rating, votes, minimum_votes=settings.GOSCALE_RATING_MINIMUM_VOTES, mean_value=settings.GOSCALE_RATING_MEAN_VALUE):
#    """Bayesian estimate
#    rating- average for the picture
#    votes - number of votes for the picture
#    m - minimum votes required to be listed
#    mean_value - the mean vote across the whole report
#    """
#    if votes==0:
#        return 0.0
#    return (float(votes) / (float(votes) + float(minimum_votes))) * float(rating) + (float(minimum_votes) / (float(votes) + float(minimum_votes))) * float(mean_value)
#
#def send_comment_replied_email(request, parent_comment, comment):
#    site = get_site(request)
#    user = parent_comment.user
#    content_dict = {
#        'site': site,
#        'username': user.username,
#        'parent_comment': parent_comment.comment,
#        'comment': comment.comment,
#        'reply_from': comment.user.username,
#        'path': parent_comment.get_content_object_url(),
#    }
#    comment_replied_subj_template = os.path.join(settings.GOSCALE_ROOT_TEMPLATE_DIR, 'comments', 'email', 'email_comment_replied_subject.txt')
#    subject = template.loader.render_to_string(comment_replied_subj_template, content_dict)
#    # Email subject *must not* contain newlines
#    subject = ''.join(subject.splitlines())
#    comment_replied_msg_template = os.path.join(settings.GOSCALE_ROOT_TEMPLATE_DIR, 'comments', 'email', 'email_comment_replied.txt')
#    message = template.loader.render_to_string(comment_replied_msg_template, content_dict)
#    user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
#
#def send_comment_deleted_email(request, comment):
#    site = get_site(request)
#    user = comment.user
#    content_dict = {
#        'site': site,
#        'username': user.username,
#        'comment': comment.comment,
#        'path': comment.get_content_object_url(),
#    }
#    comment_deleted_subj_template = os.path.join(settings.GOSCALE_ROOT_TEMPLATE_DIR, 'comments', 'email', 'email_comment_deleted_subject.txt')
#    subject = template.loader.render_to_string(comment_deleted_subj_template, content_dict)
#    # Email subject *must not* contain newlines
#    subject = ''.join(subject.splitlines())
#    comment_deleted_msg_template = os.path.join(settings.GOSCALE_ROOT_TEMPLATE_DIR, 'comments', 'email', 'email_comment_deleted.txt')
#    message = template.loader.render_to_string(comment_deleted_msg_template, content_dict)
#    user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
#
#def get_redirect_value(request):
#    redirect_field_name = settings.REDIRECT_FIELD_NAME
#    if redirect_field_name in request.session:
#        redirect_to = request.session[redirect_field_name]
#        del request.session[redirect_field_name]
#    elif redirect_field_name in request.COOKIES:
#        redirect_to = urllib2.unquote(request.COOKIES[redirect_field_name])
#    elif redirect_field_name in request.GET:
#        redirect_to = request.GET.get(redirect_field_name)
#    elif redirect_field_name in request.POST:
#        redirect_to = request.POST.get(redirect_field_name)
#    else:
#        redirect_to = settings.get('LOGIN_REDIRECT_URL', '/')
#    if not redirect_to or ' ' in redirect_to:
#        redirect_to = settings.get('LOGIN_REDIRECT_URL', '/')
#    elif '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
#        redirect_to = settings.get('LOGIN_REDIRECT_URL', '/')
#    return redirect_to
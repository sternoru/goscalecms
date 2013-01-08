# -*- coding: utf-8 -*-

import hashlib

from django.core.cache import cache
from goscale import conf


def optional_arguments(func):
    def meta_wrapper(*args, **kwargs):
        if len(args) == 1 and callable(args[0]):
            # No arguments, this is the decorator
            # Set default values for the arguments
            return func(args[0])
        else:
            def meta_func(inner_func):
                return func(inner_func, *args, **kwargs)
            return meta_func
    return meta_wrapper

@optional_arguments
def cache_func(func, duration=conf.GOSCALE_CACHE_DURATION, cache_key=None):
    """Django cache decorator for functions
    
    Basic ideas got from:
    - http://djangosnippets.org/snippets/492/
    - http://djangosnippets.org/snippets/564/

    Example usage:

    Example 1:
    - providing a cache key and a duration
    class MenuItem(models.Model):
        @classmethod
        @cache_func(, 3600*24, 'menu_root')
        def get_root(self):
            return MenuItem.objects.get(pk=1)

    Example 2:
    - providing a dynamic cache key and a duration
    @cache_func(3600, lambda u: 'user_privileges_%s' % u.username,)
    def get_user_privileges(user):
        #...
        
    Example 3:
    - providing only a duration of the cache, if no cache is provided it will
    be auto-generated
    @cache_func(1800)
    def get_page_by_absolute_url(url):
        #...
    """    
    def do_cache(*args, **kwargs):
        alternative_cache_key = '%s.%s' %  (func.__module__, func.__name__)
        key = get_cache_key(cache_key, alternative_cache_key, *args, **kwargs)
        data = cache.get(key)
        if data: 
            return data
        data = func(*args, **kwargs)
        #in case a function is not False (implicit), so object couldn't be retrieved
        cache_duration = duration
        if not data:
            cache_duration = 1
        cache.set(key, data, cache_duration)
        return data
    return do_cache

def get_cache_key(cache_key, alternative_cache_key, *func_args, **func_kwargs):
    """Not a decorator, but a helper function to retrieve the cache
    key for a cached function with its arguments or keyword arguments.
    Also used to create the cache key in the first place (cache_func decorator).
    Args:
        - cache_key: if there was a specific cache key used to cache the
        function, it should be provided here. If not this should be None
        - alternative_cache_key: a cache key with the following syntax
        full_module_name.decorated_function_name (for example 'goscale.utils.get_language_from_path)
        NOTE: This is done since a decorated function call always return the 
        do_cache function from the decorator, but never itself
        - *func_args: original arguments of the decorated function
        NOTE: strings as args/kwargs might be unicode and instead of passing
        'string' to the function u'string' need to be passed to
        - **func_kwargs: keyword arguments of the decorated function
    """
    if not cache_key:
        key = hashlib.sha1('%s.%s.%s' % (alternative_cache_key, func_args, func_kwargs)).hexdigest() #alternative_cache_key + str(func_args) + str(func_kwargs)
    elif isinstance(cache_key, (str, unicode)):
        key = hashlib.sha1(cache_key % locals()).hexdigest()
    elif callable(cache_key):
        key = hashlib.sha1(cache_key(*func_args, **func_kwargs)).hexdigest()
    return key

def get_cached_item(cache_key, alternative_cache_key, *func_args, **func_kwargs):
    """Not a decorator, but a helper function to retrieve the cached
    item for a key created via get_cache_key.
    Args:
        - cache_key: if there was a specific cache key used to cache the
        function, it should be provided here. If not this should be None
        - func: the function which was cache
        - *func_args: arguments of the function
        - **func_kwargs: keyword arguments of this function
    """
    key = get_cache_key(cache_key, func, *func_args, **func_kwargs)
    return cache.get(key)

@optional_arguments
def cache_user_page(func, duration=conf.GOSCALE_CACHE_DURATION):
    def do_cache(request, *args, **kwargs):
        if hasattr(request.user, 'email') and request.user.email is not None:
            cache_key ='page_%s_%s:%s' % (request.path_info, request.user.username, request.user.email)
        else:
            cache_key ='page_%s_%s' % (request.path_info, request.user.username)
        data = cache.get(cache_key)
        if data: 
            return data
        data = func(request, *args, **kwargs)
        #in case a function is not False (implicit), so object couldn't be retrieved
        cache_duration = duration
        if not data:
            cache_duration = 1
        cache.set(cache_key, data, cache_duration)
        return data
    return do_cache


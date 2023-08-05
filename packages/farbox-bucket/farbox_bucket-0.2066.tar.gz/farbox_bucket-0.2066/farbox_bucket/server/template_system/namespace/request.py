# coding: utf8
from flask import request as _request
import copy, re, os, time
from farbox_bucket.utils.functional import cached_property
from farbox_bucket.utils import to_unicode, to_int, string_types, smart_str
from farbox_bucket.utils.url import join_url
from farbox_bucket.utils.mime import guess_type
from farbox_bucket.server.utils.cache_for_function import cache_result
from farbox_bucket.server.utils.request_path import get_request_path, get_request_offset_path
from farbox_bucket.server.utils.request import get_language
from farbox_bucket.server.utils.request_context_vars import get_url_prefix_in_request, set_not_cache_current_request
from farbox_bucket.server.utils.cookie import set_cookie as _set_cookie, get_cookie as _get_cookie,\
    delete_cookies as _delete_cookies

system_cookie_keys = ["last_visited_at", "utoken", "verification_code", "vid"]


def get_url_without_prefix(url, prefix=None):
    # url 去除 prefix 后， 一般以 '/' 开头
    if not isinstance(url, string_types):
        return url # ignore
    url_startswith_dash = url.startswith('/')
    raw_url = url
    if prefix is None:
        prefix = get_url_prefix_in_request() or ""
    if prefix and isinstance(prefix, string_types):
        url = url.lstrip('/')
        prefix = prefix.strip().strip('/')
        if url.startswith(prefix+'/') or url == prefix:
            first_char = '/' if url_startswith_dash else ''
            url =  first_char + url.replace(prefix, '', 1).lstrip('/')
            # 确保模拟 request.path 类似的逻辑，一般可以保证 / 开头的
            return url
    return raw_url


def get_visitor_ip():
    # 得到访客的 ip
    if _request.remote_addr: # 比如 nginx 过来的，proxy-pass & 走 unix socket 的缘故，remote_addr 会是空的, 而是打到 X-Forwarded-For 上
        return _request.remote_addr
    else:
        ip = _request.environ.get('HTTP_X_FORWARDED_FOR') or ''
        if ip:
            return ip
        elif _request.access_route:
            return _request.access_route[-1].strip()
        else:
            return ''



class Request(object):
    def __init__(self):
        self.url_fields = ['path', 'url', 'base_url', 'url_root', ]
        self.fields = ['form', 'args', 'values', 'method',
              'json', 'host', 'data', 'account_id', 'form', 'args', 'values', 'method', 'data', 'referrer',]
        self.__setattr__ = lambda key,value: None # not allowed

        self.set_property_allowed = True


    def __getattr__(self, item):
        if item == 'refer':
            item = 'referrer'
        if item in self.url_fields:
            # url 相关的调用, 要先过滤掉prefix
            value = getattr(_request, item, None)
            return get_url_without_prefix(value)
        elif item.startswith('_') and item.lstrip('_') in self.url_fields:
            # 比如 request._path, request._url 返回原始的 _request 上属性
            real_item = item.lstrip('_')
            value = getattr(_request, real_item, None)
            return value
        elif item in self.fields:
            return getattr(_request, item, None)
        elif item == 'url_without_host':
            return _request.url.replace(_request.url_root, '/')
        elif item == 'user_agent':
            user_agent = copy.copy(_request.user_agent)
            user_agent._parser = None
            return user_agent
        elif re.match('^_?path_?\d+$', item): # request.path1
            offset_c = re.search('\d+', item)
            i = offset_c.group()
            return self.get_n_path(i, raw=item.startswith('_'))
        elif re.match('^_?offset_path_?\d+$', item): # request.offset_path_1
            offset_c = re.search('\d+', item)
            i = offset_c.group()
            return self.get_offset_path(i, raw=item.startswith('_'))
        else:
            return self.__dict__.get(item)

    def get_offset_path(self, offset=None, raw=True):
        offset = to_int(offset) or 1
        path = get_request_path()
        if not raw:
            path = get_url_without_prefix(path)
        return get_request_offset_path(offset, path=path)


    @cached_property
    def web_path(self):
        request_path = get_request_path()
        request_path = '/' + request_path.lstrip('/')
        return request_path


    @cached_property
    def raw_user_agent(self):
        return _request.environ.get('HTTP_USER_AGENT') or ''


    @cached_property
    def ip(self):
        return get_visitor_ip()


    @cached_property
    def protocol(self):
        protocol = _request.environ.get('HTTP_X_PROTOCOL') or 'http'
        return protocol.lower()

    @cached_property
    def domain(self):
        return _request.host.lower()

    @cached_property
    def is_https(self):
        return self.protocol=='https'

    @cached_property
    def ext(self):
        return self.get_ext()

    @cached_property
    def mime_type(self):
        return self.get_mime_type()

    @cached_property
    def lang(self):
        return get_language() or ""

    @cached_property
    def language(self):
        return get_language() or ""


    def get_mime_type(self, path=''):
        if not isinstance(path, string_types):
            path = to_unicode(path)
        path = path or _request.path
        if path and isinstance(path, string_types):
            return guess_type(path) or ''
        else:
            return ''


    def get_ext(self, path=''):
        if not isinstance(path, string_types):
            path = to_unicode(path)
        path = path or _request.path
        ext = os.path.splitext(path)[-1] or ''
        ext = ext.lstrip('.').lower()
        return ext

    @staticmethod
    def join(base_url, **kwargs):
        if isinstance(base_url, string_types):
            return join_url(base_url, **kwargs)
        else:
            return base_url

    def set_cookie(self, key, value, max_age=10*60):
        if not isinstance(key, string_types): return ""
        if key in system_cookie_keys: return ""
        value = smart_str(value)
        _set_cookie(key, value, max_age=max_age)
        return ""

    def get_cookie(self, key, max_age=None):
        if not isinstance(key, string_types): return ""
        if key in system_cookie_keys: return ""
        return _get_cookie(key, max_age=max_age) or ""

    def delete_cookie(self, key):
        if not isinstance(key, string_types): return ""
        if key in system_cookie_keys: return ""
        _delete_cookies(key)
        return ""

    def set_no_cache(self):
        set_not_cache_current_request()
        return ""




@cache_result
def request():
    return Request()
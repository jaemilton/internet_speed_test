#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from cacheout import Cache
import os, json
from datetime import datetime
from collections import OrderedDict

class CacheUtil(object):
    
    CACHE_PATH=f"{os.path.dirname(os.path.abspath(__file__))}/.cached"
    CACHE_PATH_EXPIRE_TIMES=f"{os.path.dirname(os.path.abspath(__file__))}/.cached_expire_times"
    def __init__(self) -> None:
        self._load_cache()


    def _load_cache(self):
        self.cached = Cache()
        expire_times:dict=None
        cache_contents:OrderedDict=None
        if os.path.exists(self.CACHE_PATH_EXPIRE_TIMES):
            with open(self.CACHE_PATH_EXPIRE_TIMES) as file:
                expire_times = json.load(file)

        if os.path.exists(self.CACHE_PATH):
            with open(self.CACHE_PATH) as file:
                cache_contents = json.load(file)
                for cache_key in cache_contents:
                    if cache_key is not None:
                        if expire_times is not None and cache_key in expire_times:
                            expires_at = datetime.fromtimestamp(expire_times[cache_key])
                            if expires_at > datetime.now():
                                ttl=(expires_at - datetime.now()).seconds
                                self.cached.set(key=cache_key, value=cache_contents[cache_key], ttl=ttl)

    def __dump_cache(self, cache_path:str, json_dump:str):
        if os.path.exists(cache_path):
            os.remove(cache_path)

        with open(cache_path, "a") as file:
            file.write(json_dump)

    def _save_cache(self):
        self.__dump_cache(self.CACHE_PATH, json.dumps(self.cached.copy()))
        self.__dump_cache(self.CACHE_PATH_EXPIRE_TIMES, json.dumps(self.cached.expire_times()))
        
    def _get_cached_value(self, key:str, func_get_value, force_update:bool=False, **kwargs):
        cached_value = self.cached.get(key)
        if force_update and cached_value is not None:
            self.cached.delete(key=key)
            cached_value = None
        
        if cached_value is None:
            (cached_value, ttl) = func_get_value(**kwargs)
            self.cached.set(key=key, value=cached_value, ttl=ttl)
            self._save_cache()
            
        return cached_value
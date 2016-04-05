# coding: utf-8
from publisher.manager import PublisherManager
from library import FMT_VID, FMT_AUD, FMT_DOC, FMT_IMG


class BaseManager(PublisherManager):
    def get_query_set(self):
        return super(BaseManager, self).get_query_set().filter(
            type__exact=self.get_type())


class VideoManager(BaseManager):
    def get_type(self):
        return FMT_VID


class AudioManager(BaseManager):
    def get_type(self):
        return FMT_AUD


class DocumentManager(BaseManager):
    def get_type(self):
        return FMT_DOC


class PictureManager(BaseManager):
    def get_type(self):
        return FMT_IMG

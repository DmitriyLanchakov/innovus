import haystack
from indexer.search_indexes.article import ArticleIndex
from periodics.models import Post
from indexer.search_indexes.person import PersonIndex
from library.models import Person, Picture, Video, Audio, Document
from cms.plugins.text.models import Text
from indexer.search_indexes.text import TextIndex
from indexer.search_indexes.resource import ResourceIndex

haystack.site.register(Post, ArticleIndex)
haystack.site.register(Person, PersonIndex)
haystack.site.register(Text, TextIndex)
haystack.site.register(Picture, ResourceIndex)
haystack.site.register(Video, ResourceIndex)
haystack.site.register(Audio, ResourceIndex)
haystack.site.register(Document, ResourceIndex)

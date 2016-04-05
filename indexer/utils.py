import math
from cms.utils import get_language_from_request
from pysolr import Solr
from annoying.functions import get_config


def get_category_ids(language):
    agregates = get_config('NEWS_AGREGATE_CATEGORIES', {}).get(language, None)

    if not agregates:
        return list()

    category_ids = list()
    for key, value in agregates.items():
        category_ids += list(value)

    return category_ids

LOGARITHMIC, LINEAR = 1, 2

def _calculate_thresholds(min_weight, max_weight, steps):
    delta = (max_weight - min_weight) / float(steps)
    return [min_weight + i * delta for i in range(1, steps + 1)]



def _calculate_tag_weight(weight, max_weight, distribution):
    """
    Logarithmic tag weight calculation is based on code from the
    `Tag Cloud`_ plugin for Mephisto, by Sven Fuchs.

    .. _`Tag Cloud`: http://www.artweb-design.de/projects/mephisto-plugin-tag-cloud
    """
    try:
        if distribution == LINEAR or max_weight == 1:
            return weight
        elif distribution == LOGARITHMIC:
            return math.log(weight) * max_weight / math.log(max_weight)
    except ValueError, e:
        return 0.1
    raise ValueError(_('Invalid distribution algorithm specified: %s.') % distribution)



def calculate_cloud(request, steps=4, distribution=LOGARITHMIC, min_count=5):
    """
    Add a ``font_size`` attribute to each tag according to the
    frequency of its use, as indicated by its ``count``
    attribute.

    ``steps`` defines the range of font sizes - ``font_size`` will
    be an integer between 1 and ``steps`` (inclusive).

    ``distribution`` defines the type of font size distribution
    algorithm which will be used - logarithmic or linear. It must be
    one of ``tagging.utils.LOGARITHMIC`` or ``tagging.utils.LINEAR``.
    """
    language = get_language_from_request(request)

    tag_counts = get_solr_tagcloud(language=language)

    if len(tag_counts) > 0:
        counts = [i['count'] for i in tag_counts.values()]
        min_weight = float(min(counts))
        max_weight = float(max(counts))
        thresholds = _calculate_thresholds(min_weight, max_weight, steps)

        for tag_str in tag_counts.keys():
            font_set = False
            tag_weight = _calculate_tag_weight(
                tag_counts[tag_str]['count'],
                max_weight,
                distribution
            )

            for i in xrange(steps):
                if not font_set and tag_weight <= thresholds[i]:
                    tag_counts[tag_str]['font'] = i + 1
                    font_set = True
        #

    # Cut off the data at the minimum count
    tag_list = [
        dict(
            tag       = k,
            font_size = v['font'],
            count     = v['count']
        ) for k, v in tag_counts.items() if v['count'] >= min_count
    ]

    # Sort by alphabet
    tag_list.sort(lambda x,y: cmp(x['tag'].lower(), y['tag'].lower()))

    # Reverse that
#    debug(tag_list)
    return tag_list


def get_solr_tagcloud(language='ru'):
    tag_info = {}
    try:
        solr = Solr(get_config('HAYSTACK_SOLR_URL', 'http://127.0.0.1:8983/solr'))

        kwargs = {
            'facet': 'on',
            'facet.field': 'tags',
            'rows': 0,
            'start': 1
        }
        result = solr.search(q = 'language:%s' % language, **kwargs)
        tags = result.facets['facet_fields']['tags']
        tags_len = len(tags)
        for i, item in enumerate(tags):
            if not i%2:
                if i < tags_len-1:
                    tag_info.update({ item: {'count': tags[i+1], 'font': None }})
    except:
        pass

    return tag_info


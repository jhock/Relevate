from ...profiles.models.university_model import Universities
import re
from django.db.models import Q


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    '''
    Splits the query string in invidual keywords, getting rid of unecessary spaces
    and grouping quoted words together.
        Example:
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    '''
    Returns a query, that is a combination of Q objects. That combination
    aims to search keywords within a model by testing the given search fields.

    :param query_string: the search word
    :param search_fields: the field of the ORM model to search for that word in

    :return: An appropiate query string that django can call an object filter on.
    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
                #elif could cause problems, it was added to keep the search from returning duplicates. if breaks, change back to else
            elif q not in or_query:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def find_universities(key_word):
    '''
    Runs the search algorithm for grabbing user's university.

    :param key_word: User real time entries while searching for a university

    :return: A string list of suggested university names
    '''
    uni_list = []
    university = get_query(key_word, ['name_of_university'])
    university = Universities.objects.filter(university)
    for each_uni in university:
        uni_list.append(each_uni.name_of_university)
    return uni_list
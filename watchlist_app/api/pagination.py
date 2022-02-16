from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

#For pageNumberPagination
class WatchListPagination(PageNumberPagination):
    page_size = 10
    #Classifies the name of the string used when specifying a parameter
    page_query_param = 'p'
    #Classifies the size of the parameter
    page_size_query_param = 'size'
    #Sets the maximum page size for an individual page
    max_page_size = 10
    last_page_strings = 'end'

#For LimitOffsetPagination
class WatchListLOPagination(LimitOffsetPagination):
    default_limit = 5
    limit_query_param = 'limit'
    offset_query_param = 'start'

#For cursor pagination
class WatchListCPagination(CursorPagination):

    page_size = 5
    ordering = 'created'
    cursor_query_param = 'record'
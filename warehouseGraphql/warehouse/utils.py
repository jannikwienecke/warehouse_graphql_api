
from django.db.models import Q

import operator
from functools import reduce


class Filter:
    def __init__(self, queryset, filters, filter_exclude,
        fuzzy_fields, filter_type='__icontains'):
        self.qs = queryset
        self.filters = filters
        self.filter_exclude = filter_exclude
        self.fuzzy_fields = fuzzy_fields
        self.filter_type = filter_type

    def __call__(self):
        self.run_filter()
        return self.qs

    def run_filter(self):
        for filter_key, filter_value in self.filters.items():
            
            if not filter_value and not filter_value == False:
                continue

            if self.filter_exclude and filter_key in self.filter_exclude:
                continue

            elif filter_key == 'search':
                self.qs = FuzzyFilter(self.qs, filter_value, self.fuzzy_fields)()
                
            else:
                self.filter(filter_key, filter_value)

    def filter(self, filter_key, filter_value, filter_type=None):

        if isinstance(filter_value, bool):
            filter_by = filter_key

        elif '_id' in filter_key:
            # related_model = filter_key[:-3]
            # qs = qs.select_related(related_model)
            filter_by = filter_key
        else:
            filter_by = f'{filter_key}{self.filter_type}'
        
        self.qs = self.qs.filter(Q(**{filter_by : filter_value}))


class FuzzyFilter():
    def __init__(self, queryset, filter_value, 
        filter_fields, operator=operator.or_, filter_type='icontains'):
    
        self.qs = queryset
        self.operator = operator
        self.filter_type = filter_type
        self.filter_fields = filter_fields
        self.filter_value = filter_value

    def __call__(self):
        filter_list = self._get_filter_list()
        return self._concat_filter(filter_list)

    def _concat_filter(self, filter_list):
        filter_query = reduce(self.operator, filter_list)
        return self.qs.filter(filter_query)


    def _get_filter_list(self):
        filter_list = []
        for field in self.filter_fields:
            filter_by = f'{field}__{self.filter_type}'
            filter_list.append(Q(**{filter_by : self.filter_value}))

        return filter_list
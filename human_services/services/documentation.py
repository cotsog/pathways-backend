from coreapi import Field
from coreschema import Array, String
from rest_framework.schemas.inspectors import AutoSchema

def get_list_endpoint_fields():
    # TODO this is for list only, how to make it not appear on /services/{service_id}? The paginator know how...
    #       See AutoSchema#get_pagination_fields() which calls is_list_view()
    #       See also AutoSchema#get_filter_fields(), need to get _allows_filters() to return false on non-list views
    # TODO swagger UI creates invalid separator when giving >1 elements in argument arrays
    # TODO how to define results
    return AutoSchema(manual_fields=[
        Field(
            'search',
            location='query',
            schema=Array(
                items=String(),
                description='Search terms for full text search in all fields int the '
                            'service record and related location and organization records, '
                            'logical AND implied among terms',
            ),
        ),
        Field(
            'taxonomy_term',
            location='query',
            schema=String(
                pattern='\w+:\w+',
                description='Filter result on taxonomic terms, TODO make this take an array of '
                            'terms with implied logical AND among terms, TODO make this work '
                            'for hierarchical taxonomies',
            ),
        ),
        Field(
            'sort_by',
            location='query',
            schema=Array(
                items=String(),
                description='Sort resulting services by one or more fields, prefix field '
                            'name with - for descending sort order, records that sort equal '
                            'by the first field are sorted by the second field, etc.',
            ),
        ),
    ])

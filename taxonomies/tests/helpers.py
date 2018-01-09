from taxonomies import models

class TaxonomyTermBuilder:
    def __init__(self):
        self.taxonomy_id = 'default_taxonomy_id'
        self.name = 'default name'

    def with_taxonomy_id(self, taxonomy_id):
        self.taxonomy_id = taxonomy_id
        return self

    def with_name(self, name):
        self.name = name
        return self

    def build(self):
        result = models.TaxonomyTerm()
        result.taxonomy_id = self.taxonomy_id
        result.name = self.name
        return result
from django.db import models

class SimpleSearchableModel(models.Model):

    qi_simple_searchable_search_field = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if hasattr(self, search_fields):
            search_str = ""
            for f in self.search_fields:
                search_str += getattr(self,f)
            self.qi_simple_searchable_search_field = search_str
        else:
            self.qi_simple_searchable_search_field = self.__unicode__()

        super(SimpleSearchableModel,self).save(*args, **kwargs)
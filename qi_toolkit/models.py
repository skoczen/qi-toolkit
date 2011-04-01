from django.db import models
import re
import datetime

def resave_searchable_models():
    for model in models.get_models():
        if SimpleSearchableModel in model.__bases__:
            for o in model.objects.all():
                o.save()
    

class TimestampModelMixin(models.Model):
    created_at = models.DateTimeField(blank=True, null=True, editable=False)
    modified_at = models.DateTimeField(blank=True, null=True, editable=False)
    
    def save(self, *args, **kwargs):
        self.modified_at = datetime.datetime.now()
        if not self.id:
            self.created_at = datetime.datetime.now()
        super(TimestampModelMixin,self).save(*args, **kwargs)

    class Meta:
        abstract = True
            
class SimpleSearchableModel(models.Model):

    qi_simple_searchable_search_field = models.TextField(editable=False, blank=True, null=True, unique=False) # db_index=True

    def save(self, *args, **kwargs):
        if hasattr(self, "search_fields"):
            search_str = ""
            for f in self.search_fields:
                search_str += "%s " % getattr(self,f)
            self.qi_simple_searchable_search_field = search_str
        else:
            self.qi_simple_searchable_search_field = self.__unicode__()

        super(SimpleSearchableModel,self).save(*args, **kwargs)

    @classmethod
    def search(cls, query, delimiter=" ", ignorable_chars=None):
        # Accept a list of ignorable characters to strip from the query (dashes in phone numbers, etc)
        if ignorable_chars:
            ignorable_re = re.compile("[%s]+"%("".join(ignorable_chars)))
            query = ignorable_re.sub('',query)
        
        # Split the querystring by a given delimiter.
        if delimiter and delimiter != "":
            queries = query.split(delimiter)
        else:
            queries = [query]
        
        results = cls.objects.all()
        for q in queries:
            if q != "":
                results = results.filter(qi_simple_searchable_search_field__icontains=q)

        return results

    class Meta:
        abstract = True
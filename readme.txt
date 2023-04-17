Do not forget to activate Django virtual env for development
Cron job
Set other parameters to google e.g. time to check the traffic for, etc 
Batch calls to google
Two-way direction on roads
Stringing segments
Maps / images
Colour code
check that the endpoint of the previous segment isn't the start point of the current segment - to prevent double calls to the API

Getting this error might be as a result of dirty data e.g. a row with incomplete information:
...
route = Route.objects.get(route=json.dumps(obj.get("ROUTE")))
  File "/Users/alkadelik/Documents/dev/leyyow/djangoEnv/lib/python3.10/site-packages/django/db/models/manager.py", line 85, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/Users/alkadelik/Documents/dev/leyyow/djangoEnv/lib/python3.10/site-packages/django/db/models/query.py", line 496, in get
    raise self.model.DoesNotExist(
roads.models.Route.DoesNotExist: Route matching query does not exist.
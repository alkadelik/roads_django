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



MAP
Accurate search A1 v A123
Arrange alphabetically
upload
Edit
Search
Classification

Pagination
Filter segments by quality
Rounding issues
Autocomplete
Self upload
Cron ()
Edit
Map
Segments sharing a state
Inserting segment
Proper on-screen feedback and messaging (so you know when something is happening, etc)
Code refactoring (efficiency and refactoring)
Login so not anyone can upload / corrupt the data
The integrity of raw data. Sometimes even, google not finding the road
The order

show map of routes against Nigeria - so you understand the path that it is taking


Option 1: CPMS website

Documentation / FAQs

If there's an error uploading the segment, save it somewhere
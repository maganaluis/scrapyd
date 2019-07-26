### Forked Verion Notes

This forked version writes the job information to mongodb. In order to use it simply add
the mongo db connection information to you config file: 


```cfg
[scrapyd]
mongodb_name = scrapyd_mongodb
mongodb_host = 127.0.0.1
mongodb_port = 27017
mongodb_user = custom_user  # (Optional)
mongodb_pass = custompwd  # (Optional)
...
```

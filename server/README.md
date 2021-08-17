# The server of the Quick note

- Language：`Python3.7`
- Backend Framework：`Django2.2`
- Communication protocol：`HTTP`
- Database：`MySQL5.7`

# Something need to change

```
# core/settings.py
You should add your domain name or host address to ALLOWED_HOST and modify the configuration of database;
```

Then you should create a uwsgi file named "uwsgi.ini".
The configurations are as follows:

```ini
# uwsgi.ini file
[uwsgi]

# Django-related settings
# the base directory (full path)
chdir           = /home/admin/quick_note/server
# Django's wsgi file
wsgi-file       = core/wsgi.py

# process-related settings
# master
master          = true
# maximum number of worker processes
processes       = 2
threads         = 2
# the socket (use the full path to be safe
socket          = /home/admin/quick_note/server/quick_note.sock
# ... with appropriate permissions - may be needed
chmod-socket    = 666
# clear environment on exit
vacuum          = true
```

After the configuation file is created, you would run `uwsgi --ini uwsgi.ini` so as to run your backend server. The website needs running all the time, so we should type `nohup uwsgi --ini uwsgi.ini > nohup.out &` if we want it running automatically.

The configurations of the nginx are as follows:

```
http {
    
    # resolve the MIME type of the file automatically.
    include mime.types;
    default_type application/octet-stream;

    # the upstream component nginx needs to connect to
    upstream django {
        server unix:///home/admin/quick_note/server/quick_note.sock; # for a file socket
    }

    # configuration of the server
    server {
        # the port your site will be served on
        listen      80;
        root        /home/admin/quick_note/client/browser/dist/index.html;
        # the domain name it will serve for
        server_name 47.100.34.195; # substitute your machine's IP address or FQDN
        charset     utf-8;

        # max upload size
        client_max_body_size 75M;   # adjust to taste

        location /static {
            alias /home/admin/quick_note/client/browser/dist/static;
        }

        # Finally, send all non-media requests to the Django server.
        location / {
            uwsgi_pass  django;
            include     /usr/local/nginx/uwsgi_params; # the uwsgi_params file you installed
            try_files $uri $uri/ /index.html;
        }

        location /favicon.ico {
            root /home/admin/quick_note/client/browser/dist;
        }
    }

}
```

Finally, you would run `service nginx restart` to restart nginx.

**NOTICE**: Remember in mind that you should modify the **ALLOWED_HOSTS** in ***settings.py*** and the **password** of the database.

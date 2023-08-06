================
Django IP Guard
================

Django IP Guard (DIG) is a Django app to protect your django website from spammers, bots and bad peoples by their IP addresses. You can block specific ip addresses for specific urls or the entire site. You can allow only specific ip addresses for specific urls or the entire site.


Installation Guide
__________________

1. Add "django_ip_guard" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_ip_guard', # new
    ]

2. Include the `'django_ip_guard.middleware.DjangoIpGuardMiddleware'` URLconf in your project urls.py like this::

    MIDDLEWARE = [
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django_ip_guard.middleware.DjangoIpGuardMiddleware', # new
    ]

3. Add :code:`DIG_ENABLED = True` in your settings.py  
4. Add :code:`DIG_STORAGE = 'db'` in your settings.py if you want to use your database for storing Rules. If you want to use environment variables then add `DIG_STORAGE = 'env'`.
5. Now migrate database :code:`python manage.py migrate`.
6. If you want to detect users IP address  ::

    from django_ip_guard.utils import get_client_ip
    ...
    get_client_ip(request)
    ...
    
8. If you choose 'db' you don't need to add anymore variables in settings.py. 
   
   1. You need to login to admin panel and add **Dig Rules** (Only the first row is counted).  
   2. When you add **Dig rules** you can see **Blocker url patterns** and **Blocker ip patterns**. By using these two fields you can actually block some ip addresses to get access of certain page or the entire website. Common use cases: 
      
      1. Blocking bots from accessing entire site. 
      2. Blocking some ip address to access your contact form page etc.
   
   3. You can also see **Allower url patterns** and **Allower ip patterns**. By using these two fields you can actually allow certain ip addresses to get access of certain pages or the entire website. Common use cases:
      
      1. Allow only / Restrict few ip address to access your django admin panel.
   
   4. You may have multiple URLs or IPs in a single field. You just need to separate them with a new line.
   5. and each URL and IP or a line will support Regex (Regular expression)
   6. Example of blocker:  
        **Blocker url patterns**  ::
            
            ^/blog/  
            ^contact-us/$
        
        **Blocker ip patterns**  ::

            175.38.89.10[0-9] 
            98.981.98.98  
        
        So this will block mentioned ip addresses to access blog and contact page. For entire site add :code:`^/`
        
   7. example of blocker:  
        **Blocker url patterns**  ::
        
            ^admin/ 
        
        **Blocker ip patterns**  ::
        
            76.88.12.10[0-9]
        
        So this will only allow mentioned ip addresses to access admin panel. For entire site add :code:`^/`

9. If you choose 'env' then you don't need to add rules in database. You need to add more variables in settings.py::
    
    BLOCKER_URL_PATTERNS="^/blog/,^contact-us/$"
    BLOCKER_IP_PATTERNS="175.38.89.10[0-9],98.981.98.98"
    ALLOWER_URL_PATTERNS="^admin/"
    ALLOWER_IP_PATTERNS="76.88.12.10[0-9]"
    
You see the difference? Yes it's comma. If you don't want to use database you need to separate those URLs and IPs with commas. But in database you need to separate by new lines.

8. Finally we recommend you to use this app from env/settings file in production. Because database interaction might be a bit heavier. which can slower your website performance.


Requirements / Dependencies
___________________________
1. Python >=3.6, <4.0
2. Django >= 3.0, <4.0
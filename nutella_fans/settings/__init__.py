from nutella_fans.settings.base import *
# you need to set "myproject = 'prod'" as an environment variable
# in your OS (on which your website is hosted)
if os.getenv('NUTELLA_FANS') == 'production':
    from nutella_fans.settings.prod import *
else:
    from nutella_fans.settings.local import *

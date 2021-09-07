from .base import *
# you need to set "myproject = 'prod'" as an environment variable
# in your OS (on which your website is hosted)
if os.getenv('NUTELLA_FANS') == 'production':
    from .prod import *
else:
    from .local import *

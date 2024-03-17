import os
if os.environ.get("SERVER"):
    from constants.constant_prod import * # noqa 
else:
    from constants.constant_test import * # noqa

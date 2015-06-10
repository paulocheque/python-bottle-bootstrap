import json
import time

import bottle

import safe_bottle
import handlers
# import connect_mongo
# import connect_redis

if __name__ == "__main__":
    bottle.BaseRequest.MEMFILE_MAX = 1024 * 1 # in bytes

    import os
    server = os.getenv('SERVER', 'meinheld')
    port = int(os.environ.get('PORT', 8000))
    if server:
        bottle.run(host='0.0.0.0', port=port, server=server, debug=False)
    else:
        bottle.run(host='0.0.0.0', port=port, debug=False)

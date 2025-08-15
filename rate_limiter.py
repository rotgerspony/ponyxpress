
from flask import request, abort
import time

client_hits = {}

def limit_rate(max_per_minute=30):
    def decorator(fn):
        from functools import wraps
        @wraps(fn)
        def wrapped(*args, **kwargs):
            ip = request.remote_addr
            now = time.time()
            client_hits.setdefault(ip, []).append(now)
            hits = [t for t in client_hits[ip] if now - t < 60]
            client_hits[ip] = hits
            if len(hits) > max_per_minute:
                abort(429)
            return fn(*args, **kwargs)
        return wrapped
    return decorator

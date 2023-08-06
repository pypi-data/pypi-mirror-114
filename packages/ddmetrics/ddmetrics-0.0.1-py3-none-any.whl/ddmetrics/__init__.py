#!/usr/bin/env python
import logging
from functools import wraps

from datadog import initialize, api

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class DDMetrics(object):

    @classmethod
    def send(cls, api_key, app_key=None, statsd_host='127.0.0.1',
             statsd_port=8125):
        options = {
            'api_key': api_key,
            'app_key': app_key,
            'statsd_host': statsd_host,
            'statsd_port': statsd_port
        }

        initialize(**options)

        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                logger.info("started wrapper")
                return_value = f(*args, **kwargs)
                api.Metric.send(return_value)
                return return_value

            return wrapper

        return decorator

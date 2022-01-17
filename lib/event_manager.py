import threading
import time
import logging
from django.conf import settings


class EventManager:
    events = []
    threads = []


def attach(event_name):
    def decorator(f):
        def wrapper(*args, **kwargs):
            EventManager.events.append({
                'event_name': event_name,
                'callback': f,
                'args': args,
                'kwargs': kwargs
            })
        return wrapper
    return decorator


def trigger(event_name, threaded=True, max_threads=None):
    for event in EventManager.events:
        if event['event_name'] == event_name:
            try:
                if threaded:
                    t = threading.Thread(target=event['callback'], args=(event['args']), kwargs=(event['kwargs']))
                    EventManager.threads.append(t)
                else:
                    event['callback'](*event['args'], **event['kwargs'])
            except Exception as err:
                err_logger = logging.getLogger('error_mailer')
                err_logger.error('an error occured: {}'.format(err))

    for thread in EventManager.threads:
        start_thread(thread, max_threads)

    EventManager.threads = []


def start_thread(thread, max_threads=None):
    active_threads = threading.active_count()
    max_threads = max_threads if max_threads else settings.EVENT_MANAGER['semaphore']['max_threads']

    if active_threads >= max_threads:
        time.sleep(1)
        start_thread(thread, max_threads)

    else:
        thread.start()
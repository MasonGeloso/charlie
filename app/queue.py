from threading import Thread
from time import sleep
from traceback import format_exc

from tinyrecord import transaction
from tinydb import where

from .globals import LISTEN



QUEUE = list()




def queue_listener():
    def _queue_listener():
        print('Queue listening started..')
        while LISTEN:
            for queue in QUEUE:
                try:
                    obj = queue.get('obj')
                    table = obj.table
                    action = queue.get('action')

                    with transaction(table) as tr:
                        if action == 'remove':
                            tr.remove(where('identifier') == obj.identifier)

                        if action == 'insert':
                            tr.insert(obj.to_dict())

                        if queue.get('action') == 'update':
                            tr.update(
                                obj.to_dict(),
                                where('identifier') == obj.identifier
                            )

                    QUEUE.remove(queue)
                except:
                    print(format_exc())
                    pass


    Thread(target=_queue_listener).start()




def queue_up(obj, action: ['remove', 'insert', 'remove']):
    
    QUEUE.append({
        'obj': obj,
        'action': action,
        'table': obj.table
    })
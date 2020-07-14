import django_rq
queue = django_rq.get_queue('default')

def send_email(recipient, message):

    def send_email_task(recipient, message):
        print('%s: %s' % (recipient, message))

    queue.enqueue(send_email_task, recipient, message)

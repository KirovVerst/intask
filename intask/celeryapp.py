import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'intask.settings')

app = Celery('intask',
             broker='redis://localhost:6379/0',
             backend='rpc://',
             include=['users.tasks'])

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


if __name__ == '__main__':
    app.start()

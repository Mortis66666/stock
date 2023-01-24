from deta import app
from mongo import task

@app.lib.cron()
def cron_task(event):
    task()
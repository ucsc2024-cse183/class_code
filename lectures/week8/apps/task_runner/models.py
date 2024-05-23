"""
This file defines the database models
"""

from .common import db, Field, auth
from pydal.validators import *
import threading
import time
import sys


def task1(x):
    time.sleep(int(x))
    print("done!")
   
TASKS = {"task1": task1}   

db.define_table(
    "mytask",
    Field("name"),
    Field("task_info", "json"),  # <- {"function": "task1", "inputs": {"x": 1}}
#    auth.signature
)

def process_tasks():
    with open("task_runner.log", "w") as stream:
        while True:
            rows = db(db.mytask).select()
            stream.write(f"found {len(rows)} tasks\n")
            for row in rows:
                stream.write(row.name+"\n")
                task_info = row.task_info
                func_name = task_info["function"]
                inputs = task_info["inputs"]
                TASKS[func_name](**inputs)
                row.delete_record()
                db.commit()
                sys.stdout.flush()
            sys.stdout.flush()
            stream.flush()
            time.sleep(1)

thread = threading.Thread(target=process_tasks)
thread.start()

        


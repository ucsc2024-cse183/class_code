"""
This file defines the database models
"""

from .common import db, Field, auth
from pydal.validators import *
import multiprocessing
import time
import sys


# example of a task
# some task that is time consuming here simply add 1 to x
def task1(x):
    time.sleep(int(x))
    print("done!")
    return x+1
   
# register tasks (only one for now)
TASKS = {"task1": task1}   

# table where to store task queue
db.define_table(
    "mytask",
    Field("name"),  # name given by user
    Field("task"),  # from TASKS
    Field("input", "json"),  # the input, for example {"x": 1}
    Field("output", "json"), # the output to be stored after execution
    Field("status", default="queued"), # change to success or failed
    Field("created_by", "reference auth_user"),
)

# function that will process tasks in background
def process_tasks():
    with open("task_runner.log", "w") as stream:
        # redirect output to file
        sys.stdout = stream
        sys.stderr = stream
        while True:
            rows = db(db.mytask.status=="queued").select()
            for row in rows:
                print("processing", row.name)                
                try:
                    output = {"output": TASKS[row.task](**row.input)}
                    row.update_record(output=output, status="success")
                    print("task completed!")
                except Exception:
                    print(traceback.format_exc())
                    output = {"error": traceback.format_exc()}
                    row.update_record(output=output, status="failed")
                    print("task failed!")
                db.commit()
                stream.flush()
            time.sleep(1)

# run tasks in background process or thread
process = multiprocessing.Process(target=process_tasks)
process.start()

        


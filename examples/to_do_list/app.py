import photongui
from photongui import Util

import os


util = Util()
util.exposeAll("ToDoList", locals())

indexFile = os.path.join(os.path.dirname(__file__), "view/index.html")
print(indexFile)

settings = {
    "view":indexFile
}

window = photongui.createWindow(settings)

ToDos = []

def add(todo):
    task = todo
    status = "added"

    final = {"task": task, "status":status}
    ToDos.append(final)
    print("one item is added: ", final)
    print("All Tasks: ", ToDos)

def delete(todo):
    for idx, item in enumerate(ToDos):
        if item["task"] == todo:
            del ToDos[idx]
    print("one item is deleted: ", todo)
    print("All Tasks: ", ToDos)

def edit(oldTodo, newTodo):
    for item in ToDos:
        if item["task"] == oldTodo:
            item["task"] = newTodo
            item["status"] = "updated"
            print("one task is updated: ", item, " The new update is: ", newTodo)
            print("All Tasks: ", ToDos)

def deleteAll():
    ToDos.clear()
    print("all items have been deleted")
    print("All Tasks: ", ToDos)


photongui.start(debug=True)
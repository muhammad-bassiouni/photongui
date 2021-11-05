import photongui
import csv
import pandas as pd
import os


util = photongui.Util()
util.exposeAll("database", locals())


index = os.path.join(os.path.dirname(__file__), "view/index.html")

settings = {
    "title" : "Database",
    "view" : index,
}

fields = ["Name", "Email"]

with open("./database.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(fields)

def add(name, email):
    df = pd.read_csv("./database.csv")
    if name in df["Name"].values or email in df["Email"].values:
        return 0
    
    with open("database.csv", "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([name, email])
        return 1

main = photongui.createWindow(settings)

photongui.start(debug=True)

os.remove("database.csv")
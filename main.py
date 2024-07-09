from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

def time_to_int(time_string):
    ret = 0
    splitted = time_string.split(":")
    if (len(splitted) == 2):
        ret += int(splitted[0]) * 60
        ret += int(splitted[1])
    else:
        ret += int(splitted[0]) * 3600
        ret += int(splitted[1]) * 60
        ret += int(splitted[2])
    return ret


def int_to_time(time):
    hours = int(time / 3600)
    mins = int((time % 3600) / 60)
    secs = int((time % 3600) % 60)
    if mins < 10:
        str_mins = "0" + str(mins)
    else:
        str_mins = str(mins)
    if secs < 10:
        str_secs = "0" + str(secs)
    else:
        str_secs = str(secs)
    if (hours > 0):
        return str(hours) + ":" + str_mins + ":" + str_secs
    else:
        return str_mins + ":" + str_secs


def get_data(name):
    url = "https://www.parkrun.com.au/" + name + "/results/latestresults/"
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0"}

    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, "lxml")

    results = soup.find_all("tr", attrs={"class":"Results-table-row"})
    results_processed = []

    for item in results:
        if (item["data-name"] != "Unknown" and item["data-agegrade"] != ""):
            row = []
            row.append(item["data-name"])
            row.append(item["data-gender"])
            row.append(item["data-agegroup"])
            row.append(float(item["data-agegrade"]))
            row.append(item.contents[5].contents[0].string)
            row.append(time_to_int(item.contents[5].contents[0].string))
            results_processed.append(row)

    df = pd.DataFrame(results_processed, columns=["name", "gender", "agegroup", "agegrade", "time", "timeprocessed"])
    
    return df


def get_summary_labels(data):
    global summary_stringvar
    summary = ["mean", "min", "25%", "50%", "75%", "max"]
    summary_stringvar[0].set("count: " + str(int(data["timeprocessed"].describe()["count"])))
    for count, item in enumerate(summary):
        summary_stringvar[count + 1].set(item + ": " + int_to_time(data["timeprocessed"].describe()[item]))


def get_graphs(data):
    figure = plt.figure()
    figure.add_subplot(211).hist(data["timeprocessed"])
    figure.add_subplot(212).boxplot(data["timeprocessed"], vert=False)
    chart = FigureCanvasTkAgg(figure, master=root)
    chart.draw()
    chart.get_tk_widget().grid(row=1, column=0, columnspan=7)


def update_restrictions(filter):
    if filter == "All":
        get_graphs(data)
        get_summary_labels(data)
    elif filter == "Male Only":
        get_graphs(data[data["gender"] == "Male"])
        get_summary_labels(data[data["gender"] == "Male"])
    elif filter == "Female Only":
        get_graphs(data[data["gender"] == "Female"])
        get_summary_labels(data[data["gender"] == "Female"])


def update_location_data(name, restrictions):
    global data
    data = get_data(name)
    update_restrictions(restrictions)


data = get_data("albertmelbourne")

root = tk.Tk()
root.title("Parkrun Utils")

# make all columns same width
root.columnconfigure(0, weight=1, uniform="a")
root.columnconfigure(1, weight=1, uniform="a")
root.columnconfigure(2, weight=1, uniform="a")
root.columnconfigure(3, weight=1, uniform="a")
root.columnconfigure(4, weight=1, uniform="a")
root.columnconfigure(5, weight=1, uniform="a")
root.columnconfigure(6, weight=1, uniform="a")

# location selector
locations = pd.read_csv("locations.csv", header=None)[0].tolist()
currloc = tk.StringVar()
currloc.set(locations[1])
pick = ttk.Combobox(root, textvariable=currloc, values=locations, width=35)
pick.grid(row=0, column=0, columnspan=3)

upd = ttk.Button(root, text="Get Data" , command=lambda: update_location_data(currloc.get(), filterstring.get()))
upd.grid(row=0, column=3)

# options
filterstring = tk.StringVar()
filterstring.set("All")
filter = ttk.Combobox(root, textvariable=filterstring, values=["All", "Male Only", "Female Only"])
filter.grid(row=0, column=4, columnspan=2)

upd_filter = ttk.Button(root, text="Update Filters", command=lambda: update_restrictions(filterstring.get()))
upd_filter.grid(row=0, column=6)

# graphs
get_graphs(data)

# summary statistics
summary = ["mean", "min", "25%", "50%", "75%", "max"]
summary_stringvar = []
summary_labels = []
summary_stringvar.append(tk.StringVar())
summary_stringvar[0].set("count: " + str(int(data["timeprocessed"].describe()["count"])))
summary_labels.append(ttk.Label(root, textvariable=summary_stringvar[0]))
for count, item in enumerate(summary):
    summary_stringvar.append(tk.StringVar())
    summary_stringvar[count + 1].set(item + ": " + int_to_time(data["timeprocessed"].describe()[item]))
    summary_labels.append(ttk.Label(root, textvariable=summary_stringvar[count + 1]))
for count, object in enumerate(summary_labels):
    object.grid(row=2, column=count)

root.mainloop()

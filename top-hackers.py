import requests
import matplotlib.pyplot as plt
import numpy as np

names = []
scores = []

r = requests.get("https://sheetdb.io/api/v1/fmpuahqe0npeq?sheet=hackers")

for data in r.json():
    names.append(data["display name"])
    scores.append(int(data["sum"]))

x = np.array(names)
y = np.array(scores)


plt.barh(y, x)
plt.show()
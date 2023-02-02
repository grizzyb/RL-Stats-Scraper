from bs4 import BeautifulSoup as soup
import requests
import regex as re
import tkinter as tk
from tkinter import Label, Button, Entry, Tk


def scrape_data():
    # Regex to put username into URL from input 
    url = "https://rocket-league.com/player/" + username_entry.get() + "/stats"
    results = requests.get(url)
    doc = soup(results.text, "html.parser")

    # This pulls Gamemode Names into gamemodelist[0-7]
    gamemode = doc.find_all("h2", {"class": "rlg-statsrank__title --new"})
    gamemodelist = [g.text for g in gamemode]
    gamemodelist = gamemodelist[0:8]

    # This pulls the Gamemode Ranks into gameranklist[0-7]
    gamerank = doc.find_all("div", {"class": "rlg-text rlg-statsrank__tier"})
    gameranklist = [r.text.strip() for r in gamerank]
    gameranklist = gameranklist[0:7]

    # Append "Not Ranked" into gameranklist[0] to align game mode/rank variables to account for Casual
    casualrank = "Not Ranked"
    gameranklist.insert(0, casualrank)

    # Extract gamemode metadata
    gamemodedata = doc.find_all("div", {"class": "rlg-statsrank__meta"})
    gamemodedatalist = [d.text.strip() for d in gamemodedata]
    # Regex to remove all the \n spam in the index strings
    gamemodedatalist = [re.sub(r'\n+', ' ', x) for x in gamemodedatalist]
    gamemodedatalist = gamemodedatalist[0:8]

    # Pulling player's main stats
    playerstats = doc.find_all("div", {"class": "rlg-stats"})
    playerstatslist = [d.text.strip() for d in playerstats]
    playerstatslist = [re.sub(r'\n+', ' ', x) for x in playerstatslist]

    # Display the data on the GUI
    data_label.config(text="")
    counter = 0
    while counter != 8:
        data_label.config(text=data_label.cget("text") + gamemodelist[counter] + "\n" + gameranklist[counter] + "\n" + gamemodedatalist[counter] + "\n\n")
        counter = counter + 1

# Create the GUI window
root = tk.Tk()
root.title("Rocket League Stats Scraper")

# Create the username label and entry
username_label = Label(root, text="Enter your Rocket League username: ")
username_entry = Entry(root, width=30)
username_label.grid(row=0, column=0, padx=10, pady=10)
username_entry.grid(row=0, column=1, padx=10, pady=10)

# Create the "Get Stats" button
get_stats_button = Button(root, text="Get Stats", command=scrape_data)
get_stats_button.grid(row=1, column=1, pady=10)

# Create the label to display the data
data_label = Label(root, text="")
data_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Run the GUI
root.mainloop()

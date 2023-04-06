import tkinter as tk
import os
import requests

class MainWindow(tk.Tk):
    # initial window size
    def __init__(self):
        super().__init__()
        self.title("Main Window")
        self.geometry("300x200") 
        
        # Main 4 buttons 
        self.button1 = tk.Button(self, text=" Search for Anime and Tvshows ", command=self.search_anime_tv)
        self.button1.pack()
        
        self.button2 = tk.Button(self, text=" Save listings                                 ", command=self.open_page2)
        self.button2.pack()
        
        self.button3 = tk.Button(self, text=" Plan to watch                               ", command=self.open_page3)
        self.button3.pack()
        
        self.notes_button = tk.Button(self, text=" Notes app                                     ", command=self.open_notes)
        self.notes_button.pack()
        
    #resize the window to fit both of the searches
    def search_anime_tv(self):
        self.geometry("1500x500") 
# ------------------------------------------------------------------
# Anime search :)
# ------------------------------------------------------------------

        # frame for anime search widgets
        anime_search_frame = tk.Frame(self)
        anime_search_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # label for anime search
        anime_instructions_label = tk.Label(anime_search_frame, text="Enter an anime name:", font=("Arial", 16))
        anime_instructions_label.pack()

        # entry field 
        anime_entry = tk.Entry(anime_search_frame, font=("Arial", 14))
        anime_entry.pack(pady=5)

        # search button 
        anime_search_button = tk.Button(anime_search_frame, text="Search", font=("Arial", 14))
        anime_search_button.pack(pady=5)

        # text widget that displays the anime results
        anime_results_text = tk.Text(anime_search_frame, font=("Arial", 12))
        anime_results_text.pack(pady=5)

        # function that will be done when the user clicks the anime search button
        def search_for_anime():
            # Get the anime 
            anime_name = anime_entry.get()

            # Use the requests library 
            response = requests.get(f"https://api.jikan.moe/v4/anime?q={anime_name}")
            data = response.json().get("data")

            # Create a list of dictionaries containing the id, name, and description of each anime
            anime_list = [{"id": n["mal_id"],"name": n["title"], "desc": n["synopsis"]} for n in data]

            # Clear the results text widget
            anime_results_text.delete('1.0', tk.END)

            # Loop through each anime in the list and add its information to the text widget
            for n in anime_list:
                anime_id = n["id"]
                anime_name = n["name"]
                anime_desc = n["desc"]
                anime_results_text.insert(tk.END, f"Name: {anime_name}\nMyAnimeList ID: {anime_id}\nDescription: {anime_desc}\n\n")
        
        anime_search_button["command"] = search_for_anime

# ------------------------------------------------------------------
# TV show search :)
# ------------------------------------------------------------------

        # frame
        show_frame = tk.Frame(self)
        show_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # label
        show_instructions_label = tk.Label(show_frame, text="Enter a TV show name:", font=("Arial", 16))
        show_instructions_label.pack()

        # entry
        show_entry = tk.Entry(show_frame, font=("Arial", 14))
        show_entry.pack(pady=5)

        # search button
        show_search_button = tk.Button(show_frame, text="Search", font=("Arial", 14))
        show_search_button.pack(pady=5)

        # Text widget to show the name and summary of the TV shows
        show_info_text = tk.Text(show_frame, font=("Arial", 12), wrap=tk.WORD)
        show_info_text.pack(pady=5)

        # Scrollbar for the Text widget
        scrollbar = tk.Scrollbar(show_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the Text widget and the Scrollbar
        show_info_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=show_info_text.yview)

        # install beautifulsoup4
        from bs4 import BeautifulSoup
        
        # function to get the TV show info
        def get_show_info(query):
            # request to the API
            r = requests.get(f"http://api.tvmaze.com/search/shows?q={query}")

            # successful
            if r.status_code == 200:
                # results from the search
                results = r.json()

                # If the results list is not empty
                if results:
                    show_names = []
                    show_summaries = []
                    # loop through all the results
                    for result in results:
                        # name and summary of the TV show
                        name = result['show']['name']
                        summary = result['show']['summary']
                        if summary is not None:
                            soup = BeautifulSoup(summary, "html.parser")
                            summary = soup.get_text()
                        else:
                            summary = "No summary available for this show"
                        # Append the name and summary
                        show_names.append(name)
                        show_summaries.append(summary)



                    # Return the names and summaries as tuple
                    return show_names, show_summaries
                else:
                    # return an error message
                    return "No TV show found with that name"
            else:
                # not successful, return an error message
                return "Error retrieving TV show information"


        # when the user clicks the TV show search button
        def show_search():
            # Clear the Text widget
            show_info_text.delete(1.0, tk.END)

            # TV show name from the entry field
            show_name = show_entry.get()

            # Get the TV show information
            show_info = get_show_info(show_name)

            # If the show info is a tuple (name and summary)
            if isinstance(show_info, tuple):
                names = show_info[0]
                summaries = show_info[1]
                #loop through all the names and summaries
                for name, summary in zip(names, summaries):
                    # Display the name and summary in the Text widget
                    show_info_text.insert(tk.END, f"{name}\n\n{summary}\n\n")
            else:
                # Display the error message in the Text widget
                show_info_text.insert(tk.END, show_info)
        # Tell the show search button to call the show_search function when its clicked
        show_search_button["command"] = show_search
    
# ------------------------------------------------------------------
# Name and rating :)
# ------------------------------------------------------------------

    def open_page2(self):
            # entry fields
            def submit():
                name = entry1.get()
                rating = entry2.get()
                names_list.insert(tk.END, name)
                ratings_list.insert(tk.END, rating)
                with open("names_ratings.txt", "a") as f:
                    f.write(name + "," + rating + "\n")
            # the clear button which edits the text file when something is cleared
            def clear_lists():
                selected_indices = list(names_list.curselection())
                selected_indices.reverse()
                temp_list = []
                with open("names_ratings.txt", "r") as f:
                    for line in f:
                        temp_list.append(line)
                with open("names_ratings.txt", "w") as f:
                    for i in range(len(temp_list)):
                        if i not in selected_indices:
                            f.write(temp_list[i])
                for index in selected_indices:
                    names_list.delete(index)
                    ratings_list.delete(index)


            #tkinter GUI lables, entry fields and lists
            root = tk.Tk()
            root.title("Name and Rating")

            label1 = tk.Label(root, text="Name:")
            label1.grid(row=0, column=0)

            entry1 = tk.Entry(root)
            entry1.grid(row=0, column=1)

            label2 = tk.Label(root, text="Rating (1-10):")
            label2.grid(row=1, column=0)

            entry2 = tk.Entry(root)
            entry2.grid(row=1, column=1)


            names_list = tk.Listbox(root)
            names_list.grid(row=3, column=0, padx=10, pady=10)

            ratings_list = tk.Listbox(root)
            ratings_list.grid(row=3, column=1, padx=10, pady=10)

            submit_button = tk.Button(root, text="Submit", command=submit)
            submit_button.grid(row=2, column=0, columnspan=2, pady=10)

            clear_button = tk.Button(root, text="Clear", command=clear_lists)
            clear_button.grid(row=4, column=0, columnspan=2, pady=10)

            try:
                with open("names_ratings.txt") as f:
                    for line in f:
                        name, rating = line.strip().split(",")
                        names_list.insert(tk.END, name)
                        ratings_list.insert(tk.END, rating)
            except:
                pass

            root.mainloop()
# ------------------------------------------------------------------
# Plan to watch :)
# ------------------------------------------------------------------

    def open_page3(self):
        def submit():
                # entry fields
                name = entry1.get()
                names_list.insert(tk.END, name)
                with open("names.txt", "a") as f:
                    f.write(name + "\n")
        # the clear button which edits the text file when something is cleared
        def clear_lists():
                selected_indices = list(names_list.curselection())
                selected_indices.reverse()
                temp_list = []
                with open("names.txt", "r") as f:
                    for line in f:
                        temp_list.append(line)
                with open("names.txt", "w") as f:
                    for i in range(len(temp_list)):
                        if i not in selected_indices:
                            f.write(temp_list[i])
                for index in selected_indices:
                    names_list.delete(index)
        
        #tkinter GUI lables, entry fields and list
        root = tk.Tk()
        root.title("Name")

        label1 = tk.Label(root, text="Name:")
        label1.grid(row=0, column=0)

        entry1 = tk.Entry(root)
        entry1.grid(row=0, column=1)

        names_list = tk.Listbox(root)
        names_list.grid(row=3, column=0, padx=10, pady=10)

        submit_button = tk.Button(root, text="Submit", command=submit)
        submit_button.grid(row=2, column=0, columnspan=2, pady=10)

        clear_button = tk.Button(root, text="Clear", command=clear_lists)
        clear_button.grid(row=4, column=0, columnspan=2, pady=10)

        try:
            with open("names.txt") as f:
                for line in f:
                    name = line.strip()
                    names_list.insert(tk.END, name)
        except:
            pass

        root.mainloop()

# ------------------------------------------------------------------
# Notes :)
# ------------------------------------------------------------------

    def open_notes(self):
        notes_app = NotesApp(self)

class NotesApp(tk.Toplevel):
    # notes app display
    def __init__(self, master):
        super().__init__(master)
        self.title("Notes App")
        self.geometry("500x600")
        
        #text widget to show notes
        self.notes_text = tk.Text(self, font=("TkDefaultFont", 14))
        self.notes_text.pack(fill="both", expand=True)
        
        #button to save notes
        self.save_button = tk.Button(self, text="Save Notes", command=self.save_notes)
        self.save_button.pack()

        # Check if a previous version of the notes is there
        if os.path.exists("notes.txt"):
            with open("notes.txt", "r") as f:
                notes = f.read()
                self.notes_text.insert("1.0", notes)

    def save_notes(self):
        with open("notes.txt", "w") as f:
            notes = self.notes_text.get("1.0", "end")
            f.write(notes)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()

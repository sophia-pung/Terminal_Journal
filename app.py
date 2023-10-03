import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6 import uic
from PyQt6.QtCore import QDateTime, QTimer

import sys

app = QApplication(sys.argv)

# Get the directory of the script (where this code is located)
script_directory = os.path.dirname(os.path.abspath(__file__))

# Define the directory for journal entries relative to the script's location
journal_entries_directory = os.path.join(script_directory, "journal_entries")

# Define the relative path to the 'journal.ui' file relative to the script's location
ui_file_path = os.path.join(script_directory, "resources", "journal.ui")

class JournalWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        uic.loadUi(ui_file_path, self)  # Load the UI file

        # Initialize QTimer for updating current date and time
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateCurrentDateTime)
        self.timerStarted = False

        # Initialize a counter for journal entries
        self.entry_counter = self.findHighestJournalEntryNumber() + 1
        
        # # Print the timestamp information (may be empty at this point)
        # print('timestamp in __init__:', self.loadLastJournalEntry())

        # Connect the submit button to a slot
        self.submitButton.clicked.connect(self.submitJournalEntry)

        # Set the background color of the QTextEdit widget to black
        self.journalText.setStyleSheet("background-color: black; color: white;")  # Set background to black, text to white

        # Load the last journal entry
        self.loadLastJournalEntry()

    def submitJournalEntry(self):
        # Here you can add the logic for submitting the journal entry
        # Get the text from QTextEdit widget, 'journalText'
        entry_text = self.journalText.toPlainText()
        print("Journal Entry:", entry_text)

        # Save the entry to an MD file
        self.saveToMDFile(entry_text)

        # Clear the text in the QTextEdit widget
        self.journalText.clear()

        # Create the journal_entries_directory if it doesn't exist
        # os.makedirs(journal_entries_directory, exist_ok=True)

        # Load the last journal entry
        self.loadLastJournalEntry()

    def findHighestJournalEntryNumber(self):
        # Search for journal entry files in the journal_entries_directory
        print('journal entries directory', journal_entries_directory)
        journal_files = [filename for filename in os.listdir(journal_entries_directory) if filename.startswith("journal_entry_")]

        if journal_files:
            # Extract the entry numbers from the filenames and find the highest one
            entry_numbers = [int(filename.split("_")[2].split(".")[0]) for filename in journal_files]
            return max(entry_numbers)
        else:
            return 0  # No journal entries found

    def loadLastJournalEntry(self):
        # Load the most recent journal entry if available
        highest_entry_number = self.findHighestJournalEntryNumber()

        if highest_entry_number > 0:
            filename = os.path.join(journal_entries_directory, f"journal_entry_{highest_entry_number}.md")
            with open(filename, "r", encoding="utf-8") as file:
                content = file.read()
                # Extract timestamp and text from the loaded file
                timestamp, text = content.split("\n\n", 1)
                print('timestamp22', timestamp)
                # Convert the timestamp string to QDateTime
                timestamp_datetime = QDateTime.fromString(timestamp, "ddd MMM dd hh:mm:ss")
                # Display the timestamp and text
                # self.lastEntryDateTime.setDateTime(timestamp_datetime)
                # self.journalText.setPlainText(text)

                # Update the "Last Entry" label with the loaded timestamp
                self.lastEntryLabel.setText(f"Last Entry: {timestamp}")

    def saveToMDFile(self, text):
        # Generate a filename with an incremented entry number
        # Get the directory of the main.py script
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # Define the relative path to the "journal_entries" directory
        journal_entries_directory = os.path.join(script_directory, "journal_entries")

        # Ensure the "journal_entries" directory exists, create it if necessary
        os.makedirs(journal_entries_directory, exist_ok=True)

        # Define the relative path to the journal entry file
        file_name = os.path.join(journal_entries_directory, f"journal_entry_{self.entry_counter}.md")

        print('file_name that entry was saved to', file_name)

        timestamp = QDateTime.currentDateTime().toString("ddd MMM dd hh:mm:ss")

        try:
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(f"{timestamp}\n\n")
                file.write(text)
            print(f"Saved to {file_name}")
        except Exception as e:
            print(f"Error saving file: {e}")

        # Increment the entry counter for the next entry
        self.entry_counter += 1

    def updateCurrentDateTime(self):
        # Update the current date and time every second
        self.currentDateTime.setDateTime(QDateTime.currentDateTime())

    def startTimer(self):
        # Start the timer when the window is shown
        if not self.timerStarted:
            self.timerStarted = True
            self.timer.start(1000)

# Create an instance of the JournalWindow class
window = JournalWindow()

# Start the timer to update the current date and time
window.startTimer()

window.show()
app.exec()

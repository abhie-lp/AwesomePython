import os
from sys import argv, exit
import re


class WordChecker():

    def __init__(self):             # Start building the dictionary on calling of the program
        self.word_count = 0
        self.count = 0              # Count of misspelled words
        self.dictionary = {}        # Initialising the empty dictionary
        current = os.getcwd()       # Storing the current working to get back to this directory after building dictionary
        os.chdir(os.path.join(os.getcwd(), "Dictionary"))       # Changing the directory to dictionary folder where all the words are stored
        for file in os.listdir(os.getcwd()):                    # Getting the list of all the files in the directory
            self.dictionary[file] = set()                       # Building an empty set with the name of file
            with open(file) as f:                               # Opeing the file
                for word in f:                                  # Reading all the words in the file
                    self.dictionary[file].add(word.rstrip())    # Storing all the starting with the file name in the same set
        os.chdir(current)           # Returning back to the original working directory
        print(os.getcwd())
    
    def check(self, file):
        with open(file) as f:       # Open the text file to check
            with open("mispelled.txt", "w") as m:               # Open the file to store the details of mispelled words
                for line_no, line in enumerate(f):              # looping over every line in file with its line number
                    words = re.findall(r"[a-zA-Z]+'?[a-zA-Z]*", line)           # Regular expression to find the words
                    self.word_count += len(words)                               # Adding the length of the words list to total number of words in file
                    for word_no, word in enumerate(words):                      # Looping over every word in words list with its index
                        if word.lower() not in self.dictionary[word[0].lower()]:                # Checking if word is not in dictionary
                            m.write(f"Line  {line_no+1} word {word_no+1} == {word}\n")          # Writing the line number, word number and wrong word to file 
                            self.count += 1                                                     # Increasing the count of mispelled words

                m.write(f"\n\nNo of misspelled word == {self.count}\n")
                m.write(f"No of words in file == {self.word_count}")


    


if __name__ == "__main__":
    if len(argv) < 2:                       # Checking the length of command line arguments
        exit("Give correct inputs")         # Exit the program of condition true

    ch = WordChecker()
    ch.check(argv[1])

import tkinter.filedialog
import csv

def openfile():
   filename = tkinter.filedialog.askopenfile(mode='r')
   return filename.name

def readCSV(fileName):
    listName = []
    with open(fileName, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting each data row one by one
        for row in csvreader:
            listName.append(row)
    return listName

def importDeck():
    return readCSV(openfile())

def main():
    print(importDeck())

main()

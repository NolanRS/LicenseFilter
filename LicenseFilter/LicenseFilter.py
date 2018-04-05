import csv
import re
from tkinter import *
from tkinter import filedialog

sccmFile = ''
adobeFile = ''

def checkAdmin(username):
    m = re.match('^[A-a]dmin.*$|^[S-s]ystem.*$', username)
    return m


# checks to see if the email from Adobe.com matches the username from SCCM

# because of the formatting difference between the Adobe.com csv and the csv file from SCCM
# there is a need to strip the username from the email which is done and checked
def checkEmail(email, username):
    m = re.search('(^[^@]+)', email)
    if m:
        found = m.group(1)
        return found == username
    else:
        return False


# checks current entry to see if it is a single license user
def checkSingle(row, currentList):
    username = row[1].lower()
    if (checkAdmin(username)):
        return False
    computername = row[0]
    lastLicenseEntry = currentList[-1]

    contains = True

    for line in currentList:
        checkComp = line[0]
        checkName = line[1]
        if 'Adobe' in checkComp:
            if checkName == username:
                contains = False
        elif checkComp == username and checkName == computername:
            contains = False

    return contains


# checks current entry to see if it is a serializable license
def checkMulti(row, currentList):
    username = row[1].lower()
    computername = row[0]
    lastLicenseEntry = currentList[-1]

    if lastLicenseEntry[0] == computername and lastLicenseEntry[1] != username:
        return True
    else:
        return False


# removes duplicate entries from lists before writing to file
def removeDuplicates(duplicate):
    final_list = []
    for name in duplicate:
        if name not in final_list:
            final_list.append(name)
    return final_list


def tableProcessing(inFile):
    with open(inFile, 'r', newline='') as full_table:
        fullReader = csv.reader(full_table, delimiter=',')

        full_list = list(fullReader)

        writeToList = csvToList(full_list)

        single_list = writeToList[0]
        serializable = writeToList[1]

        return (single_list, serializable)


# compares two tables to filter out lab machines from single user machines
# requires the current list of users with single licenses from the Adobe site to function properly
def compareSingleLicenses(currentUsers, dataUsers, multiUsers):
    singleCompared = []
    currently_licensed = currentUsers
    stored_licensed = dataUsers
    serializedUsers = multiUsers

    # loop through a list with users currently under a single license
    for element in currently_licensed:
        email = element[1]
        # loop through the list of unlicensed users according to sccm
        for entry in stored_licensed:
            username = entry[1]
            if (checkEmail(email, username) == False):
                singleCompared.append(entry)
            else:
                break

    mergedSingleWriter(singleCompared, serializedUsers)


# checks for single use and serialized machines
# currently must not contain column headers to function properly
def csvToList(inFile):
    shortHandList = []
    single = []
    multi = []
    for row in inFile:
        shortHandList.append([row[0]] + [row[1]])

    shortHandList = removeDuplicates(shortHandList)
    for index, line in enumerate(shortHandList):
        if (index == len(shortHandList) - 1):
            break
        print(line)
        elToCheck = shortHandList[index + 1]
        if(checkAdmin(line[1])):
            continue
        if elToCheck != line:
            if elToCheck[0] == line[0] and elToCheck[1] != line[1]:
                if line[0] not in multi:
                    multi.append(line[0])
            else:
                if line[0] not in multi:
                    single.append(line)

    return (single, multi)


# accepts two lists and creates a merged copy of the two
# used for taking a list of users that need a single license and a list with serializable licenses
# writes the merging of the two files to a single list.
def mergedSingleWriter(singleCSV, multiCSV):
    with open('MergedLicenses.csv', 'w', newline='') as file:
        singleWriter = csv.writer(file, delimiter=',', escapechar='')

        singleWriter.writerow(["Single Use Licenses"])
        singleWriter.writerow(["Number of Single User Licenses:" + str(len(singleCSV))])
        for line in singleCSV:
            singleWriter.writerow(line)
        singleWriter.writerow('')
        singleWriter.writerow(["Serializable Licenses"])
        singleWriter.writerow(["Number of Serializable Licenses:" + str(len(multiCSV))])
        for line in multiCSV:
            singleWriter.writerow([line])

def selectSccmFile():
    ftypes = [("CSV files", '*.csv')]
    global sccmFile
    sccmFile = filedialog.askopenfilename(initialdir = '/',title="Select file", filetypes = ftypes)
    sccmEntry.delete(0, END)
    sccmEntry.insert(0, sccmFile)

def selectAdobeFile():
    ftypes = [("CSV files", '*.csv')]
    global adobeFile
    adobeFile = filedialog.askopenfilename(initialdir = '/',title="Select file", filetypes = ftypes)
    adobeEntry.delete(0, END)
    adobeEntry.insert(0, adobeFile)

def run():
    licensed = tableProcessing(adobeFile)
    notLicensed = tableProcessing(sccmFile)

    compareSingleLicenses(licensed[0], notLicensed[0], notLicensed[1])

root = Tk()

root.title('License Filter')
root.configure(background='white')
root.minsize(width=650, height=150)
root.maxsize(width=650, height=150)
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
size = tuple(int(pos) for pos in root.geometry().split('+')[0].split('x'))
x = w/2 - size[0]/2
y = h/2 - size[1]/2
root.geometry("%dx%d+%d+%d" % (size + (x, y)))

sccmLabel = Label(root, text = "SCCM List",bg="white")
adobeLabel = Label(root, text = "Adobe List",bg="white")

sccmButton = Button(root,text='SCCM License File',width=20,command=selectSccmFile)
adobeButton = Button(root,text='Adobe License File',width=20,command=selectAdobeFile)
runButton = Button(root,text='Run',width=20,bg='red',command=run)

sccmEntry = Entry(root,width=65,textvariable=sccmFile)
adobeEntry = Entry(root,width=65,textvariable=adobeFile)

sccmLabel.grid(row=0)
adobeLabel.grid(row=1)

adobeButton.grid(row=1,column=1,padx=(10,10))
sccmButton.grid(row=0,column=1)
runButton.place(relx=0.5, rely=0.6, anchor=CENTER)

sccmEntry.grid(row=0,column=2)
adobeEntry.grid(row=1,column=2)


root.mainloop()


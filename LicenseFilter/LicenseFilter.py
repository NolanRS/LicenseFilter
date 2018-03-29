import csv
import re
import cProfile


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
def filterSingle(row, currentList):
    username = row[1].lower()
    if (checkAdmin(username)):
        return False
    computername = row[0]
    lastLicenseEntry = currentList[-1]

    if lastLicenseEntry[1] == username and lastLicenseEntry[0] == computername:
        return True
    else:
        return False


# checks current entry to see if it is a serializable license
def filterMulti(row, currentList):
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

    #loop through a list with users currently under a single license
    for element in currently_licensed:
        email = element[1]
        #loop through the list of unlicensed users according to sccm
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
    single_list = []
    multi_list = []
    #loops through the file/list
    for row in inFile:
        #checks to make sure that any entries with an empty computer name field are skipped
        if (row[0] != ''):
            if len(single_list) == 0:
                single_list.insert(0, [row[0]]+[row[1]])
                multi_list.insert(0, [row[0]])
                continue

            #check to see if the user being checked has already been added
            isSingle = filterSingle(row, single_list)

            #if the list does not already contain the current entry
            if (isSingle):
                #check to see if it is a machine that has multiple users
                if (filterMulti(row, single_list)):
                    multi_list.append([single_list[-1][0]])
                    single_list.remove(single_list[-1])
                    multi_list.append([row[0]])
            else:
                #check to see if it is a machine that has multiple users
                multi_list.append([single_list[-1][0]])
                single_list.remove(single_list[-1])
                multi_list.append([row[0]])
            continue
        else:
            continue

    return (removeDuplicates(single_list), removeDuplicates(multi_list))

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
            singleWriter.writerow(line)



licensed = tableProcessing("Current Users Licensed to Adobe CC.csv")
notLicensed = tableProcessing("SCCMAdobeList.csv")

compareSingleLicenses(licensed[0], notLicensed[0], notLicensed[1])

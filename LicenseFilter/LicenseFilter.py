import csv
import re
import cProfile


# compares two tables to filter out lab machines from single user machines
def compareSingleLicenses(currentUsers, dataUsers, multiUsers):
    singleCompared = []
    currently_licensed = currentUsers
    stored_licensed = dataUsers
    serializedUsers = multiUsers
    for element in currently_licensed:
        email = element[1]
        for entry in stored_licensed:
            username = entry[1]
            if (checkEmail(email, username) == False):
                singleCompared.append(entry)
            else:
                break

    mergedSingleWriter(singleCompared, serializedUsers)


def tableProcessing(inFile):
    with open(inFile, 'r', newline='') as full_table:
        fullReader = csv.reader(full_table, delimiter=',')

        full_list = list(fullReader)

        writeToList = csvToList(full_list)

        single_list = writeToList[0]
        serializable = writeToList[1]

        return (single_list, serializable)


def checkAdmin(username):
    m = re.match('^[A-a]dmin.*$|^[S-s]ystem.*$', username)
    return m


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
        return False
    else:
        return True


# checks current entry to see if it is a serializable license
def filterMulti(row, currentList):
    username = row[1].lower()
    computername = row[0]
    lastLicenseEntry = currentList[-1]

    if lastLicenseEntry[0] == computername and lastLicenseEntry[1] != username:
        return True
    else:
        return False


# checks for single use and serialized machines
# must contain column headers to function properly
def csvToList(inFile):
    single_list = []
    multi_list = []

    for row in inFile:
        if (row[0] != ''):
            if len(single_list) == 0:
                single_list.insert(0, row)
                multi_list.insert(0, [row[0]])
                continue

            isSingle = filterSingle(row, single_list)

            if (isSingle):
                if (filterMulti(row, single_list)):
                    multi_list.append([single_list[-1][0]])
                    single_list.remove(single_list[-1])
                    multi_list.append([row[0]])
                else:
                    single_list.append(row)
            else:
                multi_list.append([single_list[-1][0]])
                single_list.remove(single_list[-1])
                multi_list.append([row[0]])
            continue
        else:
            continue

    return (removeDuplicates(single_list), removeDuplicates(multi_list))


# removes duplicate entries from lists before writing to file
def removeDuplicates(duplicate):
    final_list = []
    for name in duplicate:
        if name not in final_list:
            final_list.append(name)
    return final_list


def mergedSingleWriter(singleCSV, multiCSV):
    with open('MergedLicenses.csv', 'w', newline='') as file:
        singleWriter = csv.writer(file, delimiter=',', escapechar='')

        singleWriter.writerow(["Single Use Licenses"])
        for line in singleCSV:
            singleWriter.writerow(line)
        singleWriter.writerow(["Number of Single User Licenses:" + str(len(singleCSV))])
        singleWriter.writerow(["Serializable Licenses"])
        for line in multiCSV:
            singleWriter.writerow(line)
        singleWriter.writerow(["Number of Serializable Licenses:" + str(len(multiCSV))])


licensed = tableProcessing("Current Users Licensed to Adobe CC.csv")
notLicensed = tableProcessing("SCCMAdobeList.csv")

compareSingleLicenses(licensed[0], notLicensed[0], notLicensed[1])

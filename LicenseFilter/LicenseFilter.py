import csv
import re
import cProfile


# compares two tables to filter out lab machines from single user machines
def compareTables(table_one, table_two):
    with open(table_one, 'r', newline='') as t1, open(table_two, 'r', newline='') as t2:
        t1Reader = csv.reader(t1, delimiter=',')
        t2Reader = csv.reader(t2, delimiter=',')

        t1List = list(t1Reader)
        t2List = list(t2Reader)

        if (len(t1List) > len(t2List)):
            compared_list = [license for license in t1List if license not in t2List]
        else:
            compared_list = [license for license in t2List if license not in t1List]

    getLicences = writeCSV(compared_list)

    single_list = getLicences[0]
    multi_list = getLicences[1]

    LicenseWriter(single_list)
    LicenseWriter(multi_list)

def macTableProcessing(inFile):
    inFile

def checkAdmin(username):
    m = re.match('^[A-a]dmin.*$|^[S-s]ystem.*$', username)
    return m

#checks current entry to see if it is a single license user
def filterSingle(row, currentList):
    username = row[1]
    if (checkAdmin(username)):
        return False
    computername = row[0]
    lastLicenseEntry = currentList[-1]

    if lastLicenseEntry[1] == username and lastLicenseEntry[0] == computername:
        return False
    else:
        return True

#checks current entry to see if it is a serializable license
def filterMulti(row, currentList):
    username = row[1]
    computername = row[0]
    lastLicenseEntry = currentList[-1]

    if lastLicenseEntry[0] == computername and lastLicenseEntry[1] != username:
        return True
    else:
        return False


# checks for single use and serialized machines
# must contain column headers to function properly
def writeCSV(inFile):
    single_list = []
    multi_list = []

    for row in inFile:
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

    single_list.append("Single")
    multi_list.append("Serialized")

    return (single_list, removeDuplicates(multi_list))

#removes duplicate entries from lists before writing to file
def removeDuplicates(duplicate):
    final_list = []
    for name in duplicate:
        if name not in final_list:
            final_list.append(name)
    return final_list

#writes user or machine entries into files
def LicenseWriter(inputCSV):
    with open(inputCSV[-1] + 'License.csv', 'w', newline='') as file:
        singleWriter = csv.writer(file, delimiter=',', escapechar='')

        for line in inputCSV:
            singleWriter.writerow(line)


cProfile.run('compareTables("ComparedTableTest2.csv", "ComparedTableTest.csv")')

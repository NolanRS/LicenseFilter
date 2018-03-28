import csv
import re


def compareTables(table_one, table_two, outFile):
    table_one


def checkAdmin(username):
    m = re.match('^[A-a]dmin.*$|^[S-s]ystem.*$', username)
    return m


def filterSingle(row, list):
    username = row[1]
    computername = row[0]
    lastLicenseEntry = list[-1]

    if lastLicenseEntry[1] == username and lastLicenseEntry[0] == computername or checkAdmin(username):
        return True
    else:
        return False


def filterMulti(row, list):
    username = row[1]
    computername = row[0]
    lastLicenseEntry = list[-1]

    if lastLicenseEntry[0] == computername and lastLicenseEntry[1] != username:
        return True
    else:
        return False


def writeCSV(inFile):
    list = []
    singleLicense = 0
    multiLicense = 0
    with open('TestSingle.csv', 'w', newline='') as single_file, open(inFile, 'r', newline='') as csv_file, open(
            'TestMulti.csv', 'w', newline='') as multi_file:
        singleWriter = csv.writer(single_file, delimiter=',', escapechar='')
        multiWriter = csv.writer(multi_file, delimiter=',', escapechar='')
        reader = csv.reader(csv_file, delimiter=',')

        singleWriter.writerow(next(reader))
        # gives single use number
        for row in reader:
            if len(list) == 0:
                singleLicense += 1
                list.append(row)

            isSingle = filterSingle(row, list)

            if (isSingle):
                isMulti = filterMulti(row, list)
                if (isMulti):
                    multiWriter.writerow(row)
                    multiLicense+=1
                continue
            else:
                isMulti = filterMulti(row, list)
                if (isMulti):
                    multiWriter.writerow(row)
                    multiLicense+=1
                    continue
                else:
                    singleLicense += 1
                    list.append(row)
        for item in list:
            singleWriter.writerow(item)
        print("Number of single use licenses: " + str(singleLicense))
        print("Number of serializeable use licenses: " + str(multiLicense))


writeCSV("TestCSV.csv")

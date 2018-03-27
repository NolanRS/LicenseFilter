import csv
import re


def compareTables(table_one, table_two, outFile):
    table_one


def filterSingle(row, list):
    username = row[1]
    computername = row[0]
    lastLicenseEntry = list[-1]

    if lastLicenseEntry[1] == username and lastLicenseEntry[0] == computername:
        return False
    else:
        return True


def filterMulti(row, list):
    username = row[1]
    computername = row[0]
    lastLicenseEntry = list[-1]

    if username==''
    if lastLicenseEntry[1] == username and lastLicenseEntry[0] == computername:
        return False
    else:
        return True


def writeCSV(inFile, outFile):
    list = []
    licensesToFix = 0
    with open(outFile, 'w+', newline='') as out_file, open(inFile, 'r', newline='') as csv_file:
        writer = csv.writer(out_file, delimiter=',')
        reader = csv.reader(csv_file, delimiter=',')

        next(reader)
        for row in reader:
            if len(list) == 0:
                licensesToFix += 1
                writer.writerow(row)
                list.append(row)
            lineEntry = filterSingle(row, list)
            if (lineEntry == False):
                continue
            else:
                licensesToFix += 1
                print(','.join(row))
                list.append(row)
                writer.writerow(row)

    print(licensesToFix)


writeCSV("TestCSV.csv", 'TestSuccess.csv')

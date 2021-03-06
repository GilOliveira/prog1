# -*- coding: utf-8 -*-

# 2018-2019 Programação 1 (LTI)
# Grupo 38
# 49187 Sofia Torres
# 49269 Mário Gil Oliveira

import sys
import filesReading
import formated
import filesWriting
import scheduling
import dateTime
from constants import outputIncrement


def checkError(fileNameExperts, fileNameClients):
    """Checks to see if the inputFiles are valid. Checks if the headers of the experts
    and clients files are equal and if the header of a file matches its name
    Requires: fileNameExperts, fileNameClients are str, with the names
    of the files representing the list of experts and clients, respectively,
    following the format indicated in the project.
    Ensures: return True if the files are valid and False if not"""

    # Tests if the clients match between Client and Expert
    headExp = filesReading.readHeader(fileNameExperts)
    headCli = filesReading.readHeader(fileNameClients)
    if headCli[0:3] != headExp[0:3]:
        print("Error in input files: inconsistent files",
              fileNameExperts,"and",fileNameClients)
        return False


    # tests if the header matches the file name
    # ex:2019y03m20clients12h30.txt = ('2019-02-20', '12:30', 'iCageDoree', 'Clients')   <<< deve dar erro neste exemplo
    for i in sys.argv[1:]:
        if i.replace("y","-").replace("m","-")[0:10] != (filesReading.readHeader(i))[0] or \
           str(i[10:17]) != filesReading.readHeader(i)[3].lower() or \
           str(i.replace("h",":")[17:22]) != filesReading.readHeader(i)[1]:
           print("Error in input file: inconsistent name and header in file", i)
           return False
        else:
            return True


def assign(fileNameExperts, fileNameClients):
    """
    Assign given experts given to given clients.
    Requires: fileNameExperts, fileNameClients are str, with the names
    of the files representing the list of experts and clients, respectively,
    following the format indicated in the project.
    Ensures: Two output files, respectively, with the listing of schedules
    tasks and the updated listing of experts, following the format
    and naming convention indicated in the project.
    """

    # Reads the files into the variables
    rawexp = filesReading.readFile(fileNameExperts)
    rawcl = filesReading.readFile(fileNameClients)

    # Formats the file content into lists for usage
    formatedexp = formated.formatExperts(rawexp)
    formatedcli = formated.formatClients(rawcl)

    # schedules the jobs and matches the clients and experts into a tuple
    attributionalOutput = scheduling.attributional(formatedcli,formatedexp)
    tupleClientExpert = attributionalOutput[0]

    # updates the Experts list based on the attributions
    updatedExperts = attributionalOutput[1]

    # sorts the lists in the order to be written in the file
    tupleClientExpert = scheduling.sortScheduleOutput(tupleClientExpert)
    updatedExperts = scheduling.sortExpertsOutput(updatedExperts)

    # Calculates the timestamp of the new file,
    # based on the amount of minutes in outputIncrement
    timestamp = dateTime.timeCalculate(
        filesReading.readHeader(fileNameExperts)[0],
        filesReading.readHeader(fileNameExperts)[1],
        outputIncrement  # time increment from input file
    )

    # Creates a new file for the schedule
    scheduleFile = filesWriting.newFile(
        timestamp[0],
        timestamp[1],
        'schedule',
        filesReading.readHeader(fileNameClients)[2]
    )

    # Appends each schedule entry into the file
    for i in tupleClientExpert:
        filesWriting.addSchedule(scheduleFile, i)

    # Creates a new experts file
    expertsFile = filesWriting.newFile(
        timestamp[0],
        timestamp[1],
        'experts',
        filesReading.readHeader(fileNameClients)[2]
    )

    # Appends each of the experts into the output experts file
    for i in updatedExperts:
        filesWriting.addExpert(expertsFile, i)


# PROGRAM STARTS RUNNING HERE:

inputExperts, inputClients = sys.argv[1:]

if checkError(inputExperts, inputClients):
    assign(inputExperts, inputClients)

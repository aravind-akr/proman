import os
from pathlib import Path
import fnmatch
import restoreStatus
import backupStatus
from bs4 import BeautifulSoup

job_status=["COMPLETED_SUCCESSFULLY","COMPLETED_ERRORS"]


def findStatus(filename):
    os.chdir(filename)
    with os.scandir(filename) as lists:
        for entry in lists:
            if os.path.basename(filename) in entry.name and fnmatch.fnmatch(entry, '*_status.txt'):
                p_text = Path(entry.name)
                xmlfile = os.path.basename(filename)+"_status.xml"
                contents = open(xmlfile).read()
                soup = BeautifulSoup(contents,'xml')

                print(entry.name + " contents")
                print("=================================")
                lists = p_text.read_text().split('\n')
                while '' in lists:
                    lists.remove('')

                print("Current Version of DSC: " + lists[0].split("Line ")[1])

                if lists[1].split(":") == '':
                    print("No command parameters for job_status used")
                else:
                    print("Command Parameters used are: "+lists[1].split(":")[1])

                dscJobName = lists[2].split(":")[1].strip()
                print("DSC Job name is: "+dscJobName)

                soupForOperationType = BeautifulSoup(open(dscJobName+"_plan.xml").read(),'xml')
                operationType = soupForOperationType.find('operation_type').text
                print("Operation type is " + operationType)

                print("Job Id of "+lists[2].split(":")[1] + " is "+soup.find('job_id').text)

                print("Job execution Id: "+soup.find('job_execution_id').text)

                print("Job Status is "+soup.find('job_status').text)

                print("Percentage of Job completion at the time of failure: "+soup.find('backup_progress').text)

                print("Total Time taken to run the job is: "+soup.find('job_elapsed_time').text)

                if operationType == 'BACKUP' or operationType == 'RESTORE':
                    dsmainStatus(lists,soup)
                else:
                    barncStatus(lists,soup)



                if soup.find('job_status').text in job_status:
                    jobErrorsAndWarning = True
                else:
                    jobErrorsAndWarning = False

                print("Source System:"+soup.find('source').text)
                print("Target group:"+soup.find('target').text)



                # if lists[9].startswith("Source backup job"):
                #     restoreStatus.restoreStatus(filename)
                # else:
                #     backupStatus.backupStatus(filename,lists)

                #if(jobErrorsAndWarning):

                print("=================================")


                for errorsWarnings in soup.find_all('errors_warnings'):
                    for tag in errorsWarnings.findChildren():
                        print(tag.name + ":" + tag.text)
                    print("-------------------")


def dsmainStatus(lists,soup):
    for dsmain in soup.find_all('dsmain_status'):
        for tag in dsmain.findChildren():
            print(tag.name + ":" + tag.text)
        print("-------------------")


def barncStatus(lists,soup):
    for dsmain in soup.find_all('barnc_status'):
        for tag in dsmain.findChildren():
            print(tag.name + ":" + tag.text)
        print("-------------------")

#def errorsWarnings(soup):

# def restoreStatus(lists,soup)
# def analyzeReadStatus(lists,soup)
# def analyzeValidateStatus(lists,soup)



if __name__ == "__main__":
    filepath = input("Give your path file name: ")
    findStatus(filepath)












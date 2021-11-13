import csv
import json
import pandas as pd
import random
import requests
import string
from progress.bar import ShadyBar
import whois

def menu():
    print("""
   ___                      _                                                   _                    
  / __\ ___   _   _  _ __  | |_  ___  _ __  /\  /\ __ _  _ __ __   __ ___  ___ | |_     _ __   _   _ 
 / /   / _ \ | | | || '_ \ | __|/ _ \| '__|/ /_/ // _` || '__|\ \ / // _ \/ __|| __|   | '_ \ | | | |
/ /___| (_) || |_| || | | || |_|  __/| |  / __  /| (_| || |    \ V /|  __/\__ \| |_  _ | |_) || |_| |
\____/ \___/  \__,_||_| |_| \__|\___||_|  \/ /_/  \__,_||_|     \_/  \___||___/ \__|(_)| .__/  \__, |
                                                                                       |_|     |___/ 

A python script developed by malwaredetective designed to combat Credential Harvesters! 

Select an option from the menu:

|-------------------------------|-------------------------------------------------------------------------------------------------|
|  1) Launch a Counter Attack!  | Upload randomly generated Credentials to the attacker in an effort to disrupt their operations. |
|  2) Passive Domain Takedown   | Manual walkthrough of passive reporting options to takedown the Credential Harvester.           |
|-------------------------------|-------------------------------------------------------------------------------------------------|

""")
    validInput = False
    while(validInput == False):
        mode = input("Select an Option: ")
        if str(mode) == "1" or str(mode) == "2":
            validInput = True
        else:
            print("\nThat's not a valid selection! Please enter 1 to launch a counter attack, or 2 to initiate a passive domain takedown.\n")
    return mode

def counterAttack():
    confirmedInput = False
    report_details = []
    
    while(confirmedInput == False):
        verifyInput = False
        reportInput = False
        validForm = False
        validCount = False
        baseURL = input("\nWhat is the URL of the Credential Harvester that you would like to counter attack? ").lower()
        while(validForm == False):
            formURL = input("\nWhat URL does the Credential Harvester send data to when the form is submitted? ").lower()
            if formURL.startswith('http'):
                validForm = True
            else:
                print("\nAre you sure that's the correct URL? It looks like your missing an HTTP:// or HTTPS:// schema. The python requests module will not be able to send requests to the submitted URL.")
        emailFormID = input("\nWhat is the value of the Form ID assigned to the Email Address field? ")
        passwordFormID = input("\nWhat is the value of the Form ID assigned to the Password field? ")
        while(validCount == False):
            try:
                count = int(input("\nHow many poisioned Credentials would you like to submit to {}? Please input an integer: ".format(formURL)))
                validCount = True
            except:
                print("\nThat's not a valid selection! Please enter an valid integer.")
        while(reportInput == False):
            report = input("\nWould you like to generate a report to capture the results? (Y/N) ").lower()
            if report == "y" or report == "yes": 
                report = True
                reportInput = True
            elif report == "n" or report == "no":
                report = False
                reportInput = True
            else:
                print("\nThat's not a valid selection! Please enter Y or N.")
        while(verifyInput == False):
            confirmResults = input("\nPlease confirm the details that you submitted: \n\nCredential Harvester: {}\nForm URL: {}\nForm ID for Email: {}\nForm ID for Password: {}\nNumber of poisioned Credentials: {}\nReport: {}\n\nConfirm your request details and launch a Counter Attack? (Y/N) ".format(baseURL, formURL, emailFormID, passwordFormID, count, report)).lower()
            if confirmResults == "y" or confirmResults == "yes":
                verifyInput = True
                confirmedInput = True
                print("")
            elif confirmResults == "n" or confirmResults == "no":
                verifyInput = True
            else:
                print("\nThat's not a valid selection! Please enter Y or N.")

    domains = json.loads(open('domains.json').read())

    passphrase = json.loads(open('passphrase.json').read())
    adjectives = passphrase['components'][0]['adjectives']['data']
    animals = passphrase['components'][0]['animals']['data']
    chars = string.digits + '!@#$%^&*()'

    usernames = json.loads(open('username.json').read())
    first_names = usernames['components'][0]['first_names']['data']
    last_names = usernames['components'][0]['last_names']['data']
    random.shuffle(first_names)
    random.shuffle(last_names)

    seperator = ["", ".", "_"]

    i = 0

    with ShadyBar('Sending Payload...', max=count) as bar:
        while i < count:
            #username = first_names[i].lower() + random.choice(seperator) + last_names[i].lower() + random.choice(domains)
            username = random.choice(first_names).lower() + random.choice(seperator) + random.choice(last_names).lower()+ random.choice(domains)
            password = random.choice(adjectives).lower() + random.choice(animals).lower() + random.choice(chars)
            r = requests.post(formURL, allow_redirects=False, data={
                '{}'.format(emailFormID): username,
                '{}'.format(passwordFormID): password
            })
            if report == True:
                report_details.append([username, password, str(r.status_code), formURL, baseURL])
            else:
                pass
            bar.next()
            i += 1
        bar.finish()

    if report == True:
        print("Generating a report: CounterHarvest.csv in the current working directory ...\n")
        reportComplete = False
        while(reportComplete == False):
            with open('CounterHarvest.csv', 'a', newline = '') as outcsv:
                writer = csv.DictWriter(outcsv, fieldnames = ["Email", "Password", "Status Code", "Form", "Credential Harvester"])
                writer.writeheader()
                writer = csv.writer(outcsv)
                writer.writerows(report_details)
                reportComplete = True
    else:
        pass
    print("Operation Complete! Sent {} poisioned credentials to {} to try and disrupt the Credential Harvester hosted at {}! If you haven't already, try leveraging CounterHarvest.py's passive domain takedown capabilities to cause even more turmoil to the advesaries operation.".format(count, formURL, baseURL))

def passiveDomainTakedown():
    baseURL = input("\nWhat is the URL of the Credential Harvester? ").lower()
    print("\nVisit https://safebrowsing.google.com/safebrowsing/report_phish/?hl=en and report {} as a Phishing page. Google Chrome is still the worlds most popular web browser, so adding the site to Googles Safe Browsing warning list will proactively prevent a large number of victims from being impacted.".format(baseURL))
    input("\nPress enter to continue ... ")
    print("\nRetrieving WHOIS information for {}".format(baseURL))
    try:
        w = whois.whois(baseURL)
        print("")
        print(w)
    except:
        print("\nAn error occured! Unable to query {} for WHOIS information.".format(baseURL))
        print("\nTry looking up the WHOIS information manually from whois.domaintools.com.")        
    print("\nSend an email to the abuse notification contact to inform them that {} is hosting a Credential Harvester. That effort could get the site taken offline and may even cause damage to the owner if they are hosting multiple resources through the same provider.".format(baseURL))
    
# Application Entry Point
def main():
    mode = menu()
    if mode == "1":
        counterAttack()
    else:
        passiveDomainTakedown()

if __name__ == "__main__":
    main()
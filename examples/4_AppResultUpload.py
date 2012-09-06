from BaseSpacePy.api.BaseSpaceAPI import BaseSpaceAPI
import os
import helper #@UnresolvedImport

"""
This script demonstrates how to create a new AppResults object, change its state
and upload result files to it and download files from it.  
"""
# FILL IN WITH YOUR APP VALUES HERE!
client_key                 = ""
client_secret              = ""
appSessionId               = ""
accessToken                = ""
# test if client variables have been set
#helper.checkClientVars({'client_key':client_key,'client_secret':client_secret,'AppSessionId':ApplicationActionId}) 

BaseSpaceUrl               = 'https://api.cloud-endor.illumina.com'
version                    = 'v1pre3'

# First, create a client for making calls for this user session 
myBaseSpaceAPI   = BaseSpaceAPI(client_key, client_secret, BaseSpaceUrl, version, appSessionId,AccessToken=accessToken)


# Now we'll do some work of our own. First get a project to work on
# we'll need write permission, for the project we are working on
# meaning we will need get a new token and instantiate a new BaseSpaceAPI  
p = myBaseSpaceAPI.getProjectById('89')

# A short-cut for getting a scope string if we already have a project-instance:
print p.getAccessStr(scope='write')
# or simply
p.getAccessStr()

# Assuming we now have write access for the project
# we will list the current App Results for the project 
appRes = p.getAppResults(myBaseSpaceAPI,statuses=['Running'])
print "\nThe current running AppResults are \n" + str(appRes)

# now let's do some work!
# to create an appResults for a project, simply give the name and description
appResults = p.createAppResult(myBaseSpaceAPI,"### testing","this is my results")
print "\nSome info about our new app results"
print appResults
print appResults.Id
print "\nThe app results also comes with a reference to our AppSession"
myAppSession = appResults.AppSession
print myAppSession

# we can change the status of our AppSession and add a status-summary as follows
myAppSession.setStatus(myBaseSpaceAPI,'needsattention',"We worked hard, but encountered some trouble.")
print "\nAfter a change of status of the app sessions we get\n" + str(myAppSession)

### Let's list all AppResults again and see if our new object shows up 
appRes = p.getAppResults(myBaseSpaceAPI,statuses=['Running'])
print "\nThe updated app results are \n" + str(appRes)
appResult2 = myBaseSpaceAPI.getAppResultById(appResults.Id)
print appResult2

## Now we will make another AppResult 
## and try to upload a file to it
appResults2 = p.createAppResult(myBaseSpaceAPI,"My second AppResult","This one I will upload to")
appResults2.uploadFile(myBaseSpaceAPI, '/home/mkallberg/Desktop/testFile2.txt', 'BaseSpaceTestFile.txt', '/mydir/', 'text/plain')
print "\nMy AppResult number 2 \n" + str(appResults2)

## let's see if our new file made it
appResultFiles = appResults2.getFiles(myBaseSpaceAPI)
print "\nThese are the files in the appResult"
print appResultFiles
f = appResultFiles[-1]

# we can even download our newly uploaded file
f = myBaseSpaceAPI.getFileById(f.Id)
f.downloadFile(myBaseSpaceAPI,'/home/mkallberg/Desktop/')
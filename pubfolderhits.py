import boto3
import time
import os
import configparser

# Before connecting to MTurk, set up your AWS account and IAM settings as described here:
# https://blog.mturk.com/how-to-use-iam-to-control-api-access-to-your-mturk-account-76fe2c2e66e2
# 
# Follow AWS best practices for setting up credentials here:
# http://boto3.readthedocs.io/en/latest/guide/configuration.html 

# Use the Amazon Mechanical Turk Sandbox to publish test Human Intelligence Tasks (HITs) without paying any money.
# Sign up for a Sandbox account at https://requestersandbox.mturk.com/ with the same credentials as your main MTurk account.
topLevelDir = 'HITBatches'

def publishHit(folder, imgSet, client, ann, upTime):
    config = configparser.ConfigParser()
    config.read('config.ini')
    print(imgSet)
    qxml = "<ExternalQuestion xmlns=\"http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14/ExternalQuestion.xsd\"> \
            <ExternalURL>https://" + config['SetUp']['firebaseSubdomain'] +".firebaseapp.com/index.html?category-image="+folder+"+"+imgSet[0]

    for i in range(1, len(imgSet)):
        qxml = qxml + "+" + imgSet[i]

    qxml = qxml + "&amp;annotation="+ann[0]

    for i in range(1, len(ann)):
        qxml = qxml + "+" + ann[i]

    qxml += "</ExternalURL> \
        <FrameHeight>900</FrameHeight>\
        </ExternalQuestion>"

    # questionSampleFile = open("my_question.xml", "r")
    # questionSample = questionSampleFile.read()

    # Create a qualification with Locale In('US') requirement attached 
    # NOT CURRENTLY USED but template available if you would like
    localRequirements = [{
        'QualificationTypeId': '00000000000000000071',
        'Comparator': 'In',
        'LocaleValues': [{
            'Country': 'US'
        }],
        'RequiredToPreview': True
    }]

    # Create the HIT 
    response = client.create_hit(
        MaxAssignments = 3,
        LifetimeInSeconds = upTime,
        AssignmentDurationInSeconds = 600,
        Reward ='0.02',
        Title = 'Annotate Image',
        Keywords = 'Computer Vision, Image, Annotation',
        Description = 'Annotate images for database',
        Question = qxml
    )

    # The response included several fields that will be helpful later
    hit_type_id = response['HIT']['HITTypeId']
    hit_id = response['HIT']['HITId']
    print ("Your HIT has been created. You can see it at this link:")
    print ("https://workersandbox.mturk.com/mturk/preview?groupId={}".format(hit_type_id))
    print ("Your HIT ID is: {}".format(hit_id))
    return hit_id

def publishAll(folderName, numPer, client, ann, upTime, productionBool):
    hitfileFolder = topLevelDir + '/'+folderName+time.strftime("%Y%m%d-%H%M%S")
    if (productionBool):
        hitfileFolder += '_production'
    os.mkdir(hitfileFolder)
    hitfileName = hitfileFolder + '/hitList.txt'
    hitidfile = open(hitfileName,'w')
    allFiles = os.listdir('toWeb/public/images/'+folderName)
    for i in range(0,len(allFiles),numPer):
        imgSet = []
        for j in range(i,i+numPer): 
            if j < len(allFiles):
                fn = allFiles[j]
                if fn == '.DS_Store': continue
                imgSet.append(fn)
        hitid = publishHit(folderName, imgSet, client, ann, upTime)
        if (len(imgSet)>0):
            imgSetString = imgSet[0]
            for i in range(1,len(imgSet)):
                imgSetString = imgSetString + "+" + imgSet[i]
            hitidfile.write(folderName+'\\'+imgSetString+", " + hitid + "\n")

        
        
def publish(foldername, numPer, pubType, ann, user):
    productionBool = False
    config = configparser.ConfigParser()
    config.read('config.ini')
    region_name = 'us-east-1'
    if pubType == 'developer':
        endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
        upTime = 600
    elif pubType == 'production':
        endpoint_url = 'https://mturk-requester.us-east-1.amazonaws.com'
        upTime = 604800*2
        productionBool = True
    else:
        raise NameError('Must specify developer or production type deployment')
        return 
    client = boto3.client('mturk',
        endpoint_url = endpoint_url,
        region_name = region_name,
        aws_access_key_id = config[user]['awskey'], ## Put AWS Access keys in Config File
        aws_secret_access_key = config[user]['awssakey'],
    )


    publishAll(foldername, numPer, client, ann, upTime, productionBool)

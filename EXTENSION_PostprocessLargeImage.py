"""
Author: Trishul Nagenalli (tn74@duke.edu)
Organization: Duke Energy Data Analytics Lab

Description:
Use this script to post process an image that was cut into several pieces before being placed online (like in the case you wanted to annotate a large satellite image for example).

If you would like to process large Satellite images, follow the steps below
1. Set imageToCut as the name of the image you would like to cut and run AADON_PreprocessLargeImage.py
2. Open ASCRIPT_begin.py and set folderToPublish as the name of the image without the file extension. Run it.
3. Wait for Annotations
4. Run ASCRIPT_finish.py with the appropriate Batch ID
5. Run AADDON_PostprocessLargeImage.py with on the specified Batch ID 

Variable Information

hitBatch				- 	The Batch ID of the batch you would like to process (ethe )
"""

#====================== Set Variables below
hitBatch = 'Norfolk_01_training20170727-152336'
#======================

import jsonReader as jr
import usefulImageFunc as uif
import postProcessing as pp
import os

topLevelDir = 'HITBatches'
jr.consolidateLargeImage(hitBatch, 'all_submitted.txt')
uif.annImageWholeJSON(hitBatch, 'pieced_all_submitted.txt')
pp.genConfArrays(hitBatch,'pieced_all_submitted.txt','_all_submitted')
if os.path.exists(topLevelDir + '/' + hitBatch + '/accepted.txt'):
	if (len(open(topLevelDir + '/' + hitBatch + '/accepted.txt', 'r').readlines()) != 0):
		jr.consolidateLargeImage(hitBatch, 'accepted.txt')
		uif.annImageWholeJSON(hitBatch, 'pieced_accepted.txt')
		pp.genConfArrays(hitBatch,'pieced_accepted.txt', '_all_accepted')

"""
This program runs a GUI that allows a user to approve or reject HIT annotation tasks on a per image basis. It outputs a
.txt file with the assignment IDs of the accepted HITs, a separate for the rejected ones, and also uses boto3 and the
 usefulFunctions.py to approve Hits via the Turk API.

Author: Shamikh Hossain (ssh50@duke.edu)
Organization: Duke Energy Data Analytics Lab
"""

from tkinter import Tk, Label, Button
from PIL import Image
from PIL.ImageDraw import Draw
import json
import usefulFunctions as uf
import usefulImageFunc as ui
from tkinter import *
from PIL import Image, ImageTk
import os
import argparse

ap = argparse.ArgumentParser(description='Accept or reject hits from the entered directory.')

ap.add_argument("-f", "--folder", type=str, default= ".",
                help="String of the folder that contains indJSONS.txt (a txt file of jsons). ex: folders/powerplants20170707-130633")
args = vars(ap.parse_args())

imgdir = "/".join(args["json"].split("/")[:-1])

class Hit:
    def __init__(self, txt, id, img, dir, annot):
        """
        :param txt: whole json line
        :param id: assignmentID
        :param img: image filename
        :param dir: directory of image files
        :param annot:
        """
        self.txt = txt
        self.id = id
        self.img = img
        self.dir = dir
        self.annot = annot
        self.result = "" # reference to accepted or rejected status

    def __str__(self):
        return self.dir + '/' + self.img

    def accept(self):
        self.result = "accept"

    def reject(self):
        self.result = "reject"

# JSON example:
# {"assignmentID": "3X1FV8S5JYZR0QSGZLEQ46KD2AQGVU", "annotations": ["building", "road", "car"], "fileName":
# "Norfolk_01_training_small/Norfolk_01_training_small_U0000_L0200.jpg", "objs": [{"name": "building", "type":
# "polygon", "data": [[[22, 41, 92, 71], [92, 111, 159, 142], [171, 155, 208, 224], [42, 56, 56, 4, 3, 2],
# [64, 80, 131, 119]], [[47, 16, 44, 79], [77, 49, 72, 104], [85, 114, 139, 111],167, 182, 195, 210, 199, 181]]]},
# {"name": "road", "type": "line", "data": [[[123, 234, 251, 261, 262, 264, 217]], [[6, 61, 69, 79, 90, 119, 291]]]},
# {"name": "car", "type": "point", "data": [[154, 159, 215, 250], [59, 46, 37, 134]]}]}

accepted, rejected = [], []

class GUI:
    def __init__(self, master, hit):
        self.master = master
        self.hit = hit
        # get fixed window size by setting bounds


        # master.bind('y', self.y)
        # master.bind('n', self.n)


        master.title('Accept or Reject HITs')

        img_path = "toWeb/public/images/" + hit.dir + "/" + hit.img
        self.gen_img = ui.gen_Image(img_path, hit.txt)
        img = Image.open(self.gen_img)
        # [width, height] = img.size

        # adjust these to resize images or the window! 
        width = img.size[0]//3
        height = img.size[1]//3
        img = img.resize((width, height), Image.ANTIALIAS)
        master.minsize(width=width + 100, height=height + 100)
        master.maxsize(width=width + 100, height=height + 100)

        img = ImageTk.PhotoImage(img)

        # txt = self.hit.annot
        self.label = Label(master, image = img)
        self.label.image = img
        self.label.pack()

        self.by = Button(master, text= self.hit.annot)
        self.by.pack()

        self.accept_button = Button(master, text="Accept", command=self.y)
        self.accept_button.pack()

        self.reject_button = Button(master, text="Reject", command=self.n)
        self.reject_button.pack()

    def y(self, event=None):
        self.hit.accept()
        accepted.append(self.hit)
        print("The hit was {}ed!".format(self.hit.result))
        self.label.destroy()
        self.by.destroy()
        self.accept_button.destroy()
        self.reject_button.destroy()
        try:
            os.remove(self.gen_img)
        except:
            print('file not found')

    def n(self, event=None):
        self.hit.reject()
        rejected.append(self.hit)
        print("The hit was {}ed!".format(self.hit.result))
        self.label.destroy()
        self.by.destroy()
        self.accept_button.destroy()
        self.reject_button.destroy()
        os.remove(self.gen_img)
        try:
            os.remove(self.gen_img)
        except:
            print('file not found')

def loadjson(filepath):
    """ Returns a list of Hit objects using jsons in a text file, and the directory name in a tuple.
        @param file .txt file that contains JSON objects."""
    hits = []
    for line in open(filepath):
        d = json.loads(line)
        id = d["assignmentID"]
        dir = d["fileName"].split("/")[0]
        img = d["fileName"].split("/")[1]
        annot = ' '.join(d['annotations'])
        hits.append(Hit(line, id, img, dir, annot))
    return (hits, dir)

root = Tk()
path = args['folder'] + '/indJSONS.txt'
hitlist = loadjson(path)[0] # returns a list
print (len(hitlist))


# "folders/'powerplants20170707-130633/indJSONS.txt"

for f in hitlist:
    status = uf.checkStatus(uf.createRealClient("Bradbury"), f.id)
    if status == "Submitted":
        my_gui = GUI(root, f)
    else:
        print("AssignmentID " + f.id + " has already been evaluated.")
root.mainloop()


accepted_ids = [hit.id for hit in accepted]
rejected_ids = [hit.id for hit in rejected]

print('{} hits were approved'.format(len(accepted_ids))) # prints after the window is closed
print('{} hits were rejected'.format(len(rejected_ids)))

f = open(imgdir + "/accepted" + ".txt", "a")
for i in accepted:
     f.write(json.dumps(i.txt) + '\n')
f.close()


rej = open(imgdir + "/rejected" + ".txt", "a")
for i in rejected:
     rej.write(json.dumps(i.txt) + '\n')
rej.close()

uf.approveAssignments(uf.createRealClient("Bradbury"), accepted_ids) # Approve HITs with boto3
uf.rejectAssignments(uf.createRealClient("Bradbury"), rejected_ids) # Reject HITs with boto3


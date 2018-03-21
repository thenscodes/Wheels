# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 11:59:18 2018

@author: thens
"""

from io import StringIO
import sys
import os
from matplotlib import pyplot as plt

def prepareImageArray(files, title):
    total = len(files)
    panel=5
    panel_height=3
    panel_width=2
    nrows = int(total/panel)
    curr_figsize = plt.rcParams["figure.figsize"]
    plt.rcParams["figure.figsize"] = (panel*panel_width,nrows*panel_height)
    ax = [ [plt.subplot2grid((nrows,panel),(i,j)) for j in range(panel)] for i in range(nrows)]
    count = 0
    for i in range(nrows):
        for j in range(panel):
            count = count + 1
            idx = i*panel+j
            file = files[idx]
            ax[i][j] = plt.subplot2grid((nrows,panel),(i,j))
            ax[i][j].imshow(plt.imread(file))
            ax[i][j].set_xlabel(count,fontsize=12)
            ax[i][j].set_yticks([])
            ax[i][j].set_xticks([])
            # add a ylabel
        #ax[i][0].set_ylabel('Stage '+str(i+1), fontsize=14)
    plt.suptitle(title,fontsize=16,y=1.0)
    plt.tight_layout()
    plt.show(block=False)
    plt.rcParams["figure.figsize"] = curr_figsize

def prepareImageChart(result):
    total = len(result)
    panel = 5
    panel_height=3
    panel_width=2

    nrows = int(total/panel)
    curr_figsize = plt.rcParams["figure.figsize"]
    plt.rcParams["figure.figsize"] = (panel*panel_width,nrows*panel_height)
    ax = [ [plt.subplot2grid((nrows,panel),(i,j)) for j in range(panel)] for i in range(nrows)]

    for i in range(nrows):
        for j in range(panel):
            idx = i*panel+j
            res = result[idx]
            title = res['first_label'] + ":" + res['first_conf'] + "\n" + res['second_label'] + ":" + res['second_conf']
            ax[i][j] = plt.subplot2grid((nrows,panel),(i,j))
            ax[i][j].imshow(plt.imread(res['file']))
            ax[i][j].set_xlabel(title,fontsize=12)
            ax[i][j].set_yticks([])
            ax[i][j].set_xticks([])
            # add a ylabel
        #ax[i][0].set_ylabel('Stage '+str(i+1), fontsize=14)
    plt.suptitle("Test Result",fontsize=16,y=1.0)
    plt.tight_layout()
    plt.show(block=False)
    plt.rcParams["figure.figsize"] = curr_figsize

# https://stackoverflow.com/questions/16571150/how-to-capture-stdout-output-from-a-python-function-call
class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout
        
#with Capturing() as output:
#    do_something(my_object)
if (len(sys.argv) <= 1):
    print ("ERROR: Usage ",sys.argv[0], " <image directory>")
    sys.exit()
    

directory= sys.argv[1]

result= []
for image_file in (os.listdir(directory)):
    file = directory+"/"+image_file
    print ("FILE>>", file)
    with Capturing() as output:
        runfile ('C:/Projects/Misc/tensorflow/tensorflow/examples/label_image/label_image.py', args='--graph=/tmp/output_graph.pb --labels=/tmp/output_labels.txt --input_layer=input --output_layer=final_result --input_height=128 --input_width=128 --input_mean=128 --input_std=128 --image='+file)
    label1 = output[0].split(" ")
    label2 = output[1].split(" ")
    res = { 'file' : file }
    if (label1[1] > label2[1]):
        res['first_label'] = label1[0]
        res['second_label'] = label2[0]
        res['first_conf'] = label1[1]
        res['second_conf'] = label2[1]
    else:
        res['first_label'] = label2[0]
        res['second_label'] = label1[0]
        res['first_conf'] = label2[1]
        res['second_conf'] = label1[1]
    result.append(res)

print (result)
prepareImageChart(result)
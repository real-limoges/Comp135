#!/usr/bin/python

import copy
import arff
import sys
import random
from math import ceil

def get_data(data_file):
    data = []
    x = 0
    for row in arff.load(data_file):
	addMe = list(row)
	example_number = "ex" + str(x)
	addMe.pop()
	data.append({
	    'name'      : example_number,
	    'point'     : addMe,
	    'label'     : int(-1),
	    'mark'      : 0,
	    'fold'      : int(-1),
	    'guess'     : int(-1),
	    'out'       : 0
	})
	x = x + 1 
    return data

def normalize(data):
    features = len(data[0]['point'])
    lendata = len(data)
    for feat in range(0,features):
    	x = 0
    	x2 = 0
    	for row in range(0,lendata):
            addMe = data[row]['point'][feat]
            x = x + addMe
            x2 = x2 + addMe**2
    	mean = float(x)/float(lendata)
    	stdev = ((float(x2)/float(lendata)) - (mean**2))**0.5
    	for row in range(0,lendata):
            if stdev == 0:
		data[row]['point'][feat] = 0
            else:
		data[row]['point'][feat] = (data[row]['point'][feat] - mean) / stdev

def distance_matrix(data):
    distances = []
    for i in range(0,len(data)):
	distances.append([])
	for j in range(0, len(data)):
            distances[i].append(find_distances(data[i],data[j]))
    return distances

def find_distances(point1, point2):
    features = len(point1['point'])
    distance = 0
    for feat in range(0, features):
	distance = (point1['point'][feat] - point2['point'][feat])**2
    distance = distance**0.5
    return distance


# DBSCAN to Create the Synthetic Labels 

def DBSCAN(data, distances, epsilon, minpts, num):
    C = 0
    for point in range(0,len(data)):
	if data[point]['mark'] == 0:
            data[point]['mark'] = 1
            Neighbors = neighborPts(epsilon, point, distances)
            if len(Neighbors) >= minpts:
		expandCluster(point, Neighbors, C, epsilon, minpts, data, distances)
		C = C + 1
    unmarked = 0
    for x in range(0,len(data)):
	if data[x]['label'] == -1:
            unmarked = unmarked + 1
    y = round((float(unmarked)/float(len(data))),4)
    if num == 0:
	return y
    else:
    	print "\nAnomalies are ", y*100, "%"
        for c in range(0,C):
            sum = 0
            for x in range(0,len(data)):
            	if data[x]['label'] == c:
                    sum = sum + 1
            print "Cluster ", c, " has ", sum

# Part of DBSCAN to create Labels
def neighborPts(epsilon, point, distances):
    neighbors = []
    for item in range(0,len(distances[point])):
	if distances[point][item] <= epsilon and point != item:
            neighbors.append(item)
    return neighbors

# Part of DBSCAN to create Labels
def expandCluster(point, Neighbors, C, epsilon, minpts, data, distances):
    data[point]['label'] = C
    while len(Neighbors)> 0:
	x = Neighbors.pop()
	if data[x]['mark'] == 0:
            data[x]['mark'] = 1
            Neighbors_1 = neighborPts(epsilon, x, distances)
            if len(Neighbors_1) >= minpts:
		while len(Neighbors_1)>0:
                    Neighbors.append(Neighbors_1.pop())
        if data[x]['label'] == -1:
            data[x]['label'] = C



# Reworked DBSCAN Algorithm modified for not using held out fold data
def DBSCAN_fold(data, distances, epsilon, minpts, fold):
    C = 0
    for point in range(0,len(data)):
	if data[point]['mark'] == 0 and data[point]['fold'] != fold:
            data[point]['mark'] = 1
            Neighbors = neighborPts_fold(data, epsilon, point, distances, fold)
            if len(Neighbors) >= minpts:
		expandCluster_fold(point, Neighbors, C, epsilon, minpts, data, distances, fold)
		C = C + 1
    unmarked = 0
    for x in range(0,len(data)):
	if data[x]['fold'] != fold:
            if data[x]['guess'] == -1:
            	unmarked = unmarked + 1
    denominator = 0
    for x in range(0,len(data)):
	if data[x]['fold'] != fold:
            denominator = denominator + 1
    print "Anomaly Percentage : ", round((float(unmarked)/float(denominator)),4)*100
    print "Anomalies    has ", unmarked
    for c in range(0,C):
        sum1 = 0
	for x in range(0,len(data)):
            if data[x]['guess'] == c:
		sum1 = sum1 + 1
	print "Cluster ", c, " has", sum1

# See Above
def neighborPts_fold(data, epsilon, point, distances, fold):
    neighbors = []
    for item in range(0,len(distances[point])):
	if distances[point][item] <= epsilon and point != item:
            if data[item]['fold'] != fold:
		neighbors.append(item)
    return neighbors

# See Above
def expandCluster_fold(point, Neighbors, C, epsilon, minpts, data, distances, fold):
    data[point]['guess'] = C
    while len(Neighbors)>0:
	x = Neighbors.pop()
	if data[x]['mark'] == 0:
            data[x]['mark'] = 1
            Neighbors_1 = neighborPts_fold(data, epsilon, x, distances, fold)
            if len(Neighbors_1) >= minpts:
		while len(Neighbors_1)>0:
                    Neighbors.append(Neighbors_1.pop())
	if data[x]['guess'] == -1:
            data[x]['guess'] = C

# Assigns each data point a fold number, picked from int((0,10))
def define_folds(data):
    for item in range(0,len(data)):
	data[item]['fold'] =int(random.uniform(0,10))
    print "\nNumber in Each Fold:"
    for x in range(0,10):
        sum1 = 0
        for item in range(0,len(data)):
            if data[item]['fold'] == x:
		sum1 = sum1 + 1
	print "Fold ", x, "has ", sum1


def minindex(dist, fold, data):
    for i in range(0,len(data)):
	if data[i]['guess'] != -1 and data[i]['fold'] != fold:
            min = dist[i]
            index = i
            break
    for i in range(0,len(data)):
        if data[i]['guess'] != -1 and dist[i] < min:
            index = i
            min = dist[i]
    return index


def maxindex(dist, fold, data, c, minind):
    max = dist[minind]
    index = minind
    for i in range(0,len(data)):
	if data[i]['guess'] == c and data[i]['fold'] != fold and dist[i]>max:
            index = i
            max = dist[i]
    return index

# Calculates the measure of outlierness 
def rate_outlier(data, fold, distances):
    for item in range(0,len(data)):
	if data[item]['guess'] == -1 and data[item]['fold'] != fold:
            dist = distances[item]
            minind = minindex(dist, fold, data)
            c = data[minind]['guess']
            maxind = maxindex(dist, fold, data, c, minind)
            dist1 = distances[item][minind]
            dist2 = distances[minind][maxind]
            outlierness = round(float(dist1)/float(dist2),4)
            data[item]['out'] = data[item]['out'] + outlierness


# Sets the problem into a binary class problem
def collapse_Data(data, num):
    if num == 0:
	string = 'label'
    elif num == 1:
	string = 'guess'
    for item in range(0,len(data)):
	if data[item][string] >= 0:
            data[item][string] = 1
	elif data[item][string] == -1:
            data[item][string] = 0

# Prints Confusion Matrices
def accuracy_measures(data, fold):
    fp = 0
    tp = 0
    fn = 0
    tn = 0
    for item in range(0,len(data)):
	if data[item]['fold'] != fold:
            if data[item]['label'] == 1 and data[item]['guess'] == 1:
		tp = tp+1
            elif data[item]['label'] == 1 and data[item]['guess'] == 0:
                fp = fp+1
            elif data[item]['label'] == 0 and data[item]['guess'] == 0:
		tn = tn+1
            elif data[item]['label'] == 0 and data[item]['guess'] == 1:
		fn = fn+1
            else:
		error = error + 1
    print "\n   Confusion Matrix     "
    print "------------------------"
    print "|         Predicted    |"
    print "|           0      1   |"
    print "|Actual  0 ",tn, "   ", fp, "  |"
    print "|        1 ",fn, "  ", tp, "  |" 
    print "------------------------\n"

    accuracy = round((float(tp+tn)/float(tp + fn + fp + tn))*100,2)
    fp_rate = round((float(fp)/float(fp+tn))*100,2)
    fn_rate = round((float(fn)/float(fn+tp))*100,2)
    print "Accuracy : ", accuracy
    print "False Positive Rate : ", fp_rate
    print "False Negative Rate : ", fn_rate

# Unmarks the data for the next fold
def reset_data(data):
    for item in range(0,len(data)):
	data[item]['mark'] = 0
	data[item]['guess'] = -1

# Calls the reset_data function which unmarks data.  Then Calls DBSCAN_fold
# to run on the held out data.
def run_DBSCAN_fold(data, distances, epsilon, minpts):
    for fold in range(0,10):
        print "\nFold ", fold, ":"
	reset_data(data)
	DBSCAN_fold(data, distances, epsilon, minpts, fold)	
	rate_outlier(data, fold, distances)
	collapse_Data(data,1)
	accuracy_measures(data, fold)

def print_outliers(data, output, name):
    string1 = name + " results" + "\n\n"
    output.write(string1)

    outliers = []
    for item in range(0,len(data)):
	if data[item]['out'] != 0:
            x = copy.deepcopy(data[item])
            outliers.append(x)

    while len(outliers)>0:
	max = outliers[0]['out']
	index = 0
	for item in range(0,len(outliers)):
            if outliers[item]['out'] > max:
		index = item
		max = outliers[item]['out']
	x = outliers.pop(index)
	string1 = x['name'] + " : " + str(x['out'])+ "\n"
	output.write(string1)

def main(args):
    random.seed(7202075)
    data = get_data(args[1])
    name = args[1]
    output = open(args[2], 'w')
    # Set initial points
    if args[1] == 'dataset1.arff':
	epsilon = 0.01
	minpts = 5
	error = 0.02
    else:
	epsilon = 0.01
	minpts = 3
	error = 0.04

    normalize(data)
    distances = distance_matrix(data)
    epsilon = find_epsilon(epsilon, data, distances, minpts, error)
    DBSCAN(data, distances, epsilon, minpts, 1)
    define_folds(data)
    collapse_Data(data, 0)
    run_DBSCAN_fold(data, distances, epsilon, minpts)
    print_outliers(data, output, name)

#Iteratively Finds the Optimal Value of Epsilon, given a target error
#percentage and a fixed minpts.  Greedy - finds the first in an acceptable
#range.
def find_epsilon(epsilon, data, distances, minpts, error):
    # Find Optimal Epsilon
    diff = 10
    counter = 0
    while diff > 0.005:
	counter = counter + 1
	if counter%20 == 0:
            print "Iteration : ", counter
	if counter > 1000:
            print "didn't converge"
            break
	x = DBSCAN(data, distances, epsilon, minpts,0)
	diff = abs(x - error)
	for item in range(0,len(data)):
            data[item]['mark'] = 0
            data[item]['label'] = -1
	if diff <= 0.005:
            break
	if epsilon > 0.20:
            break
	if x > error:
            epsilon = epsilon + 0.0001
	else:
            epsilon = epsilon - 0.0001
    return epsilon
main(sys.argv)

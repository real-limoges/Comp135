#!/usr/bin/python
'''
COMP 135, Spring 2014
Benjamin Limoges
Assignment 6

Note: I have used the code sample available from Project 1
and added a few functions of my own to address problems for 
Assignment 4 and Assignment 6. I have put a comment on these
functions that states that they were new functions.  There were
some minor changes to the main() function as well.

*****************************
*****************************
Important Note:

This program takes a very long time to run.  I highly recommend
running this overnight in the background.  Please see README
file.
*****************************
*****************************
'''

import sys
import copy
import arff
import string
import math
import time

def get_training(training_file):
    training = []
    for row in arff.load(training_file) :
        row = list(row)
        training.append({
            'class' : row.pop(),
            'point' : row
        })
    return training

#New Function

def find_k(args):
    for item in range(0,len(args)):
	if args[item] == "-k":
            return int(7)

#New Function

def find_normalize(args):
    for item in range(0,len(args)):
	if args[item] == "-Z":
            return int(1)

#New Function

def find_means(row,dimension):
    means = []
    for item in range(0,dimension):
	sum = 0
	for x in range(0,len(row)):
            sum = sum + row[x][item]
	mean = round(float(sum/len(row)),5)
    	means.append(mean)
    return means

#New Function

def find_st_dev(row, means, dimension):
    stdevs = []
    for item in range(0, dimension):
        sqdev = 0
        for x in range(0,len(row)):
            sqdev = sqdev + (row[x][item] - means[item])**2
        var = sqdev/(len(row)-1)
	stdevs.append(round((sqdev/(len(row)-1))**0.5,5))
    return stdevs    

def correlation(training, feature):
    length = float(len(training))
    sum_sq_x = 0.0
    sum_sq_y = 0.0
    sum_coproduct = 0.0
    mean_x = 0.0
    mean_y = 0.0
    for item in range(0,len(training)):
        sum_sq_x += training[item]['point'][feature]**2
        sum_sq_y += float(training[item]['class'])**2
        sum_coproduct += training[item]['point'][feature] * float(training[item]['class'])
        mean_x += training[item]['point'][feature]
        mean_y += float((training[item]['class']))
    mean_x = mean_x / length
    mean_y = mean_y / length
    pop_sd_x = ((sum_sq_x/length) - (mean_x **2))**0.5
    pop_sd_y = ((sum_sq_y/length) - (mean_y **2))**0.5
    cov_x_y = (sum_coproduct/length)- (mean_x * mean_y)
    correlation = cov_x_y / (pop_sd_x * pop_sd_y)
    return abs(correlation)

def main(args):
    filter_time = time.time()
    training = get_training(args[1])
    output_filter = open(args[2], 'w')
    output_wrapper = open(args[3], 'w')
    output_own = open(args[4], 'w')
    means = []
    stdevs = []

    normalize = 0
    if int(normalize) == 1:
       	row = []	
	dimension = len(training[0]['point'])
	for x in range(0,len(training)):
            row.append(training[x]['point'])
      	means = find_means(row, dimension)
	stdevs = find_st_dev(row, means, dimension)
	for item in range(0,dimension):
            for x in range(0,len(row)):
		row[x][item] = round((row[x][item]-means[item])/stdevs[item],5)
	for x in range(0,len(training)):
            training[x]['point'] = row[x]
    filter(training, output_filter)
#    print "Filter Time :", time.time() - filter_time, " seconds"
#    wrapper_time = time.time()
    remaining_features = list(xrange(len(training[0]['point'])))
    method = "Wrapper method\n"
    wrapper(training, output_wrapper,remaining_features, method)
#    print "Wrapper Time :", time.time()- wrapper_time, " seconds"
#    own_time = time.time()
    method = "Own Method\n"
    own_method(training, output_own, method)
#    print "Own Time: ", time.time() - own_time, " seconds"

def own_method(training, output_own, method):
    correlations = []                                                        
    order = []          
    threshold = 0.3                                
    for item in range(0,len(training[0]['point'])):    
	correlations.append(correlation(training,item))                     
	find_order = list(correlations)                                       
    for item in range(0,len(correlations)):                                    
        maximum = max(find_order)
	if maximum > threshold:
            order.append(find_order.index(maximum))
            find_order[order[item]] = -1
    wrapper(training, output_own, order, method)
def wrapper(training, output_wrapper, remaining_features, method):
    text = method
    text += "Iteration 0, Selected Features : {} LOOCV Accuracy: 0/"
    text += str(len(training))
    text += "\n"
    output_wrapper.write(text)

    total_dimension = len(remaining_features)
    added_features = []

    incorrect = len(training)
    iteration = 1
    while incorrect >= 0:
#        print "Iteration: ", iteration
        incorrect = wrapper_helper(training,output_wrapper,incorrect, added_features,remaining_features,iteration)
        iteration = iteration +1 
#    print remaining_features
#    print added_features

def wrapper_helper(training, output_wrapper, incorrect, added_features, remaining_features,iteration):
    sums = []
    for columnnums in range(0,len(remaining_features)):
        sum = 0
        total = 0
        columns = []
        columns = copy.deepcopy(added_features)
        columns.append(remaining_features[columnnums])
#        print columnnums
        for item in range(0,len(training)):
            new_training = []
#            print "omitting " 
#            print item
            for x in range(0,len(training)):
                store_row = []
                for columnrange in range(0,len(columns)):
                  #  print training[x]['point'][columns[columnrange]]
                    store_row.append(training[x]['point'][columns[columnrange]])
                new_training.append({
                     'point' : store_row,
                     'class' : int(training[x]['class'])
                })
            x = new_training.pop(item)
#            if item == 3:
#                print x
#                print training[item]
            t = kdtree(new_training)
            dimensions = len(new_training[0]['point'])
            testpoint = []
            for columnrange in range(0,len(columns)):
                testpoint.append(training[item]['point'][columns[columnrange]])
                testpoint.append(int(training[item]['class']))
#            if item == 3:
#                print testpoint
            class_test = testpoint.pop()
            place = testpoint
            knn = chooseBest(getNeighbors(dimensions,t,place,7,[]))
            total = total + 1
            if int(knn) == int(class_test):
                sum = sum +1
#        print sum
        sums.append(sum)
#    print sums
    if len(sums) == 0:
	return -1
    maximum = max(sums)
#    print "total-maximum : ", total-maximum
#    print "incorrect :" ,incorrect
    if incorrect > (total - maximum):
        added_features.append(sums.index(max(sums)))
        remaining_features.pop(sums.index(max(sums)))
        text = "Iteration "
        text += str(iteration)
        text += " Selected Features : { "
        for value in range(0,len(added_features)):
            num = int(added_features[value])
            num = num + 1
            text += str(num)
            text += " "
        text += "} LOOCV Accuracy: "
        text += str(max(sums))
        text += "/"
        text += str(total)
        text += "\n"
        output_wrapper.write(text)
        return total-maximum
    elif (total-maximum) >= incorrect:
#        print "Final Incorrect: ", incorrect
        return -1


# Don't touch below the line!!
#######################################################
#######################################################

def filter(training,output_filter):
    correlations = []
    order = []
    for item in range(0,len(training[0]['point'])):
        correlations.append(correlation(training,item))
    find_order = list(correlations)
    for item in range(0,len(correlations)):
        maximum = max(find_order)
        order.append(find_order.index(maximum))
        find_order[order[item]] = -1
#    print order
    text = "Filter Method\n"
    text += "Part A: Features listed in descending order according to the |r| value\n"
    output_filter.write(text)
    for item in range(0,len(correlations)):
        text = "Feature "
        text += str(order[item]+1)
        text += " has an |r| of "
        text += str(correlations[order[item]])
        text += str('\n')
        output_filter.write(text)
    text = "\nPart B: Values of m and Avg LOOCV accuracy\n"
    output_filter.write(text)
    for columnnums in range(0,len(order)):
#        print "Iteration: ", columnnums

        sum = 0
	total = 0
        columns = []
        for y in range(0,columnnums+1):
            columns.append(order[y])

#        print columns
        #Loop over all data
        for item in range(0,len(training)):
            new_training = []
#            print item
        #Leave out this data point(item)    
            for x in range(0,len(training)):
                store_row = []
                for columnrange in range(0,len(columns)):
                    store_row.append(training[x]['point'][order[columnrange]])
                new_training.append({
                    'point' : store_row,
                    'class' : int(training[x]['class'])
                })
            x =new_training.pop(item)
#            print x
            t = kdtree(new_training)
            dimensions = len(new_training[0]['point'])
            testpoint = []
            for columnrange in range(0,len(columns)):
                testpoint.append(training[item]['point'][order[columnrange]])
                testpoint.append(int(training[item]['class']))
            class_test = testpoint.pop()
            place = testpoint
            knn = chooseBest(getNeighbors(dimensions,t,place,7,[]))
            total = total+1
            if int(knn) == int(class_test):
                sum = sum + 1
        text = "M: "
        text += str(columnnums+1)
        text += ", LOOCV Accuracy: "
        text += str(sum)
        text += "/"
        text += str(total)
        text += ", "
        text += str(round(float(sum)*100/float(total),1))
        text += "% Correctly Classified\n"
        output_filter.write(text)
def avg_h(neighbors):
    # pulls out average of all sqdists
    accum = 0
    for neighbor in neighbors :
        accum += neighbor['sqdist']
    return accum / len(neighbors)

def chooseBest(neighbors):
    i = 0
    classes = {}
    # build dictionary : classes are keys, values are lists
    # of relevant neighbors 
    for neighbor in neighbors :
        class_name = neighbor['class']
        if not class_name in classes :
            classes[class_name] = [neighbor]
        else :
            classes[class_name].append(neighbor)
    
    # find key value pair with best length of relative neighbors
    # manage ties with average closeness
    bestavg = float('inf')
    bestcount = 0
    for class_name, neighbors in classes.iteritems():
        if len(neighbors) > bestcount :
            bestclass = class_name
            bestcount = len(neighbors)
            bestavg = avg_h(neighbors) 
        elif len(neighbors) == bestcount:
            accum = 0
            avg = avg_h(neighbors) 
            if avg < bestavg :
                bestavg = avg
                bestclass = class_name
    return bestclass

def kdtree(pointlist):
    k = len(pointlist[0]['point'])
    # initial bounds start at -inf -> +inf on all axes
    bounds = [{'min':-float('inf'),'max':float('inf')} for axis in range(k)]
    return kdtree_assist(k, pointlist, bounds, 0)

def kdtree_assist(k, pointlist, bounds, depth):
    if len(pointlist) == 0 : 
        # empty obj as leaves
        return {}

    axis = depth % k; # rotate through axis as descending through tree

    # sort points, split on median
    pl = sorted(pointlist, key=lambda x: x['point'][axis])
    if len(pl) == 1 : 
        medianIndex = 0
    else :
        medianIndex = (len(pl) + 1) / 2;
    median = pl[medianIndex]
    left   = pl[:medianIndex]
    right  = pl[medianIndex + 1:]

    # generate boundary regions for children
    l_bounds = copy.deepcopy(bounds)
    l_bounds[axis]['max'] = median['point'][axis] 
    r_bounds = copy.deepcopy(bounds)
    r_bounds[axis]['min'] = median['point'][axis] 

    # build node of tree around the median
    node = {
        'axis'      : axis,
        'point'     : median['point'],
        'class'     : median['class'],
        'l'         : kdtree_assist(k,left, l_bounds, depth + 1),
        'r'         : kdtree_assist(k,right,r_bounds, depth + 1),
        'bounds'    : bounds
    }

    return node


def getNeighbors(k,tree, point,num, neighbors):
    # contract, neighbors is sorted by furthest to closest
    if not tree : 
        return
    rsearched = False
    lsearched = False
    if not neighbors : #no elements in list
        if tree['r'] and point[tree['axis']] > tree['point'][tree['axis']]:
            rsearched = True
            neighbors = getNeighbors(k,tree['r'],point,num,neighbors)
        elif tree['l'] and point[tree['axis']] > tree['point'][tree['axis']] :
            lsearched = True
            neighbors = getNeighbors(k, tree['l'], point,num, neighbors)

    # check self for better neighborhood if within hypersphere
    # neighbors only added to list in this case
    if len(neighbors) < num or neighbors[0]['sqdist'] >=  eu_sq(k, point, tree['point']) :
        addneighbor(num, neighbors, {
            'point' : tree['point'],
            'class' : tree['class'],
            'sqdist'   : eu_sq(k, point, tree['point'])
        })

    # search right subtree
    if not rsearched and tree['r'] and \
            neighbors[0]['sqdist'] >= region_dist(tree['r'], point) :
        neighbors = getNeighbors(k, tree['r'],point, num, neighbors)

    # search left subtree
    if not lsearched and tree['l'] and \
            neighbors[0]['sqdist'] >= region_dist(tree['l'], point) :
        neighbors = getNeighbors(k, tree['l'],point, num, neighbors)
    return neighbors

def addneighbor(num, neighbors, newneighbor):
    # adds neighbor to neighbors list
    # keeps length of neighbors less than or equal to num unless there's a tie
    # keeps neighbors sorted largest to smallest distance from considered point 
    count = len(neighbors)
    i = 0
    while i < count and neighbors[i]['sqdist'] > newneighbor['sqdist']:
        i += 1
    
    neighbors.insert(i,newneighbor)
    count += 1

    if count <= num :
        return neighbors

    i = 1
    while i < count and neighbors[i-1]['sqdist'] == neighbors[i]['sqdist']:
        # count the number tied at the front of the list
        i += 1
    
    if count - i >= num :
        # remove tied if they alone bring the count above num
        while i > 0 :
            neighbors.pop(0)
            i -= 1
    return neighbors

def eu_sq(k,p1,p2):
    # returns euclidian distance squared
    d = 0
    for dimension in range(k):
        d += (p1[dimension] - p2[dimension])**2
    return d


def region_dist(region, point):
    # distance between a point and the closest point in the boundary region
    bounds = region['bounds']
    closest_point = []
    for dimension in range(len(bounds)):
        if point[dimension] < bounds[dimension]['min'] :
            closest_point.append(bounds[dimension]['min'])
        elif point[dimension] > bounds[dimension]['max'] :
            closest_point.append(bounds[dimension]['max'])
        else :
            closest_point.append(point[dimension])
    return eu_sq(len(bounds), point, closest_point)


main(sys.argv)

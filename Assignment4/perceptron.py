#!/usr/bin/python

import sys
import arff
import copy
import string

def find_eta(args):
    for item in range(0,len(args)):
        if args[item] == "-eta":
            return float(args[item+1])

def get_training(training_file):
    training = []
    for row in arff.load(training_file):
        row = list(row)
	training.append({
	   'class' : int(row.pop()),
	   'point' : row
	})
    return training

def find_means(row, dimension):
    means = []
    for item in range(0,dimension):
	sum = 0
	for x in range(0,len(row)):
            sum = sum + row[x][item]
	mean = round(float(sum/len(row)),5)
	means.append(mean)
    return means

def find_st_devs(row, means, dimension):
    stdevs = []
    for item in range(0, dimension):
	sqdev = 0
	for x in range(0,len(row)):
            sqdev = sqdev + (row[x][item] - means[item])**2
	var = sqdev/(len(row)-1)
	stdevs.append(round((sqdev/(len(row)-1))**0.5,5))
    return stdevs

def main(args):
    eta = find_eta(args)
    training = get_training(args[3])
    test = get_training(args[4])

    # Number of initialization cycles
    initialization = 500

    # Initialize training data
    row_training = []
    dimension = len(training[0]['point'])
    for x in range(0,len(training)):
	row_training.append(training[x]['point'])
    means = find_means(row_training, dimension)
    stdevs = find_st_devs(row_training, means, dimension)

    for item in range(0,dimension):
	for x in range(0,len(row_training)):
            row_training[x][item] = round((row_training[x][item]- \
					means[item])/stdevs[item],5)

    for x in range(0,len(training)):
	training[x]['point'] = row_training[x]

    for x in range(0,len(row_training)):
	row_training[x].append(1.0)

    # Initialize test data
    row_test = []
    for x in range(0,len(test)):
	item = list(test[x]['point'])
	row_test.append(item)

    for item in range(0,dimension):
	for x in range(0,len(row_test)):
            row_test[x][item] = round((row_test[x][item] - \
				  means[item])/stdevs[item],5)

    for x in range(0,len(row_test)):
	row_test[x].append(1.0)
    
    #Initialize Weights - Final weight is the intercept
    weights = []
    for weight in range(0,dimension+1):
	weights.append(0.0)

    weights = train_data(training, eta, row_training, initialization, weights)
    test_data(test, row_test, weights, args, means, stdevs)
    
def test_data(test, row_test, weights, args, means, stdevs):

    output = open(args[5], 'w')
    header = open(args[4], 'r')

    sgn = lambda x: (x>0)-(x<0)
    
    for line in header:
	if line[0] == '@' or line[0] == '%' or line[0] == '\n':
            output.write(line)            

    for x in range(0,len(test)):
	for item in range(0,len(test[x]['point'])):
            output.write(str(test[x]['point'][item]) + ',')
        output.write(str(sgn(inner_product(row_test, x, weights))) + '\n')
	

def train_data(training, eta, row, initialization, weights):
    
    sgn = lambda x: (x>0)-(x<0)

    for count in range(0,initialization):
	for x in range(0,len(training)):
            o = sgn(inner_product(row, x, weights))
            t = sgn(training[x]['class'])
            for item in range(0,len(weights)):
	    	weights[item] = weights[item] + eta*(t-o)*row[x][item]
    return weights

def inner_product(row, x, weights):
    sum = 0
    for item in range(0,len(weights)):
        sum = sum + weights[item]*row[x][item]
    return sum

main(sys.argv)

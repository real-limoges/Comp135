#!/usr/bin/python

import copy
import arff
from math import exp
from math import ceil
import sys
from random import randrange

# Opens the ARFF data file and reads into memory
def get_data(data_file):                               
    unlabeled = []                                
    for row in arff.load(data_file) :             
        row = list(row)                          
        unlabeled.append({                          
            'class' : int(row.pop()),                                          
            'point' : row,
	    'cert'  : float(0)
        })                           
    return unlabeled

# Finds the kNN; calls voting_unlabeled to have the certainty calculated
def kNN(training, unlabeled, k, sigma, classes):
    for item in range(0,len(unlabeled)):
        point = unlabeled[item]
    	distances = []
    	kNN = []
    	for train_point in range(0,len(training)):
		dist = distance(point, training[train_point])
		list_dist = [dist,train_point]
    		distances.append(list_dist)
    	for neighbor in range(0,k):
		minimum = distances.pop(distances.index(min(distances)))
		kNN.append(minimum)
    	unlabeled[item]['cert'] = voting_unlabeled(kNN, training, point, sigma, classes)

# for the kNN it calculates the votes for each. returns the difference
# between the first and second place vote (the certainty)
def voting_unlabeled(kNN, training, point, sigma, classes):
    votes = []
    for item in range(0,classes):
	votes.append(0)
    for neighbor in range(0,len(kNN)):
	x = kNN[neighbor][1]
	num = -1*(kNN[neighbor][0]**2)
	dem = 2*(sigma**2)
	vote = exp(float(num/dem))
	votes[training[x]['class']] = votes[training[x]['class']] + vote
    max1 = votes.pop(votes.index(max(votes)))
    max2 = votes.pop(votes.index(max(votes)))
    return (max1-max2)

# Finds the Euclidean distance between the unlabeled and labeled points
def distance(point, train_point):
    sqs = 0
    for x in range(0,len(point['point'])):
	sqs = sqs + (point['point'][x] - train_point['point'][x])**2
    return sqs**0.5

# Requests m additional labels from the dataset.  If there are less than
# m unlabeled points remaining, it labels the remainder
def request(unlabeled, training, m):
    if len(unlabeled) < m:
	m = len(unlabeled)
    for req in range(0,m):
    	cert = []
    	for item in range(0,len(unlabeled)):
		cert.append(unlabeled[item]['cert'])
    	minimum = cert.index(min(cert))
    	cert.pop(cert.index(min(cert)))
    	training.append(unlabeled.pop(minimum))

# Randomly pops off V instances from the data read in to serve as the
# validation set
def create_validation(unlabeled, V):
    validation = []
    for item in range(0,V):
	random_index = randrange(0,len(unlabeled))
    	validation.append(unlabeled.pop(random_index))
    return validation

# Randomly pops off k/classes points from each class, after the validation
# data is created
def create_training(unlabeled, k, classes):
    training = []
    per_class = int(ceil(float(k)/float(classes)))
    for class_label in range(0,classes):
	x = 0
	while x < per_class:
            random_index = randrange(0,len(unlabeled))
            if unlabeled[random_index]['class'] == class_label:
                training.append(unlabeled.pop(random_index))
            	x = x +1 
    return training

# finds the kNN of the validation test set. calls function to write to
# file the accuracy of the validation set on the training set.
def kNN_validation(validation, train_set, output_file, classes, sigma, k):
    sum = 0
    for item in range(0,len(validation)):  
        point = validation[item]
        distances = []                                                         
        kNN = []                                                        
        for train_point in range(0,len(train_set)):   
            dist = distance(point, train_set[train_point])                   
            list_dist = [dist,train_point]                                  
            distances.append(list_dist)                                     
        for neighbor in range(0,k):                                            
            minimum = distances.pop(distances.index(min(distances)))        
            kNN.append(minimum)                                             
	vote = voting_validation(point, kNN, classes, sigma, train_set)
    	sum = sum + vote
    sum = float(sum)/float(len(validation))*100
    sum = round(sum, 1)
    output_file.write(str(sum))
        
# finds the voting of the kNN for the validation dataset. Returns 1 if
# the vote has the same class as the true class.  Returns 0 otherwise
def voting_validation(vld_pt, kNN, classes, sigma, train_set):
    votes = []
    for item in range(0,int(classes)):
	votes.append(0)
    for neighbor in range(0,len(kNN)):
	x = kNN[neighbor][1]
	num = -1*(kNN[neighbor][0]**2)
	dem = 2*(sigma**2)
	vote = exp(float(num/dem))
    	votes[train_set[x]['class']] = votes[train_set[x]['class']] + vote
    max1 = votes.index(max(votes))
    if vld_pt['class'] == max1:
	return 1
    else:
	return 0

# Preprocesses the data to to have the classes be next to each other
def preprocess(filename, unlabeled):
    if filename == 'Ionosphere.arff':
	for item in range(0, len(unlabeled)):
            unlabeled[item]['class'] = unlabeled[item]['class'] -1 
    else:
	for item in range(0, len(unlabeled)):
		if unlabeled[item]['class'] == 1:
			unlabeled[item]['class'] = 0
		elif unlabeled[item]['class'] == 3:
			unlabeled[item]['class'] = 1
		elif unlabeled[item]['class'] == 5:
			unlabeled[item]['class'] = 2
		elif unlabeled[item]['class'] == 7:
			unlabeled[item]['class'] = 3
		elif unlabeled[item]['class'] == 8:
			unlabeled[item]['class'] = 4


# Writes the header for the output files
def initial_write(x, y, output_u, output_r, k):
    s = "K = " + str(k) + '\n\n' + "Number of Labeled Instances: " + '\n'
    while x > 0:
	if x < 5:
            y = y + x
            x = 0
            s = s + str(y)
    	else:
            y = y + 5
            x = x - 5
            s = s + str(y) + ", "
    s = s + '\n\n'
    output_u.write(s)
    output_r.write(s)
# Runs the uncertainty sampling routine
def uncertainty_sampling(training, validation, unlabeled, sigma, classes, output_u, k, m , item):
    s = "Trial " + str(item + 1) + ": "
    output_u.write(s)
    #Loop through unlabeled and add to training until empty
    while len(unlabeled) >0:
	kNN(training, unlabeled, k, sigma, classes)
	request(unlabeled, training, m)
	kNN_validation(validation, training, output_u, classes, sigma, k)
	if len(unlabeled) != 0:
            output_u.write(", ")
    output_u.write('\n\n')

# Runs the random sampling routine
def random_sampling(training_random, validation, unlabeled_random, sigma, classes, output_r, k, m, item):
	s = "Trial " + str(item + 1) + ": "
	output_r.write(s)
	while len(unlabeled_random) > 0:
            request(unlabeled_random, training_random,  m)
            kNN_validation(validation, training_random, output_r, classes, sigma, k)
            if len(unlabeled_random) != 0:
		output_r.write(", ")
        output_r.write('\n\n')

# Main Function.
def main(args):
    k = int(args[2])
    m = 5

    output_u = open(args[4], 'w')
    output_r = open(args[5], 'w')

    # Data Preprocessing
    if args[3] == 'Ionosphere.arff':
	classes = 2
	sigma = 3.0
	V = 40

    elif args[3] == 'ecoli.arff':
	classes = 5
	sigma = 0.75
	V = 70

    unlabeled = get_data(args[3])
    preprocess(args[3], unlabeled)

    validation = create_validation(unlabeled, V)
    training = create_training(unlabeled, k, classes)
    unlabeled_random = copy.deepcopy(list(unlabeled))
    training_random = copy.deepcopy(list(training))

    initial_write(len(unlabeled), len(training), output_u, output_r, k)

    for item in range(0,10):
	if item != 0:
            for y in range(0, len(validation)):
            	x = validation.pop()
            	x['cert'] = 0.0
            	unlabeled.append(x)
            for y in range(0,len(training)):
            	x = training.pop()
            	x['cert'] = 0.0
            	unlabeled.append(x)
            unlabeled_random = []
            training_random = []

            validation = create_validation(unlabeled, V)
            training = create_training(unlabeled, k, classes)
            unlabeled_random = copy.deepcopy(list(unlabeled))
            training_random = copy.deepcopy(list(training))
	uncertainty_sampling(training, validation, unlabeled, sigma, classes, output_u, k, m, item)
   	random_sampling(training_random, validation, unlabeled_random, sigma, classes, output_r, k, m, item)

main(sys.argv)

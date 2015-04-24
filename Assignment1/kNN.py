# Benjamin Limoges
# Comp 135 : Assignment 1
# January 22, 2014
#
# Notes: I have hard coded the names of the plant types in the code, as well
# as places on lists that I wanted to loop over.
# On future assignments, I will utilize the liac-arff reader (I didn't
# install it until after I had finished coding this assignment)


#Import different packages
import sys
import math

def main():
    # Global Variables
    training = []
    test = []
    types = []
    output = open(sys.argv[3], 'w')

    #Executes code
    header(output)
    loadin(training, 1)
    loadin(test, 2)
    execute_kNN(training, test, output)
    output.closed

# This function takes the header off of training data file and writes
# it to an output file - "output.arff"

def header(output):
    # Intermediate Storage Variables
    data_dump = []

    # Read in data - Write the header for output.arff
    readin = open(sys.argv[1], 'r')

    for line in readin:
    	if line[0] == '@' or line[0] == '%' or line[0] == '\n':
	       output.write(line)

# This function takes in a global data storage (list) and loads the
# data into memory - this function loads both the training and test data

def loadin(data, num):
    # Intermediate Storage Variables
    data_dump = []
    # Read in data - Write the header for output.arff
    readin = open(sys.argv[num], 'r')

    for line in readin:
    	if line[0] != '@' and line[0] != '%' and line[0] != '\n':
	    data_dump.append(line)

    # Remove data from intermediate storage into final storage
    count_data_dump = len(data_dump)

    for i in range(0,len(data_dump)):
    	#Splits imput
    	data_pull = data_dump[i].split(',')

	#Removes the \n from the end of lines
    	remove_end_line  = data_pull[len(data_pull)-1].split('\n')
    	data_pull[len(data_pull)-1] = remove_end_line[0]

	#Appends to data
    	data.append([])
    	data[i] = data_pull

    for i in range(0, len(data_dump)):
    	for j in range(0, 4):
	    data[i][j]= float(data[i][j])


# Executes the kNN file and write the output to "output.arff"
def execute_kNN(training, test, output):

    for item in range(0,len(test)):
    	for x in range(0, len(test[item])):
	    write_me = str(test[item][x])
	    output.write(str(test[item][x]) + ',')
        for k in range(1,10,2):
    		output.write(kNN(training, test[item], k))
		x= kNN(training, test[item],k)
		if k != 9 :
		    output.write(',')
	output.write('\n')
	
# Loops over the different values of k for each test_item
# Calls function to determine the closest neighbors (voters)
# Computes the unweighted vote, returns value as string

def kNN(training, test_item, k):
    voters = []
    initial_k(training, test_item, voters, k)
    farthest = find_max(voters)
    for item in range(0, len(training)):
    	distance = find_distance(training[item], test_item)
    	if farthest > distance:
	        update_voters(distance, training[item][4], voters, farthest)
        farthest = find_max(voters)
    return voting(voters)   


# Determines the initial voters (the first k elements)
# Finds the distances of the initial voters
# Voters list will be a 2D array of eligible voters by distance[0] and
# type[1]

def initial_k(training, test_item, voters, k):
    for i in range(0,k):
	voters.append([])
	voters[i].append(find_distance(training[i],test_item))
	voters[i].append(find_type(training[i]))


# Updates the list of voting eligible by iterating through the remainder
# of the training data. Calls function to replace if there is a lesser
# distance than the largest distance in the eligible voter list

def update_voters(distance, type, voters, farthest):
    for item in range(0,len(voters)):
    	if(voters[item][0] == farthest):
            voters[item][0] = distance
	    voters[item][1] = type

# This function is run after the updating of the "voting" eligible candidates
# have been selected. This function looks at their type and then classifies
# them
# Names have been hard coded

def voting(voters):
    types = [0,0,0]
    names = ['versicolor', 'virginica', 'setosa']
    for item in range(0,len(voters)):
    	for name in range(0,len(types)):
	    if voters[item][1] == names[name]:
	       types[name] = types[name] + 1

    maximum_votes = max(types)
    count_max = 0
    for item in range(0,len(types)):
    	if types[item] == maximum_votes:
	   count_max = count_max + 1

    if count_max == 1:
       for item in range(0,len(types)):
       	   if maximum_votes == types[item]:
	      return names[item]
    else:
	return tiebreaker(types, names, voters, maximum_votes)

# Finds the potential tie breakers. Breaks tie by computing the sum of
# distance for each type. Returns the type that has the minimum amount
# If two or more have the same vote count and the same distance, then
# return the first minimum distance, maxiumum voting candidate in the
# order of the list

def tiebreaker(types, names, voters, maximum_votes):
    identify_tie_type = []
    distances = []
    for item in range(0, len(types)):
    	 if types[item] == maximum_votes:
	    identify_tie_type.append(names[item])
	    distances.append(0)

    for item in range(0, len(identify_tie_type)):
    	for voter in range(0,len(voters)):
	    if voters[voter][1] == identify_tie_type[item]:
	       distances[item] = distances[item] + voters[voter][0]

    minimum = min(distances)

    # Loop returns the first minimum distance
    for item in range(0, len(distances)):
    	if distances[item] == minimum:
	   return identify_tie_type[item]

# Finds the maximum value in the voters list.  Returns this value

def find_max(voters):
    max = voters[0][0]
    for item in range(1,len(voters)):
    	if (max < voters[item][0]):
	   max = voters[item][0]
    return max


# Finds the Euclidean distance from the test_point to the trained_point
# To make the distance formula more readable, x will be the point from
# the training data, and y will be the point from the test line

def find_distance(x, y):
    return round(((x[0]-y[0])**2 + (x[1]-y[1])**2 + (x[2]-y[2])**2 +
    	        (x[3]-y[3])**2 )**(0.5),5)

# Takes in the training data line and returns the "type"
# Mimics finding the distance.  Assumes the type is always in
# index 4

def find_type(x):
    return x[4]

# Executes the code
main()

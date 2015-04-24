#!/usr/bin/python

import arff
import sys
import math
import copy

def get_training(training_file):
    training = []
    for row in arff.load(training_file):
        row = list(row)
        training.append({
            'class' : -1,
            'point' : row
        })
    return training

def get_instances(instance_file):
    file = open(instance_file,'r')
    instances = []
    for line in file:
        instances.append(int(line))
    instances.reverse()
    return instances
        

def find_means(training,dimension):
    means = []
    for item in range(0,dimension):
        sum = 0
        for x in range(0,len(training)):
            sum = sum + training[x]['point'][item]
        sum = float(sum)/float(x)
        means.append(round(sum,5))
    return means

def find_st_dev(training,means,dimension):
    stdevs = []
    for item in range(0,dimension):
        sqdev = 0
        for x in range(0,len(training)):
            sqdev = sqdev + (training[x]['point'][item]-means[item])**2
        std = (sqdev/(len(training)-1))**0.5
        stdevs.append(round(std,5))
    return stdevs
        

def find_distance(test_point, k_means):
    distances = []
    for k in range(0,len(k_means)):
        sumsq = 0
        for attribute in range(0,len(k_means[k])):
            sumsq = sumsq + (k_means[k][attribute] - test_point[attribute])**2
        distances.append(round(sumsq,5))
    return distances.index(min(distances))


def find_clusters(k,training,instances):
    k_indexes = []
    k_means = []
    for x in range(0,k):
        item = instances.pop()
        item = item -1
        k_indexes.append(item)
    for x in range(0,len(k_indexes)):
        k_means.append(training[k_indexes[x]]['point'])
    return k_means

def update_clusters(training, k_means):
    for k in range(0,len(k_means)):
        updated_cluster = []
        for item in range(0,len(training[0]['point'])):
            updated_cluster.append(0)

        count = 0
        for item in range(0,len(training)):
            if training[item]['class'] == k:
                count = count+ 1
            for attribute in range(0,len(training[0]['point'])):
                if int(training[item]['class']) == k:
                    updated_cluster[attribute] = updated_cluster[attribute] + training[item]['point'][attribute]

        for attribute in range(0,len(training[0]['point'])):
            updated_cluster[attribute] =  round(updated_cluster[attribute]/float(count),5)
        k_means[k] = updated_cluster

def main(args):
    training = get_training(args[1])
    output = open(args[2], 'w')
    dimension = len(training[0]['point'])
    means = find_means(training,dimension)
    stdevs= find_st_dev(training,means,dimension)
    for x in range(0,len(training)):
        for item in range(0,dimension):
            training[x]['point'][item] = round((training[x]['point'][item] - means[item])/(stdevs[item]),5)
    for k in range(1,17):
        k_clusters(training,k, output,means,stdevs)

def sse_calc(training,k_means):
    sses = []
    for attribute in range(0,len(k_means)):
        sses.append(0.0)
    
    for item in range(0,len(training)):
        class_label = training[item]['class'] - 1
        sses_point = 0.0
        for attribute in range(0,len(training[0]['point'])):
            sses_point = sses_point + (training[item]['point'][attribute] - k_means[class_label][attribute])**2
        sses[class_label] = sses[class_label] + sses_point
    return round(sum(sses),5)
        

def k_clusters(training, k, output, means, stdevs):
    str1 = "k = " + str(k) + '\n'
    output.write(str1)
    instances = get_instances('instances.txt')
    sse = []
    runs = []
    for x in range(0,25):
        sse.append(0)
        for item in range(0,len(training)):
            training[item]['class'] = -1
        errors = 0
        previous_errors = len(training)
        k_means = find_clusters(k,training,instances)
        for iteration in range(0,50):
            for item in range(0,len(training)):
                class_label = find_distance(training[item]['point'],k_means)
                if class_label != training[item]['class']:
                    errors = errors + 1
                    training[item]['class'] = class_label
            if k == 1:
                runs.append(k_means)
                sse[x] = sse_calc(training,k_means)
                break
            elif previous_errors > errors or iteration == 0:
                update_clusters(training,k_means)
#                print "Updating Clusters"
#                print "There were : ", errors, " errors"
            else:
                runs.append(k_means)
                sse[x] = sse_calc(training,k_means)
                break
            previous_errors = errors
            errors = 0
    best = sse.index(min(sse))
    runs1 = copy.deepcopy(runs)
    for cluster in range(0,len(runs[best])):
        for attribute in range(0,len(runs1[best][0])):
            runs1[best][cluster][attribute] = round(((runs1[best][cluster][attribute])*stdevs[attribute] + means[attribute]),5)

    for item in range(0,len(runs[best])):
        str1 = "Cluster " + str(item+1) + " "
        output.write(str1)
        for x in range(0,len(runs[best][0])):
            runs1[best][item][x] = str(runs1[best][item][x])
        str1 = " ".join(runs1[best][item])
        output.write(str1)
        output.write('\n')
    output.write('\n')

#    print k
#    mean_k = float(sum(sse))/float(len(sse))
#    print mean_k, " mean"
#    sqdev = 0
#    for item in range(0,len(sse)):
#        sqdev = sqdev + (sse[item] - mean_k)**2
#    print (sqdev/(float(len(sse))-1))**0.5, " standard deviation"
    

main(sys.argv)

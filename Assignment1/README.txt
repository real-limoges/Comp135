Benjamin Limoges
Project 1

How to Run the File:

bash RUNME.sh

What the File Does:

The bash RUNME script runs a command line argument to run the kNN.py file
and passes 3 files into the kNN script.

The kNN script reads in training data, stores it, and then uses that
information to implement the kth nearest neighbor algorithm. The kNN script
then opens the test data, and tests for each point the nearest kth neighbor
for k = 1,3,...,9. It does so by a majority, nonweighted vote. 

If there is a tie, the minimum distance is computed between the tied types. 
If after a majority vote and minimum distance comparison there is still a tie, 
the first eligible voter when looping over the eligible voters will be used.

kNN then outputs the file in ARFF format; the name of the file generated is the
third of the files passed into kNN from the command line.

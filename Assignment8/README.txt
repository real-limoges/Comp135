Benjamin Limoges
Assignment 8

python knn.py -k K <datafile> <output1> <output2>

Where K is a positive odd integer

Where <datafile> is either 'ecoli.arff' or 'Ionosphere.arff'.  Files *must* be
named these file names.

<output1>, <output2> are file names for the output



knn.py

Reads in <datafile> to memory.  Randomly selects |V| instances as the
validation set.  Then it selects ceil(k/#number of classes) for the dataset
as a training set (label known). All other datapoints are unlabeled.

Runs knn on training set. Each unlabeled point has a certainty value calculated
on its K nearest neighbors that drops off with distance (weighted vote).
Certainty is the difference between the highest voted class and second highest.

Requests of size m are made for those with the lowest certainty value.  These
are popped off the unlabeled set into the training set (where the label is
allowed to be used). Validation set is then tested and this is the accuracy
reported.  This is repeated until the unlabeled pool is equal to 0.

Repeats the above with the same validation and original training but randomly
pops off m instances (no weighted vote).  Accuracy is tested against the
validation set.

knn.py repeats the above process 10 times and outputs the uncertainty sampling
to <output1> and random sampling to <output2>.  Output is (percent correct)*100
rounded to 1 decimal point.  Therefore 70.3% is written as 70.3

Note: To run this program in its entirety (k = 3,5,7,9,11) with both datasets
takes about 33 minutes.  Each run takes about 3 minutes (for k = 3, Ionosphere
for instance).

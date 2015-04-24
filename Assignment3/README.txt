Benjamin Limoges
Project 2

How to Run the File:

bash RUNME.sh

What the File Does:

The bash RUNME script runs a command line argument to run the preprocess.py
file, which passes two files into the preprocess script (train.arff and 
test.arff).

The preprocess script pre-processes the data to be used in Weka to build the
decision trees.  The script creates three output files: test_processed.arff
train_simple.arff, and train_complex.arff. Each of these is described below:

1. train_simple.arff takes the train.arff file, strips the header off, and then
loops through the data. '?' values (missing values) are replaced with the
simple mean of the attribute, regardless of class label.  No other pieces
of the file are changed.

2. train_complex.arff takes the train.arff file, similarily strips the header 
off, and then loops through the data. '?' values are replaced with the mean of
the class label - i.e. data points with a '?' and a class label of '1' are
replaced with the mean of the attribute for those data points with label
of '1'.  The file is then written; no other pieces of the file are changed.

3. test_processed.arff takes the test.arff file, strips off the header, and
loops through the data.  '?' are replaced with the simple mean across all
class labels for that attribute from the *train.arff* file.  The file is then
written; no othe rpieces of the file are changed.

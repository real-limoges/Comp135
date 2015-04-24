Benjamin Limoges
Assignment 4

While I have programmed in Python, I did create a shell script to run.  
To run the script:

bash RUNME.sh

----Kth Nearest Neighbor----

It runs for all 32 implementation.  For the 24 kth nearest neighbor
implementations, it runs the file in the following manner:

python knn.py -k <int> -Z <bool> <dataset>_train_<version>.arff <dataset>_test_<version>.arff <dataset>_knn_<version>_<normalization>_<option>

Where <dataset> is the dataset (sonar or vertebrate)
Where <version> is either noise or nonoise
Where <option> is the k value
Where <normalization> is either normalized data or non-normalized.
Where -k is a flag for the k in the kth nearest neighbor

Where -Z is a flag for normalization.  0 is no normalization, 1 is
normalization. Normalization is a standard Z-Score normalization.

Note: -k and -Z can have their order reversed. The training, test, and output
files may not have their order switched, and must come after the flags.


The kth nearest neighbor file is a modified version of the class solution
from Assignment 1.  I have commented which functions are my additional
functions. The script reads in the training data, performs normalization
if necessary, and trains on the data.  It then reads in the test data and
tests with the appropriate k provided by the user in the command line
argument.

When completed, it outputs to a file, in the format given above. The file
contains the original data from the test file (non-normalized), but the class
label has been removed and replaced with the predicted class label.


----Perceptron----

python perceptron.py -eta <float> <dataset>_train_<version>.arff <dataset>_test_<version>.arff <dataset>_perceptron_<version>_<option>

Where <dataset> and <version> are the same as kth nearest neighbor.

Where <option> in the case of perceptron is the learning rate, or the 
same as <float>

where -eta is a flag for the learning rate (or the eta) for the program

Program must be run as specified above.


The perceptron.py file is an original file of the perceptron learning
algorithm. It uses stochastic gradient descent to minimize the error. It reads
the learning rate and the training data.  It then normalizes the training data
It iterates through the training data 500 times, each time updating the weights
on each feature. When the weights are updated, it is dependent on the learning
rate provided to the function. After 500 iterations are completed, it then reads in the test data which it normalizes from the mean and standard deviation 
from the training dataset.

It then predicts the class of the test set.  It writes the original test data
to an output file, without the true class label. Instead the predicted
class label is output to the file.

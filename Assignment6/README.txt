Benjamin Limoges
Assignment 6

*********************************
*********************************
IMPORTANT NOTE:

My implementation is really slow (~13 hours). I made a mistake in
deep copying my data structure each time I build a tree.  I tried
to remove this issue, but it caused errors in other places in my
code. I spoke to Rishit about this, and he asked me to flag this in my
README.

I'm terribly sorry I'm abusing the "no time requirement" of this
assignment. I *swear* it converges (I have run it on homework.cs.tufts.edu
multiple times and it did converge each time.) 
Naturally I suggest running it as a background task.

I have provided my output for my assignment so you can check it ahead of time
(and then run it to assure that you get the same results) to hasten the
grading process.

Again, I'm so sorry that my program is shoddy!
********************************
*******************************

Run Program:

python knn.py biodegrade.arff output_filter output_wrapper output_own

General Notes:

I have 1 indexed the Feature List, as this is how the ARFF file is structured.
Therefore if I say Feature 1 has a correlation of x, I mean to say that
the first feature read in from the biodegrade dataset has a correlation
of x. There does not exist a feature 0.

Methodology:

*************
Filter Method:

Takes file that has been read in and computes the Pearson correlation
coefficient, p. It then computes the ordering that the filter method should
follow. The ordering is to start with m = 1 features. The feature selected
first has the highest value of |p|. It then builds a tree without the n=0
data point with only one feature; it tests the tree with the n=0 datapoint.
It then iterates through leaving each data point out.

It then selects the m = 2 features with the highest |p| (where the first
is the one from above).  It does the same cross validation.

Filter method prints the |p| values to file.  It also prints the accuracy
for each of the m feature filters.

**************
Wrapper Method:

Uses data that has already been read in.  Starts with an empty set of 
features, with accuracy 0. It then tests to see what the best feature
to add is; it tests this by exhaustively testing each feature and using
the feature that contributes the most number of accurate classifications.

If there is a tie in the number of accurate responses, the feature with the
lowest index is returned.

Ends if the marginal feature adds no additional correct classifications.

Writes the iterations out to file in the format specified in the assignment.

*************
Own Method:

Recognizing that the above two methods are computationally intractable in
my implementation, I've tried preprocessing my data.  I first take the
dataset and calculate the correlations. Typically a moderate amount of 
correlation is anywhere between 0.3 and 0.7, so I will threshold the
correlation to 0.3.  Features with correlation of less than 0.3 will be
not be considered.

I then implement the wrapper method on these features and select features
that reduce the most errors until it terminates when the next feature
does not increase accuracy.

START=$(date +%s)

for i in 3 5 7 9 11
do
	python knn.py -k $i Ionosphere.arff output_u_I_$i output_r_I_$i
	echo "I did Ionosphere $i"
	python knn.py -k $i ecoli.arff output_u_e_$i output_r_e_$i
	echo "I did ecoli $i"
done

END=$(date +%s)
echo "Total Time"
echo $((END-START)) | awk '{print int($1/60)"m "int($1%60)"s"}'
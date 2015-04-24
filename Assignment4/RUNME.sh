python knn.py -Z 0 -k 1 sonar_train_nonoise.arff sonar_test_nonoise.arff sonar_knn_nonoise_unnormalized_1
python knn.py -Z 0 -k 3 sonar_train_nonoise.arff sonar_test_nonoise.arff sonar_knn_nonoise_unnormalized_3
python knn.py -Z 0 -k 5 sonar_train_nonoise.arff sonar_test_nonoise.arff sonar_knn_nonoise_unnormalized_5

python knn.py -Z 1 -k 1 sonar_train_nonoise.arff sonar_test_nonoise.arff sonar_knn_nonoise_normalized_1
python knn.py -Z 1 -k 3 sonar_train_nonoise.arff sonar_test_nonoise.arff sonar_knn_nonoise_normalized_3
python knn.py -Z 1 -k 5 sonar_train_nonoise.arff sonar_test_nonoise.arff sonar_knn_nonoise_normalized_5

python knn.py -Z 0 -k 1 sonar_train_noise.arff sonar_test_noise.arff sonar_knn_noise_unnormalized_1
python knn.py -Z 0 -k 3 sonar_train_noise.arff sonar_test_noise.arff sonar_knn_noise_unnormalized_3
python knn.py -Z 0 -k 5 sonar_train_noise.arff sonar_test_noise.arff sonar_knn_noise_unnormalized_5

python knn.py -Z 1 -k 1 sonar_train_noise.arff sonar_test_noise.arff sonar_knn_noise_normalized_1
python knn.py -Z 1 -k 3 sonar_train_noise.arff sonar_test_noise.arff sonar_knn_noise_normalized_3
python knn.py -Z 1 -k 5 sonar_train_noise.arff sonar_test_noise.arff sonar_knn_noise_normalized_5

python knn.py -Z 0 -k 1 vertebrate_train_nonoise.arff vertebrate_test_nonoise.arff vertebrate_knn_nonoise_unnormalized_1
python knn.py -Z 0 -k 3 vertebrate_train_nonoise.arff vertebrate_test_nonoise.arff vertebrate_knn_nonoise_unnormalized_3
python knn.py -Z 0 -k 5 vertebrate_train_nonoise.arff vertebrate_test_nonoise.arff vertebrate_knn_nonoise_unnormalized_5

python knn.py -Z 1 -k 1 vertebrate_train_nonoise.arff vertebrate_test_nonoise.arff vertebrate_knn_nonoise_normalized_1
python knn.py -Z 1 -k 3 vertebrate_train_nonoise.arff vertebrate_test_nonoise.arff vertebrate_knn_nonoise_normalized_3
python knn.py -Z 1 -k 5 vertebrate_train_nonoise.arff vertebrate_test_nonoise.arff vertebrate_knn_nonoise_normalized_5

python knn.py -Z 0 -k 1 vertebrate_train_noise.arff vertebrate_test_noise.arff vertebrate_knn_noise_unnormalized_1
python knn.py -Z 0 -k 3 vertebrate_train_noise.arff vertebrate_test_noise.arff vertebrate_knn_noise_unnormalized_3
python knn.py -Z 0 -k 5 vertebrate_train_noise.arff vertebrate_test_noise.arff vertebrate_knn_noise_unnormalized_5

python knn.py -Z 1 -k 1 vertebrate_train_noise.arff vertebrate_test_noise.arff vertebrate_knn_noise_normalized_1
python knn.py -Z 1 -k 3 vertebrate_train_noise.arff vertebrate_test_noise.arff vertebrate_knn_noise_normalized_3
python knn.py -Z 1 -k 5 vertebrate_train_noise.arff vertebrate_test_noise.arff vertebrate_knn_noise_normalized_5

python perceptron.py -eta 0.01 sonar_train_nonoise.arff sonar_test_nonoise.arff sonar_perceptron_nonoise_0.01
python perceptron.py -eta 0.01 sonar_train_noise.arff sonar_test_noise.arff sonar_perceptron_noise_0.01

python perceptron.py -eta 0.001 sonar_train_nonoise.arff sonar_test_nonoise.arff sonar_perceptron_nonoise_0.001
python perceptron.py -eta 0.001 sonar_train_noise.arff sonar_test_noise.arff sonar_perceptron_noise_0.001

python perceptron.py -eta 0.01 vertebrate_train_nonoise.arff vertebrate_test_nonoise.arff vertebrate_perceptron_nonoise_0.01
python perceptron.py -eta 0.01 vertebrate_test_noise.arff vertebrate_test_noise.arff vertebrate_perceptron_noise_0.01

python perceptron.py -eta 0.001 vertebrate_train_nonoise.arff vertebrate_test_nonoise.arff vertebrate_perceptron_nonoise_0.001
python perceptron.py -eta 0.001 vertebrate_train_noise.arff vertebrate_test_noise.arff vertebrate_perceptron_noise_0.001

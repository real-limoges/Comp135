import sys

def main():
    output_train_simple = open('train_simple.arff', 'w')
    output_train_complex = open('train_complex.arff', 'w')
    output_test = open('test_processed.arff', 'w')

    header(sys.argv[1], output_train_simple)
    header(sys.argv[1], output_train_complex)
    header(sys.argv[2], output_test)

    train_simple = []
    train_complex = []
    test_processed = []

    loadin(sys.argv[1], train_simple)
    loadin(sys.argv[1], train_complex)
    loadin(sys.argv[2], test_processed)

    mean = simple_mean(train_simple)
    simple_replace(train_simple, mean, output_train_simple)
    simple_replace(test_processed, mean, output_test)

    mean_1 = complex_mean(train_complex,1)
    mean_2 = complex_mean(train_complex,2)
    complex_replace(train_complex, mean_1, mean_2, output_train_complex)

# Removes the header of the appropriate training sets

def header(data_source, output):
    readin = open(data_source, 'r')
    for line in readin:
        if line[0] == '@' or line[0] == '%' or line[0] == '\n':
            output.write(line)

# Loads the data into memory. Parses the arff file into python lists

def loadin(data_source, data):
    data_dump = []
    readin = open(data_source, 'r')

    for line in readin:
        if line[0] != '@' and line[0] != '%' and line[0] != '\n':
            data_dump.append(line)

    for i in range(0, len(data_dump)):
        data_pull = data_dump[i].split(',')
        remove_end_line = data_pull[len(data_pull)-1].split('\n')
        data_pull[len(data_pull)-1] = remove_end_line[0]

        data.append([])
        data[i] = data_pull

# Calculates the simple mean for the entire dataset (omitting '?')
# Returns this value as a float rounded to 5 decimal places

def simple_mean(data):
    numerator = 0
    denominator = 0

    for i in range(0, len(data)):
        if data[i][2] != '?':
            numerator = numerator + float(data[i][2])
            denominator = denominator + 1

    return round(numerator/float(denominator),5)


# Writes the simple mean (used for the simple training and the test file)
# in any place where there is a '?'

def simple_replace(data, mean, output):
    for i in range(0,len(data)):
        if data[i][2] == '?':
            data[i][2] = mean
    
    write_to_file(data, output)

# Calculates a simple mean for a specific passed argument
# I'm unsure how to overload functions in python so I just created a
# seperate function

def complex_mean(data, num):
    numerator = 0
    denominator = 0

    for i in range(0, len(data)):
        if data[i][2] != '?' and int(data[i][3]) == num: 
            numerator = numerator + float(data[i][2])
            denominator = denominator + 1
    return round(numerator/float(denominator), 5)

# Replaces the complex data

def complex_replace(data, mean_1, mean_2, output):
    for i in range(0, len(data)):
        if data[i][2] == '?' and int(data[i][3]) == 1:
            data[i][2] = mean_1
        elif data[i][2] == '?' and int(data[i][3]) == 2:
            data[i][2] = mean_2

    write_to_file(data, output)

# Writes the final output to the designated file

def write_to_file(data,output):
    for item in range(0, len(data)):
        for x in range(0, len(data[item])):
            output.write(str(data[item][x]))
            if x != len(data[item])-1:
                output.write(',')
            else:
                output.write('\n')
main()


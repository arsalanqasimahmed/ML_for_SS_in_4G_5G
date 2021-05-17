
# use with data generated by "prog_A_cyclicRes.m" program

import numpy as np
import re
from bunch import Bunch
from sklearn.cluster import KMeans
from decimal import *
import matplotlib.pyplot as plt

def frange(start, stop, step):
    i = start
    while i <= stop:
        yield i
        i += step


SNR_tab = frange(-40, -40, 1)


# loop for every SNR value
for SNR in SNR_tab:
    print("\nIteration for SNR = {}".format(SNR))

    if SNR - int(SNR) == 0:
        SNR_2 = int(SNR)
    else:
        SNR_2 = SNR

    if SNR < 0:
        file_name1 = "data_" + str(abs(SNR_2)) + ".txt"
        file_name2 = "data_" + str(abs(SNR_2)) + "_test.txt"
    else:
        file_name1 = "data" + str(SNR_2) + ".txt"
        file_name2 = "data" + str(SNR_2) + "_test.txt"

    folder_name = "C:/Users/User/Desktop/Habib Resources/Final Year Project/5G Data/Bandwidth Parts"

    print("opening file named: " + file_name1)
    file_object1 = open(folder_name+"/"+file_name1, "r")
    d = file_object1.readlines()

    count_line = 0
    for line in d:
        if not len(line.strip()) == 0:
            count_line += 1

    print("number of lines: {}".format(count_line))

    print("opening file named: " + file_name2)
    file_object2 = open(folder_name+"/"+file_name2, "r")
    d2 = file_object2.readlines()

    count_line2 = 0
    for line in d2:
        if not len(line.strip()) == 0:
            count_line2 += 1

    print("number of lines: {}".format(count_line2))

    f_array1 = np.zeros(count_line)
    t_array1 = np.zeros(count_line)
    occ_array1 = np.zeros(count_line)


    f_array2 = np.zeros(count_line2)
    t_array2 = np.zeros(count_line2)
    occ_array2 = np.zeros(count_line2)


    # reading data from files to arrays
    ind = 0
    for line in d:
        if not len(line.strip()) == 0:
            words = line.split()
            f_array1[ind] = words[0]
            t_array1[ind] = int(words[1]) % 80
            occ_array1[ind] = words[2]
            ind += 1

    ind = 0
    for line in d2:
        if not len(line.strip()) == 0:
            words = line.split()
            f_array2[ind] = words[0]
            t_array2[ind] = int(words[1]) % 80
            occ_array2[ind] = words[2]
            ind += 1

    file_object1.close()
    file_object2.close()

    # creating training data sets


    lte_dataset_train= Bunch()
    # Storing data in numpy arrays
    lte_dataset_train['data'] = np.array([f_array1, t_array1]).T
    lte_dataset_train['target'] = np.array(occ_array1).T
    lte_dataset_train['target_names'] = ['free', 'occupied']


    # creating testing data sets

    lte_dataset_test = Bunch()
    # Storing data in numpy arrays
    lte_dataset_test['data'] = np.array([f_array2, t_array2]).T 
    lte_dataset_test['target'] = np.array(occ_array2).T
    lte_dataset_test['target_names'] = ['free', 'occupied']


    X_train = lte_dataset_train['data']
    y_train = lte_dataset_train['target']
    X_test = lte_dataset_test['data']
    y_test = lte_dataset_test['target']



    # implementing kMeans Clustering Algorithm
    for k in range(10):
        print("Running K Means for iteration: ", k)
        kmeans = KMeans(n_clusters = 6, random_state = 0).fit(X_train)
        clusters = kmeans.predict(X_train)
        centroids = kmeans.cluster_centers_

    
        print("Cluster Centroids: ", centroids)
        print("labels: ", kmeans.labels_)
        zero, one, two, three, four, five = 0,0,0,0,0,0
        for i in kmeans.labels_:
            if i == 0:
                zero +=1
            elif i == 1:
                one += 1
            elif i == 2:
                two += 1
            elif i == 3:
                three += 1
            elif i == 4:
                four += 1
            else:
                five += 1
                
                
        numer = [16*5,32*5,64*5]
        labels = [zero,one,two,three, four, five]
        lst = [[0, zero], [1, one], [2, two], [3, three]]
        print("Total Bandwidth part 0 resource blocks: ", zero)
        print("Total Bandwidth part 1 resource blocks: ", one)
        print("Total Bandwidth part 2 resource blocks: ", two)
        print("Total Bandwidth part 3 resource blocks: ", three)
        print("Total Bandwidth part 4 resource blocks: ", four)
        print("Total Bandwidth part 5 resource blocks: ", five)
        
   
        num0 = []
        num1 = []
        num2 = []
        for i in numer:
            for j in range(len(labels)):
                if int(labels[j]//i) == 1:
                    if i == 16*5 and labels[j] == 16*5:
                       num2 = np.concatenate((num2, np.where(clusters == j)), axis = None)
                    elif i == 32*5 and labels[j] == 32*5:
                        num1 = np.concatenate((num1, np.where(clusters == j)), axis = None)
                    else:
                        num0 = np.concatenate((num0, np.where(clusters == j)), axis = None)
                        
                        
        num0 = num0.astype('int')
        num1 = num1.astype('int')
        num2 = num2.astype('int')
        for i in lst:
            if i[1] == 16:
                i.append('num2')
            elif i[1] == 32:
                i.append('num1')
            else:
                i.append('num0')

        for i in num0:
            plt.scatter(X_train[i,1], X_train[i,0], marker = 'x', c = 'red')
  
        for i in num1:
            plt.scatter(X_train[i,1], X_train[i,0], marker = 'x', c = 'blue')

        for i in num2:
            plt.scatter(X_train[i,1], X_train[i,0], marker = 'x', c = 'green') 

    
        plt.scatter(centroids[:,1], centroids[:,0], marker = 'o')
        plt.xlim([0,80])
        plt.ylim([0,150])
        plt.xlabel("time slot")
        plt.ylabel("frequency")
        plt.title("Detecting Numerologies through K-Means (Gaussian)")
    
        plt.show()




# end (for SNR in SNR_tab)

file_results.close()
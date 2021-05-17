
# use with data generated by "prog_A_cyclicRes.m" program

import numpy as np
import re
from bunch import Bunch
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import Perceptron
from sklearn.neural_network import MLPClassifier
from decimal import *
import tensorflow as tf

np.set_printoptions(threshold=np.inf)
def frange(start, stop, step):
    i = start
    while i <= stop:
        yield i
        i += step


SNR_tab = frange(-40, 20, 1)

# this file will keep results for every SNR
file_results = open("results_ANN_ED_numerology0.txt", "w")

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

    folder_name = "C:/Users/User/Desktop/Habib Resources/Final Year Project/5G Data/Numerology 0/ED (scattered grid and users 20)"

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
    dcs_array1 = np.zeros(count_line)
    wall_nghbrs1 = np.zeros(count_line)
    corner_nghbrs1 = np.zeros(count_line)
    ff_data1 = np.zeros(count_line)


    f_array2 = np.zeros(count_line2)
    t_array2 = np.zeros(count_line2)
    t_array_f = np.zeros(count_line2)
    occ_array2 = np.zeros(count_line2)
    dcs_array2 = np.zeros(count_line2)
    wall_nghbrs2 = np.zeros(count_line2)
    corner_nghbrs2 = np.zeros(count_line2)
    ff_data2 = np.zeros(count_line2)


    # reading data from files to arrays
    ind = 0
    for line in d:
        if not len(line.strip()) == 0:
            words = line.split()
            f_array1[ind] = words[0]
            t_array1[ind] = int(words[1]) % 80
            occ_array1[ind] = words[2]
            dcs_array1[ind] = words[3]
            wall_nghbrs1[ind] = words[4]
            corner_nghbrs1[ind] = words[5]
            ff_data1[ind] = words[7]
            ind += 1

    ind = 0
    for line in d2:
        if not len(line.strip()) == 0:
            words = line.split()
            f_array2[ind] = words[0]
            t_array2[ind] = int(words[1]) % 80
            t_array_f[ind] = words[1]
            occ_array2[ind] = words[2]
            dcs_array2[ind] = words[3]
            wall_nghbrs2[ind] = words[4]
            corner_nghbrs2[ind] = words[5]
            ff_data2[ind] = words[7]
            ind += 1

    file_object1.close()
    file_object2.close()

    # creating training data sets


    lte_dataset_train= Bunch()
    # choose energy detection data or energy values data
    lte_dataset_train['data'] = np.array([f_array1, t_array1, dcs_array1, wall_nghbrs1, corner_nghbrs1, ff_data1]).T # Energy detection only
    lte_dataset_train['target'] = np.array(occ_array1).T
    lte_dataset_train['target_names'] = ['free', 'occupied']


    # creating testing data sets

    lte_dataset_test = Bunch()
    # choose energy detection data or energy values data
    lte_dataset_test['data'] = np.array([f_array2, t_array2, dcs_array2, wall_nghbrs2, corner_nghbrs2, ff_data2]).T # energy detection only
    lte_dataset_test['target'] = np.array(occ_array2).T
    lte_dataset_test['target_names'] = ['free', 'occupied']


    X_train = lte_dataset_train['data']
    y_train = lte_dataset_train['target']
    X_test = lte_dataset_test['data']
    y_test = lte_dataset_test['target']


    #Implementing Artificial Neural Network

    clf = MLPClassifier(solver='adam', alpha=1e-5,
                   hidden_layer_sizes=(10), max_iter = 500, activation = 'relu', random_state=1)
    y = clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    

    print("Accuracy on training set: {:.3f}%".format(100*clf.score(X_train, y_train)))
    print("Accuracy on test set: {:.3f}%".format(100*clf.score(X_test, y_test)))

    det_prob = 0
    al_prob = 0
    n_RB = np.sum(y_test)
    id_y = 0


    for y_p in y_pred[:]:
        if y_p == 1:
            if y_test[id_y] == 1:
                det_prob += 1
            else:
                al_prob += 1
        id_y += 1
    
    det_prob = 100*det_prob / n_RB
    al_prob = 100*al_prob / (id_y-n_RB)
    print("For SNR = {}:".format(SNR))
    print("Probability of detection: {:.3f}%".format(det_prob))
    print("Probability of false alarm: {:.3f}%".format(al_prob))

    res = np.array([det_prob, al_prob, SNR])
    res_str = np.array2string(res, precision=3)
    file_results.write("\n")
    file_results.write(re.sub('[\[\]]', '', res_str))

# end (for SNR in SNR_tab)

file_results.close()
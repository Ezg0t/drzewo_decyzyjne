import math


def loadFile(plik):
    data = [(i.strip('\n')).split(',') for i in open(plik, "r")]
    return data


def quantityOfRepetitions(file):
    results = []
    for i in range(len(file[0])):
        tempDictionary = {}
        results.append(tempDictionary)
        for j in range(len(file)):
            if file[j][i] in results[i]:
                results[i][file[j][i]] += 1
            else:
                results[i][file[j][i]] = 1
    print(results)
    return (results)


def countAttributes(data):
    tempAttributes = []
    temp = [''] * len(data[0])
    attributes = []
    max_quantity_of_attributes = []
    print(len(data))
    print(len(data[0]))
    for i in range(len(data)):
        for j in range(len(data[i])):
            temp = data[i][j] + ' '
            if temp not in temp[j]:
                temp[j] = temp[j] + temp
            if temp not in tempAttributes:
                tempAttributes.append(temp)
    for n in range(len(data[0])):
        attributes.append(tempAttributes[0][n].split())
        max_quantity_of_attributes.append(len(attributes[n]))
    return attributes


def countRepetitions(data, attributes):
    dictionaries_list = []
    dictionary = {}
    for i in range(len(attributes)):
        for j in range(len(attributes[i])):

            dictionary[list(attributes[i].keys())[j]] = 0
            for k in range(len(data)):
                if list(attributes[i].keys())[j] == data[k][i]:
                    dictionary[list(attributes[i].keys())[j]] = dictionary[list(attributes[i].keys())[j]] + 1
        dictionaries_list.append(dictionary.copy())
        dictionary.clear()
    print(dictionaries_list)
    return dictionaries_list


def probability_of_occurence(dictonaries_list, max):
    temp_propabolities_list = []
    propabolities_list = []
    for i in range(len(dictonaries_list)):
        for j in range(len(dictonaries_list[i])):
            pomocnicza = 0
            for x in dictonaries_list[i]:
                if pomocnicza == j:
                    sum = ((dictonaries_list[i][x]) / max)
                    temp_propabolities_list.append(sum)
        propabolities_list.append(temp_propabolities_list.copy())
        temp_propabolities_list.clear()
    return propabolities_list


def allEntropies(probability_of_occurence):
    entropies_list = []
    for i in range(len(probability_of_occurence)):
        entropy = 0
        for j in range(len(probability_of_occurence[i])):
            if (probability_of_occurence[i][j]) == 0:
                entropy = 0
            else:
                entropy += (probability_of_occurence[i][j] * math.log2(probability_of_occurence[i][j]))
        entropy *= (-1)
        entropies_list.append(entropy)
    return entropies_list


def information_function(file, occurances, probability_of_occurence, entropy):
    # old
    # a1= 3/10 * I(3/3, 0/3)
    # a1 = a1 + 4/10 * I(2/4, 2/4) + 3/10
    # 3/10 * I(3/3, 0/3) + 4/10 * I(2/4, 2/4) + 3/10 * I(0/3, 3/3)
    information_function_tab_temp = []
    tabTemp = []
    for i in range(len(occurances) - 1):
        for x in occurances[i]:
            slowTemp = {}
            for j in range(len(file)):
                if file[j][i] == x:
                    klucz = (file[j][len(file[j]) - 1])
                    if klucz in slowTemp:
                        slowTemp[klucz] += 1
                    else:
                        slowTemp[klucz] = 1
            tabTemp.append(slowTemp.copy())
        information_function_tab_temp.append(tabTemp.copy())
        tabTemp.clear()
    information_function_tab = []
    information_gain_tab = []

    # print(infotmation_function_tab)

    for i in range(len(information_function_tab_temp)):
        info = 0
        for j in range(len(information_function_tab_temp[i])):
            count = []
            tempTab = []
            for x in information_function_tab_temp[i][j]:
                temp = (information_function_tab_temp[i][j][x] / (sum(information_function_tab_temp[i][j].values())))
                count.append(temp)
            tempTab.append(count)
            info += probability_of_occurence[i][j] * allEntropies(tempTab)[0]
        gainInfo = entropy[-1] - info
        information_gain_tab.append(gainInfo)
        information_function_tab.append(info)
    print("Funkcje informacji (Info): " + str(information_function_tab))
    print("Przyrosty informacji (Gain): " + str(information_gain_tab))
    return information_gain_tab


def balancedGainInfo(information_gain_tab, entropy):
    balanced_information_gain_tab = []
    for x in range(len(information_gain_tab)):
        if entropy[x] != 0:
            temp = information_gain_tab[x] / entropy[x]
        else:
            temp = 0
        balanced_information_gain_tab.append(temp)
    print("Zrównoważone przyrosty informacji (Gain ratio): " + str(balanced_information_gain_tab))
    print(" ")
    return balanced_information_gain_tab


def algorithm(file, visualisation):
    print(" ")
    for row in file:
        print(row)
    print(" ")
    # atrybuty = policzAtrybuty(plik)
    attributes = quantityOfRepetitions(file)
    # [{'old': 3, 'mid': 4, 'new': 3}, {'yes': 4, 'no': 6}, {'swr': 6, 'hwr': 4}, {'down': 5, 'up': 5}]
    occurances = countRepetitions(file, attributes)
    p_of_occurances = probability_of_occurence(occurances, len(file))
    print(p_of_occurances)
    entropy = allEntropies(p_of_occurances)
    print("ENTROPIE:", entropy)
    info = information_function(file, occurances, p_of_occurances, entropy)
    gainInfo = balancedGainInfo(info, entropy)
    max_gain_info = max(gainInfo)
    max_gain_info_index = gainInfo.index(max_gain_info)
    if max_gain_info == 0:
        decision_attribute = str(file[0][-1])
        visualisation['wynik'] = decision_attribute
        print("KONIEC, ATRYBUT DECYZYJNY: " + decision_attribute)
        print("===========================================================================")
        print("===========================================================================")
        print("===========================================================================")
    else:
        print("NAJWYŻSZY GAIN RATIO " + str(max_gain_info) + ' CZYLI DZIELIMY PO ATRYBUCIE A' + str(
            max_gain_info_index + 1))
        print("===========================================================================")
        new_file = divide(file, occurances, max_gain_info_index)

        visualisation[max_gain_info_index + 1] = {}
        visualisationTemp = visualisation[max_gain_info_index + 1]
        print(visualisation)
        for i in range(len(new_file)):
            print(new_file[i][0][max_gain_info_index])
            visualisationTemp[new_file[i][0][max_gain_info_index]] = {}
            algorithm(new_file[i], visualisationTemp[new_file[i][0][max_gain_info_index]])
    return visualisation

def divide(file, occurances, max_gain_info_index):
    segments_tab = []
    for x in occurances[max_gain_info_index]:
        segment = []
        for i in range(len(file)):
            if file[i][max_gain_info_index] == x:
                segment.append(file[i])
        segments_tab.append(segment)
    return segments_tab


def showTree(tree, shift):
    keys = list(tree.keys())
    if len(keys) == 1:
        if keys[0] == "wynik":
            print(tree[keys[0]])
        else:
            print("Atrybut a" + str(keys[0]))
            showTree(tree[keys[0]], shift + 5)
    else:
        for key in keys:
            print(" " * shift, end="")
            print(key, end=" ---> ")
            showTree(tree[key], shift)



file = loadFile('testowaTabDec.txt')
file2 = loadFile('breast-cancer.data')
tree = {}
tree2 = {}
print(algorithm(file, tree))
showTree(algorithm(file2, tree2), 0)

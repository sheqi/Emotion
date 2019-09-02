# codes for co-occurrence matrix for justifying recognition results
import numpy as np
from sklearn.preprocessing import scale
from collections import defaultdict

# result is the string of two items
# result[0] = "human" (e.g. objects)
# result[1] = "wall"  (e.g. context)
# co_mat["wall"]["human"] = number

def scale_fun(value, beta):
    return 2 / (1 + np.exp(- beta * value)) - 1

def mod_2dim_dict(thedict, key_a, key_b):
    beta = 0.7
    if key_a in thedict:
        thedict[key_a].update({key_b: scale_fun(thedict[key_a][key_b], beta)})
    else:
        thedict.update({key_a:{key_b: scale_fun(thedict[key_a][key_b], beta)}})
    return thedict

def add_2dim_dict(thedict, key_a, key_b, val):
    if key_a in thedict:
        thedict[key_a].update({key_b: val})
    else:
        thedict.update({key_a:{key_b: val}})

def co_matrix(result, dict_common, dict_person):

    # query on personal KG first, if not exit, then only query common sense KG
    # query on personal KG first, if exit, then query common sense KG, if exit in common sense, then fuse them
    if result[0] and result[1] in dict_person.keys():
        thedic = mod_2dim_dict(dict_person, result[0], result[1])
        score1 = thedic[result[0]][result[1]]
        if result[0] and result[1] in dict_common.keys():
            score2 = dict_common[result[0]][result[1]]
            if score1 > 0.5 and score2 < 0.2:
                confidence_score = score2
            else:
                confidence_score = 0.5 * score1 + 0.5 * score2
        else:
            confidence_score = score1
    else:
        if result[0] and result[1] in dict_common.keys():
            confidence_score = dict_common[result[0]][result[1]]
        #Todo: adding human supervision
    return confidence_score
    #print("The recognition confidence is", confidence_score)

# test add two dim dic
# mapdict = dict()
#
# addtwodimdict(mapdict, 'Beijing', 'Guangzhou', 1897)
# addtwodimdict(mapdict, 'Chengdu', 'Guangzhou', 1243)
# addtwodimdict(mapdict, 'Guangzhou', 'Shanghai', 1212)
# addtwodimdict(mapdict, 'Beijing', 'Chengdu', 1516)
# addtwodimdict(mapdict, 'Chengdu', 'Shanghai', 1657)
# addtwodimdict(mapdict, 'Beijing', 'Shanghai', 1075)
#
# print('The distance between Chengdu and Guangzhou is ', mapdict['Chengdu']['Guangzhou'])
dict = defaultdict(dict)

# build common sense KG
dict_common = {('obj-69', 'chair'): {('obj-69', 'chair'): 1.0, ('obj-0', 'chair'): 1.0, ('demo_room', 'room'): 0.193, ('obj-63', 'chair'): 1.0}, ('obj-0', 'chair'): {('obj-69', 'chair'): 1.0, ('obj-0', 'chair'): 1.0, ('demo_room', 'room'): 0.193, ('obj-63', 'chair'): 1.0}, ('demo_room', 'room'): {('obj-69', 'chair'): 0.193, ('obj-0', 'chair'): 0.193, ('demo_room', 'room'): 1.0, ('obj-63', 'chair'): 0.193}, ('obj-63', 'chair'): {('obj-69', 'chair'): 1.0, ('obj-0', 'chair'): 1.0, ('demo_room', 'room'): 0.193, ('obj-63', 'chair'): 1.0}}

# build personalized KG
dict_person = {('obj-69', 'chair'): {('obj-69', 'chair'): 0, ('obj-0', 'chair'): 0, ('demo_room', 'room'): 2.0, ('obj-63', 'chair'): 2.0}, ('obj-0', 'chair'): {('obj-69', 'chair'): 0, ('obj-0', 'chair'): 0, ('demo_room', 'room'): 2.0, ('obj-63', 'chair'): 0}, ('demo_room', 'room'): {('obj-69', 'chair'): 2.0, ('obj-0', 'chair'): 2.0, ('demo_room', 'room'): 0, ('obj-63', 'chair'): 2.0}, ('obj-63', 'chair'): {('obj-69', 'chair'): 2.0, ('obj-0', 'chair'): 0, ('demo_room', 'room'): 2.0, ('obj-63', 'chair'): 0}}

# final fusion results

# test for the source and target co-occurrence
print("We have the following relationship for estimating their co-occurrence", dict_person.keys())
print("You can pick for example two of them above for verification")

# a simple test
inquiry = [('obj-63', 'chair'), ('obj-0', 'chair')]
print("When we reason the co-occurrence of", inquiry[0], "and", inquiry[1], "we have")

#co_matrix(inquiry, dict_common, dict_person)
score = []
for i in range(len(inquiry)):
    for j in range(i+1,len(inquiry)):
        score.append(co_matrix([inquiry[i], inquiry[j]], dict_common, dict_person))

print("The recognition confidence is", sum(score)/(len(inquiry)*(len(inquiry)-1))*2)




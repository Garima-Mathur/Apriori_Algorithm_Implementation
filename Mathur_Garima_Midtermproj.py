#!/usr/bin/env python
# coding: utf-8

# **Importing all required Libraries**

# In[1]:


import numpy as np
import pandas as pd
import io
import itertools


# ## **DATASET 1-**

# **Uploading Dataset using filesystem. All Datasets are available in GitHub for convinience.**

# In[19]:


data=pd.read_csv(r"C:\Users\HP\OneDrive\Desktop\DATA_MINING_MIDTERM_PROJECT\Dataset1.csv")


# In[20]:


data.head()


# In[21]:


data.tail()


# **Getting input from the user for the following :**
#  
# **1.Number of Transactions (Max possible value = 20)**
# 
# **2.Maximum items per transactions (Max possible value = 5)**
# 
# **3.Minimum value of support (Min possible value = 20)**
# 
# **4.Minimum confidence value (Maximum possible value =100)**
# 

# In[22]:


No_of_Transactions=int(input("Number of transactions as per database : "))
Maximum_Items=int(input("Maximum items in each transaction as per database : "))

minimum_support_count=float(input("Minimum support value : "))
Minimum_Support= (minimum_support_count/100)*No_of_Transactions

Minimum_Confidence_value=float(input("Minimum_Confidence_value : "))


# **Data processing to create the required records and item-list for further processing.**

# In[23]:


Input_Data = []
for i in range(0, No_of_Transactions):
    Input_Data.append([str(data.values[i,j]) for j in range(0, Maximum_Items)])

print("Input Transactions : ", Input_Data)
items = sorted([item for sublist in Input_Data for item in sublist if item != 'nan'])


# **For k=1 to 4 , candidate_set and the frequent ItemSet are calculated by comparing the support count of each item in the list to the Minimum Support value. We check  if all the subsets in itemset are frequent using the check subset frequency function and if not, we remove respective itemset from the list by comparing the length of the two possible lists using the sublist function.**
# 
# **We are printing all the Item_Sets generated after calculations.**

# In[24]:



# For k=1 , the candidate_set C1 is calculated alongwith Item_set  L1 which is our desired output.

def k_1(items, Minimum_Support):
    candidate_set1 = {i:items.count(i) for i in items}
    Item_set1 = {}
    for key, value in candidate_set1.items():
        if value >= Minimum_Support:
           Item_set1[key] = value 
    
    return candidate_set1, Item_set1

# For k=2 , the candidate_set C2 is calculated alongwith Frequent Item_set  L2 which is calculated by comparing value with Minimum_Support .

def k_2(Item_set1, Input_Data, Minimum_Support):
    Item_set1 = sorted(list(Item_set1.keys()))
    L1 = list(itertools.combinations(Item_set1, 2))
    candidate_set2 = {}
    Item_set2 = {}
    for iter1 in L1:
        count = 0
        for iter2 in Input_Data:
            if sublist(iter1, iter2):
                count+=1
        candidate_set2[iter1] = count
    for key, value in candidate_set2.items():
        if value >= Minimum_Support:
            if check_subset_frequency(key, Item_set1, 1):  
                Item_set2[key] = value 
    
    return candidate_set2, Item_set2

# For k=3 , the candidate_set C3 is calculated alongwith Frequent Item_set  L3 which is calculated by comparing value with Minimum_Support .   
def k_3(Item_set2, Input_Data, Minimum_Support):
    Item_set2 = list(Item_set2.keys())
    L2 = sorted(list(set([item for t in Item_set2 for item in t])))
    L2 = list(itertools.combinations(L2, 3))
    candidate_set3 = {}
    Item_set3 = {}
    for iter1 in L2:
        count = 0
        for iter2 in Input_Data:
            if sublist(iter1, iter2):
                count+=1
        candidate_set3[iter1] = count
    for key, value in candidate_set3.items():
        if value >= Minimum_Support:
            if check_subset_frequency(key, Item_set2, 2):  
                Item_set3[key] = value 
        
    return candidate_set3, Item_set3

# For k=4 , the candidate_set C4 is calculated alongwith Frequent Item_set  L4 which is calculated by comparing value with Minimum_Support . 
def k_4(Item_set3, Input_Data, Minimum_Support):
    Item_set3 = list(Item_set3.keys())
    L3 = sorted(list(set([item for t in Item_set3 for item in t])))
    L3 = list(itertools.combinations(L3, 4))
    candidate_set4 = {}
    Item_set4 = {}
    for iter1 in L3:
        count = 0
        for iter2 in Input_Data:
            if sublist(iter1, iter2):
                count+=1
        candidate_set4[iter1] = count
    for key, value in candidate_set4.items():
        if value >= Minimum_Support:
            if check_subset_frequency(key, Item_set3, 3):    
                Item_set4[key] = value 
        
    return candidate_set4, Item_set4

def sublist(lst1, lst2):
    return set(lst1) <= set(lst2)
    
def check_subset_frequency(itemset, l, n):
    if n>1:    
        subsets = list(itertools.combinations(itemset, n))
    else:
        subsets = itemset
    for iter1 in subsets:
        if not iter1 in l:
            return False
    return True


candidate_set1, Item_set1 = k_1(items, Minimum_Support)
candidate_set2, Item_set2 = k_2(Item_set1, Input_Data, Minimum_Support)
candidate_set3, Item_set3 = k_3(Item_set2, Input_Data, Minimum_Support)
candidate_set4, Item_set4 = k_4(Item_set3, Input_Data, Minimum_Support)
print(" ")
print(" ")
print("Frequent Item set generated when k=1 => ", Item_set1)
print("Frequent Item set generated when k=2 => ", Item_set2)
print("Frequent Item set generated when k=3 => ", Item_set3)
print("Frequent Item set generated when k=4 => ", Item_set4)


itemlist = {**Item_set1, **Item_set2, **Item_set3, **Item_set4}


# **Calculating  the Association rules based on the confidence value.**

# In[25]:


def support_count(itemset, itemlist):
    return itemlist[itemset]

sets = []
for iter1 in list(Item_set3.keys()):
    subsets = list(itertools.combinations(iter1, 2))
    sets.append(subsets)

list_l3 = list(Item_set3.keys())
for i in range(0, len(list_l3)):
    for iter1 in sets[i]:
        a = iter1
        b = set(list_l3[i]) - set(iter1)
        confidence = (support_count(list_l3[i], itemlist)/support_count(iter1, itemlist))*100
        if(confidence >= Minimum_Confidence_value):
          print(" ")
          print(" ")
          print("Association rules generated with their confidence value =>{}->{} = ".format(a,b), confidence)


# ## **DATASET 2 -**

# **Uploading Dataset using filesystem. All Datasets are available in GitHub for convinience.**

# In[26]:


data=pd.read_csv(r"C:\Users\HP\OneDrive\Desktop\DATA_MINING_MIDTERM_PROJECT\Dataset2.csv")


# In[27]:


data.head()


# In[28]:


data.tail()


# **Getting input from the user for the following :**
# 
# **1.Number of Transactions (Max possible value = 20)**
# 
# **2.Maximum items per transactions (Max possible value = 5)**
# 
# **3.Minimum value of support (Min possible value = 20)**
# 
# **4.Minimum confidence value (Maximum possible value =100)**

# In[29]:


No_of_Transactions=int(input("Number of transactions as per database : "))
Maximum_Items=int(input("Maximum items in each transaction as per database : "))

minimum_support_count=float(input("Minimum support value : "))
Minimum_Support= (minimum_support_count/100)*No_of_Transactions

Minimum_Confidence_value=float(input("Minimum_Confidence_value : "))


# **Data processing to create the required records and item-list for further processing.**

# In[30]:


Input_Data = []
for i in range(0, No_of_Transactions):
    Input_Data.append([str(data.values[i,j]) for j in range(0, Maximum_Items)])

print("Input Transactions : ", Input_Data)
items = sorted([item for sublist in Input_Data for item in sublist if item != 'nan'])


# **For k=1 to 4 , candidate_set and the frequent ItemSet are calculated by comparing the support count of each item in the list to the Minimum Support value. We check  if all the subsets in itemset are frequent using the check subset frequency function and if not, we remove respective itemset from the list by comparing the length of the two possible lists using the sublist function.**
# 
# **We are printing all the Item_Sets generated after calculations.**

# In[31]:


# For k=1 , the candidate_set C1 is calculated alongwith Item_set  L1 which is our desired output.

def k_1(items, Minimum_Support):
    candidate_set1 = {i:items.count(i) for i in items}
    Item_set1 = {}
    for key, value in candidate_set1.items():
        if value >= Minimum_Support:
           Item_set1[key] = value 
    
    return candidate_set1, Item_set1

# For k=2 , the candidate_set C2 is calculated alongwith Frequent Item_set  L2 which is calculated by comparing value with Minimum_Support .

def k_2(Item_set1, Input_Data, Minimum_Support):
    Item_set1 = sorted(list(Item_set1.keys()))
    L1 = list(itertools.combinations(Item_set1, 2))
    candidate_set2 = {}
    Item_set2 = {}
    for iter1 in L1:
        count = 0
        for iter2 in Input_Data:
            if sublist(iter1, iter2):
                count+=1
        candidate_set2[iter1] = count
    for key, value in candidate_set2.items():
        if value >= Minimum_Support:
            if check_subset_frequency(key, Item_set1, 1):  
                Item_set2[key] = value 
    
    return candidate_set2, Item_set2

# For k=3 , the candidate_set C3 is calculated alongwith Frequent Item_set  L3 which is calculated by comparing value with Minimum_Support .   
def k_3(Item_set2, Input_Data, Minimum_Support):
    Item_set2 = list(Item_set2.keys())
    L2 = sorted(list(set([item for t in Item_set2 for item in t])))
    L2 = list(itertools.combinations(L2, 3))
    candidate_set3 = {}
    Item_set3 = {}
    for iter1 in L2:
        count = 0
        for iter2 in Input_Data:
            if sublist(iter1, iter2):
                count+=1
        candidate_set3[iter1] = count
    for key, value in candidate_set3.items():
        if value >= Minimum_Support:
            if check_subset_frequency(key, Item_set2, 2):  
                Item_set3[key] = value 
        
    return candidate_set3, Item_set3

# For k=4 , the candidate_set C4 is calculated alongwith Frequent Item_set  L4 which is calculated by comparing value with Minimum_Support . 
def k_4(Item_set3, Input_Data, Minimum_Support):
    Item_set3 = list(Item_set3.keys())
    L3 = sorted(list(set([item for t in Item_set3 for item in t])))
    L3 = list(itertools.combinations(L3, 4))
    candidate_set4 = {}
    Item_set4 = {}
    for iter1 in L3:
        count = 0
        for iter2 in Input_Data:
            if sublist(iter1, iter2):
                count+=1
        candidate_set4[iter1] = count
    for key, value in candidate_set4.items():
        if value >= Minimum_Support:
            if check_subset_frequency(key, Item_set3, 3):    
                Item_set4[key] = value 
        
    return candidate_set4, Item_set4

def sublist(lst1, lst2):
    return set(lst1) <= set(lst2)
    
def check_subset_frequency(itemset, l, n):
    if n>1:    
        subsets = list(itertools.combinations(itemset, n))
    else:
        subsets = itemset
    for iter1 in subsets:
        if not iter1 in l:
            return False
    return True


candidate_set1, Item_set1 = k_1(items, Minimum_Support)
candidate_set2, Item_set2 = k_2(Item_set1, Input_Data, Minimum_Support)
candidate_set3, Item_set3 = k_3(Item_set2, Input_Data, Minimum_Support)
candidate_set4, Item_set4 = k_4(Item_set3, Input_Data, Minimum_Support)
print(" ")
print(" ")
print("Frequent Item set generated when k=1 => ", Item_set1)
print("Frequent Item set generated when k=2 => ", Item_set2)
print("Frequent Item set generated when k=3 => ", Item_set3)
print("Frequent Item set generated when k=4 => ", Item_set4)


itemlist = {**Item_set1, **Item_set2, **Item_set3, **Item_set4}


# **Calculating  the Association rules based on the confidence value.**

# In[32]:


def support_count(itemset, itemlist):
    return itemlist[itemset]

sets = []
for iter1 in list(Item_set3.keys()):
    subsets = list(itertools.combinations(iter1, 2))
    sets.append(subsets)

list_l3 = list(Item_set3.keys())
for i in range(0, len(list_l3)):
    for iter1 in sets[i]:
        a = iter1
        b = set(list_l3[i]) - set(iter1)
        confidence = (support_count(list_l3[i], itemlist)/support_count(iter1, itemlist))*100
        if(confidence >= Minimum_Confidence_value):
          print(" ")
          print(" ")
          print("Association rules generated with their confidence value =>{}->{} = ".format(a,b), confidence)


# ## **DATASET 3 -**

# **Uploading Dataset using filesystem. All Datasets are available in GitHub for convinience.**

# In[33]:


data=pd.read_csv(r"C:\Users\HP\OneDrive\Desktop\DATA_MINING_MIDTERM_PROJECT\Dataset3.csv")


# In[34]:


data.head()


# In[35]:


data.tail()


# **Getting input from the user for the following :**
# 
# **1.Number of Transactions (Max possible value = 20)**
# 
# **2.Maximum items per transactions (Max possible value = 5)**
# 
# **3.Minimum value of support (Min possible value = 20)**
# 
# **4.Minimum confidence value (Maximum possible value =100)**

# In[36]:


No_of_Transactions=int(input("Number of transactions as per database : "))
Maximum_Items=int(input("Maximum items in each transaction as per database : "))

minimum_support_count=float(input("Minimum support value : "))
Minimum_Support= (minimum_support_count/100)*No_of_Transactions

Minimum_Confidence_value=float(input("Minimum_Confidence_value : "))


# **Data processing to create the required records and item-list for further processing.**

# In[37]:


Input_Data = []
for i in range(0, No_of_Transactions):
    Input_Data.append([str(data.values[i,j]) for j in range(0, Maximum_Items)])

print("Input Transactions : ", Input_Data)
items = sorted([item for sublist in Input_Data for item in sublist if item != 'nan'])


# **For k=1 to 4 , candidate_set and the frequent ItemSet are calculated by comparing the support count of each item in the list to the Minimum Support value. We check if all the subsets in itemset are frequent using the check subset frequency function and if not, we remove respective itemset from the list by comparing the length of the two possible lists using the sublist function.**
# 
# **We are printing all the Item_Sets generated after calculations.**

# In[38]:


# For k=1 , the candidate_set C1 is calculated alongwith Item_set  L1 which is our desired output.

def k_1(items, Minimum_Support):
    candidate_set1 = {i:items.count(i) for i in items}
    Item_set1 = {}
    for key, value in candidate_set1.items():
        if value >= Minimum_Support:
           Item_set1[key] = value 
    
    return candidate_set1, Item_set1

# For k=2 , the candidate_set C2 is calculated alongwith Frequent Item_set  L2 which is calculated by comparing value with Minimum_Support .

def k_2(Item_set1, Input_Data, Minimum_Support):
    Item_set1 = sorted(list(Item_set1.keys()))
    L1 = list(itertools.combinations(Item_set1, 2))
    candidate_set2 = {}
    Item_set2 = {}
    for iter1 in L1:
        count = 0
        for iter2 in Input_Data:
            if sublist(iter1, iter2):
                count+=1
        candidate_set2[iter1] = count
    for key, value in candidate_set2.items():
        if value >= Minimum_Support:
            if check_subset_frequency(key, Item_set1, 1):  
                Item_set2[key] = value 
    
    return candidate_set2, Item_set2

# For k=3 , the candidate_set C3 is calculated alongwith Frequent Item_set  L3 which is calculated by comparing value with Minimum_Support .   
def k_3(Item_set2, Input_Data, Minimum_Support):
    Item_set2 = list(Item_set2.keys())
    L2 = sorted(list(set([item for t in Item_set2 for item in t])))
    L2 = list(itertools.combinations(L2, 3))
    candidate_set3 = {}
    Item_set3 = {}
    for iter1 in L2:
        count = 0
        for iter2 in Input_Data:
            if sublist(iter1, iter2):
                count+=1
        candidate_set3[iter1] = count
    for key, value in candidate_set3.items():
        if value >= Minimum_Support:
            if check_subset_frequency(key, Item_set2, 2):  
                Item_set3[key] = value 
        
    return candidate_set3, Item_set3

# For k=4 , the candidate_set C4 is calculated alongwith Frequent Item_set  L4 which is calculated by comparing value with Minimum_Support . 
def k_4(Item_set3, Input_Data, Minimum_Support):
    Item_set3 = list(Item_set3.keys())
    L3 = sorted(list(set([item for t in Item_set3 for item in t])))
    L3 = list(itertools.combinations(L3, 4))
    candidate_set4 = {}
    Item_set4 = {}
    for iter1 in L3:
        count = 0
        for iter2 in Input_Data:
            if sublist(iter1, iter2):
                count+=1
        candidate_set4[iter1] = count
    for key, value in candidate_set4.items():
        if value >= Minimum_Support:
            if check_subset_frequency(key, Item_set3, 3):    
                Item_set4[key] = value 
        
    return candidate_set4, Item_set4

def sublist(lst1, lst2):
    return set(lst1) <= set(lst2)
    
def check_subset_frequency(itemset, l, n):
    if n>1:    
        subsets = list(itertools.combinations(itemset, n))
    else:
        subsets = itemset
    for iter1 in subsets:
        if not iter1 in l:
            return False
    return True


candidate_set1, Item_set1 = k_1(items, Minimum_Support)
candidate_set2, Item_set2 = k_2(Item_set1, Input_Data, Minimum_Support)
candidate_set3, Item_set3 = k_3(Item_set2, Input_Data, Minimum_Support)
candidate_set4, Item_set4 = k_4(Item_set3, Input_Data, Minimum_Support)
print(" ")
print(" ")
print("Frequent Item set generated when k=1 => ", Item_set1)
print("Frequent Item set generated when k=2 => ", Item_set2)
print("Frequent Item set generated when k=3 => ", Item_set3)
print("Frequent Item set generated when k=4 => ", Item_set4)


itemlist = {**Item_set1, **Item_set2, **Item_set3, **Item_set4}


# **Calculating  the Association rules based on the confidence value.**

# In[39]:


def support_count(itemset, itemlist):
    return itemlist[itemset]

sets = []
for iter1 in list(Item_set3.keys()):
    subsets = list(itertools.combinations(iter1, 2))
    sets.append(subsets)

list_l3 = list(Item_set3.keys())
for i in range(0, len(list_l3)):
    for iter1 in sets[i]:
        a = iter1
        b = set(list_l3[i]) - set(iter1)
        confidence = (support_count(list_l3[i], itemlist)/support_count(iter1, itemlist))*100
        if(confidence >= Minimum_Confidence_value):
          print(" ")
          print(" ")
          print("Association rules generated with their confidence value =>{}->{} = ".format(a,b), confidence)


# ## **DATASET 4 -**

# **Uploading Dataset using filesystem. All Datasets are available in GitHub for convinience.**

# In[40]:


data=pd.read_csv(r"C:\Users\HP\OneDrive\Desktop\DATA_MINING_MIDTERM_PROJECT\Dataset4.csv")


# In[41]:


data.head()


# In[42]:


data.tail()


# **Getting input from the user for the following :**
# 
# **1.Number of Transactions (Max possible value = 20)**
# 
# **2.Maximum items per transactions (Max possible value = 5)**
# 
# **3.Minimum value of support (Min possible value = 20)**
# 
# **4.Minimum confidence value (Maximum possible value =100)**

# In[43]:


No_of_Transactions=int(input("Number of transactions as per database : "))
Maximum_Items=int(input("Maximum items in each transaction as per database : "))

minimum_support_count=float(input("Minimum support value : "))
Minimum_Support= (minimum_support_count/100)*No_of_Transactions

Minimum_Confidence_value=float(input("Minimum_Confidence_value : "))


# **Data processing to create the required records and item-list for further processing.**

# In[44]:


Input_Data = []
for i in range(0, No_of_Transactions):
    Input_Data.append([str(data.values[i,j]) for j in range(0, Maximum_Items)])

print("Input Transactions : ", Input_Data)
items = sorted([item for sublist in Input_Data for item in sublist if item != 'nan'])


# **For k=1 to 4 , candidate_set and the frequent ItemSet are calculated by comparing the support count of each item in the list to the Minimum Support value. We check if all the subsets in itemset are frequent using the check subset frequency function and if not, we remove respective itemset from the list by comparing the length of the two possible lists using the sublist function.**
# 
# **We are printing all the Item_Sets generated after calculations.**

# In[45]:


# For k=1 , the candidate_set C1 is calculated alongwith Item_set  L1 which is our desired output.

def k_1(items, Minimum_Support):
    candidate_set1 = {i:items.count(i) for i in items}
    Item_set1 = {}
    for key, value in candidate_set1.items():
        if value >= Minimum_Support:
           Item_set1[key] = value 
    
    return candidate_set1, Item_set1

# For k=2 , the candidate_set C2 is calculated alongwith Frequent Item_set  L2 which is calculated by comparing value with Minimum_Support .

def k_2(Item_set1, Input_Data, Minimum_Support):
    Item_set1 = sorted(list(Item_set1.keys()))
    L1 = list(itertools.combinations(Item_set1, 2))
    candidate_set2 = {}
    Item_set2 = {}
    for iter1 in L1:
        count = 0
        for iter2 in Input_Data:
            if sublist(iter1, iter2):
                count+=1
        candidate_set2[iter1] = count
    for key, value in candidate_set2.items():
        if value >= Minimum_Support:
            if check_subset_frequency(key, Item_set1, 1):  
                Item_set2[key] = value 
    
    return candidate_set2, Item_set2

# For k=3 , the candidate_set C3 is calculated alongwith Frequent Item_set  L3 which is calculated by comparing value with Minimum_Support .   
def k_3(Item_set2, Input_Data, Minimum_Support):
    Item_set2 = list(Item_set2.keys())
    L2 = sorted(list(set([item for t in Item_set2 for item in t])))
    L2 = list(itertools.combinations(L2, 3))
    candidate_set3 = {}
    Item_set3 = {}
    for iter1 in L2:
        count = 0
        for iter2 in Input_Data:
            if sublist(iter1, iter2):
                count+=1
        candidate_set3[iter1] = count
    for key, value in candidate_set3.items():
        if value >= Minimum_Support:
            if check_subset_frequency(key, Item_set2, 2):  
                Item_set3[key] = value 
        
    return candidate_set3, Item_set3

# For k=4 , the candidate_set C4 is calculated alongwith Frequent Item_set  L4 which is calculated by comparing value with Minimum_Support . 
def k_4(Item_set3, Input_Data, Minimum_Support):
    Item_set3 = list(Item_set3.keys())
    L3 = sorted(list(set([item for t in Item_set3 for item in t])))
    L3 = list(itertools.combinations(L3, 4))
    candidate_set4 = {}
    Item_set4 = {}
    for iter1 in L3:
        count = 0
        for iter2 in Input_Data:
            if sublist(iter1, iter2):
                count+=1
        candidate_set4[iter1] = count
    for key, value in candidate_set4.items():
        if value >= Minimum_Support:
            if check_subset_frequency(key, Item_set3, 3):    
                Item_set4[key] = value 
        
    return candidate_set4, Item_set4

def sublist(lst1, lst2):
    return set(lst1) <= set(lst2)
    
def check_subset_frequency(itemset, l, n):
    if n>1:    
        subsets = list(itertools.combinations(itemset, n))
    else:
        subsets = itemset
    for iter1 in subsets:
        if not iter1 in l:
            return False
    return True


candidate_set1, Item_set1 = k_1(items, Minimum_Support)
candidate_set2, Item_set2 = k_2(Item_set1, Input_Data, Minimum_Support)
candidate_set3, Item_set3 = k_3(Item_set2, Input_Data, Minimum_Support)
candidate_set4, Item_set4 = k_4(Item_set3, Input_Data, Minimum_Support)
print(" ")
print(" ")
print("Frequent Item set generated when k=1 => ", Item_set1)
print("Frequent Item set generated when k=2 => ", Item_set2)
print("Frequent Item set generated when k=3 => ", Item_set3)
print("Frequent Item set generated when k=4 => ", Item_set4)


itemlist = {**Item_set1, **Item_set2, **Item_set3, **Item_set4}


# **Calculating  the Association rules based on the confidence value.**

# In[46]:


def support_count(itemset, itemlist):
    return itemlist[itemset]

sets = []
for iter1 in list(Item_set3.keys()):
    subsets = list(itertools.combinations(iter1, 2))
    sets.append(subsets)

list_l3 = list(Item_set3.keys())
for i in range(0, len(list_l3)):
    for iter1 in sets[i]:
        a = iter1
        b = set(list_l3[i]) - set(iter1)
        confidence = (support_count(list_l3[i], itemlist)/support_count(iter1, itemlist))*100
        if(confidence >= Minimum_Confidence_value):
          print(" ")
          print(" ")
          print("Association rules generated with their confidence value =>{}->{} = ".format(a,b), confidence)


# ## **DATASET 5 -**

# **Uploading Dataset from filesystem. All Datasets are available in GitHub for convinience.**

# In[5]:


data=pd.read_csv(r"C:\Users\HP\OneDrive\Desktop\DATA_MINING_MIDTERM_PROJECT\Dataset5.csv")


# In[6]:


data.head()


# In[7]:


data.tail()


# **Getting input from the user for the following :**
# 
# **1.Number of Transactions (Max possible value = 20)**
# 
# **2.Maximum items per transactions (Max possible value = 5)**
# 
# **3.Minimum value of support (Min possible value = 20)**
# 
# **4.Minimum confidence value (Maximum possible value =100)**

# In[8]:


No_of_Transactions=int(input("Number of transactions as per database : "))
Maximum_Items=int(input("Maximum items in each transaction as per database : "))

minimum_support_count=float(input("Minimum support value : "))
Minimum_Support= (minimum_support_count/100)*No_of_Transactions

Minimum_Confidence_value=float(input("Minimum_Confidence_value : "))


# **Data processing to create the required records and item-list for further processing.**

# In[9]:


Input_Data = []
for i in range(0, No_of_Transactions):
    Input_Data.append([str(data.values[i,j]) for j in range(0, Maximum_Items)])

print("Input Transactions : ", Input_Data)
items = sorted([item for sublist in Input_Data for item in sublist if item != 'nan'])


# **For k=1 to 4 , candidate_set and the frequent ItemSet are calculated by comparing the support count of each item in the list to the Minimum Support value. We check if all the subsets in itemset are frequent using the check subset frequency function and if not, we remove respective itemset from the list by comparing the length of the two possible lists using the sublist function.**
# 
# **We are printing all the Item_Sets generated after calculations.**

# In[10]:


# For k=1 , the candidate_set C1 is calculated alongwith Item_set  L1 which is our desired output.

def k_1(items, Minimum_Support):
    candidate_set1 = {i:items.count(i) for i in items}
    Item_set1 = {}
    for key, value in candidate_set1.items():
        if value >= Minimum_Support:
           Item_set1[key] = value 
    
    return candidate_set1, Item_set1

# For k=2 , the candidate_set C2 is calculated alongwith Frequent Item_set  L2 which is calculated by comparing value with Minimum_Support .

def k_2(Item_set1, Input_Data, Minimum_Support):
    Item_set1 = sorted(list(Item_set1.keys()))
    L1 = list(itertools.combinations(Item_set1, 2))
    candidate_set2 = {}
    Item_set2 = {}
    for iter1 in L1:
        count = 0
        for iter2 in Input_Data:
            if sublist(iter1, iter2):
                count+=1
        candidate_set2[iter1] = count
    for key, value in candidate_set2.items():
        if value >= Minimum_Support:
            if check_subset_frequency(key, Item_set1, 1):  
                Item_set2[key] = value 
    
    return candidate_set2, Item_set2

# For k=3 , the candidate_set C3 is calculated alongwith Frequent Item_set  L3 which is calculated by comparing value with Minimum_Support .   
def k_3(Item_set2, Input_Data, Minimum_Support):
    Item_set2 = list(Item_set2.keys())
    L2 = sorted(list(set([item for t in Item_set2 for item in t])))
    L2 = list(itertools.combinations(L2, 3))
    candidate_set3 = {}
    Item_set3 = {}
    for iter1 in L2:
        count = 0
        for iter2 in Input_Data:
            if sublist(iter1, iter2):
                count+=1
        candidate_set3[iter1] = count
    for key, value in candidate_set3.items():
        if value >= Minimum_Support:
            if check_subset_frequency(key, Item_set2, 2):  
                Item_set3[key] = value 
        
    return candidate_set3, Item_set3

# For k=4 , the candidate_set C4 is calculated alongwith Frequent Item_set  L4 which is calculated by comparing value with Minimum_Support . 
def k_4(Item_set3, Input_Data, Minimum_Support):
    Item_set3 = list(Item_set3.keys())
    L3 = sorted(list(set([item for t in Item_set3 for item in t])))
    L3 = list(itertools.combinations(L3, 4))
    candidate_set4 = {}
    Item_set4 = {}
    for iter1 in L3:
        count = 0
        for iter2 in Input_Data:
            if sublist(iter1, iter2):
                count+=1
        candidate_set4[iter1] = count
    for key, value in candidate_set4.items():
        if value >= Minimum_Support:
            if check_subset_frequency(key, Item_set3, 3):    
                Item_set4[key] = value 
        
    return candidate_set4, Item_set4

def sublist(lst1, lst2):
    return set(lst1) <= set(lst2)
    
def check_subset_frequency(itemset, l, n):
    if n>1:    
        subsets = list(itertools.combinations(itemset, n))
    else:
        subsets = itemset
    for iter1 in subsets:
        if not iter1 in l:
            return False
    return True


candidate_set1, Item_set1 = k_1(items, Minimum_Support)
candidate_set2, Item_set2 = k_2(Item_set1, Input_Data, Minimum_Support)
candidate_set3, Item_set3 = k_3(Item_set2, Input_Data, Minimum_Support)
candidate_set4, Item_set4 = k_4(Item_set3, Input_Data, Minimum_Support)
print(" ")
print(" ")
print("Frequent Item set generated when k=1 => ", Item_set1)
print("Frequent Item set generated when k=2 => ", Item_set2)
print("Frequent Item set generated when k=3 => ", Item_set3)
print("Frequent Item set generated when k=4 => ", Item_set4)


itemlist = {**Item_set1, **Item_set2, **Item_set3, **Item_set4}


# **Calculating  the Association rules based on the confidence value.**

# In[11]:


def support_count(itemset, itemlist):
    return itemlist[itemset]

sets = []
for iter1 in list(Item_set3.keys()):
    subsets = list(itertools.combinations(iter1, 2))
    sets.append(subsets)

list_l3 = list(Item_set3.keys())
for i in range(0, len(list_l3)):
    for iter1 in sets[i]:
        a = iter1
        b = set(list_l3[i]) - set(iter1)
        confidence = (support_count(list_l3[i], itemlist)/support_count(iter1, itemlist))*100
        if(confidence >= Minimum_Confidence_value):
          print(" ")
          print(" ")
          print("Association rules generated with their confidence value =>{}->{} = ".format(a,b), confidence)


#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def create_terrorist_code_dict(terrorists):
    result = {}
    for i, ter in enumerate(terrorists):
        result[ter] = i
    return result


# In[3]:


def prepare_graph(data_file):
    # getting data and create graph from it.
    with open(data_file, 'r') as csv_file:
        terrorists = csv_file.readline().strip().split(',')[1:] # get rid of first element which is not relevant
        terrorists_dict = create_terrorist_code_dict(terrorists)
        co_attack_data = [[] for _ in range(len(terrorists))]
        for row in csv_file.readlines():
            ter_data = row.strip().split(',')
            terrorist_index = terrorists_dict[ter_data[0]]
            ter_co_location = ter_data[1:]
            for i, ally in enumerate(ter_co_location):
                if ally == '1' and i != terrorist_index:
                    co_attack_data[terrorist_index].append(i)
    return terrorists, terrorists_dict, co_attack_data


# In[4]:


def calculate_co_attack_group(co_attack_data, terrorist):
    return len(co_attack_data[terrorist])


# In[8]:


terrorists, terrorists_dict, co_attack_data = prepare_graph('BAAD_1M.csv')


# In[43]:


import matplotlib.pyplot as plt

# creating a histogram based on number of co-location of attack
frequencies_co_location_numbers = [len(group) for group in co_attack_data]
hist = plt.hist(frequencies_co_location_numbers, bins=100)
x = plt.xlabel('Co-location attack number')
y = plt.ylabel('Group count')


# In[23]:


count = 0
for terrorist in terrorists:
    if calculate_co_attack_group(co_attack_data, terrorists_dict[terrorist]) == 13:
        count += 1
print(count)


# In[ ]:





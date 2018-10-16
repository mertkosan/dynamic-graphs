#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

nodes = pd.read_csv('data/Madrid/Madrid_Nodes_Public_Version2.csv')
relations = pd.read_csv('data/Madrid/Madrid_Relations_Public_Version2.csv')


# In[6]:


# union of dynamic graph to one static graph

graph = relations.groupby('ID')['Tie_ID'].apply(list).to_dict()
freqs = [len(graph[node]) for node in graph]

import matplotlib.pyplot as plt

histogram = plt.hist(freqs, bins=max(freqs))


# In[7]:


# Build a dynamic graph from Madrid data. Find a k-core for each graph (timestamp) and compare the k-cores, how did they change?


# In[9]:


# Also use build a dynamic graph, calculate (k,r) core for each graph (timestamp) and compare the (k,r) cores, how did they change?
# You need to create a similarity metric between the nodes.


# In[ ]:





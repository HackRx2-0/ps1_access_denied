#!/usr/bin/env python
# coding: utf-8

# In[8]:


import requests
from bs4 import BeautifulSoup
import re
import json


# In[9]:


parent_url="https://www.bajajfinservmarkets.in/discover/"
links_array=[parent_url]
links_map={parent_url:'discover'}
final_data={}


# In[10]:


def get_links_from_page(content):
    soup = BeautifulSoup(content, 'html5lib') 
    clean_html=soup.prettify()
    for link in soup.find_all('a'):
        link_str=link.get('href') or ""
        link_str=link_str.split('?')[0]
        if(len(link_str)>0 and link_str[len(link_str)-1]=='/'):
            link_str=link_str[:len(link_str)-1]
        link_str_name=link_str.split('/')[-1]
        if ('discover/..' not in link_str) and ('https://www.bajajfinservmarkets.in/discover' in link_str) and (link_str_name not in links_map) and (link_str not in links_array):
            links_array.append(link_str)
            links_map[link_str]=link_str_name
            print(links_map)            


# In[11]:


def get_data(content):
    data_dict={}
    soup = BeautifulSoup(content, 'html5lib') 
    table = soup.find('div')
    if(table != None):
        for row in table.findAll('div',attrs = {'class':'parawithrte aem-GridColumn aem-GridColumn--default--12'}):
            raw_header=row.find('h2')
            raw_metadata=" "
            row_metadata=row.findAll('p')
            raw_metadata=raw_metadata.join([str(elem) for elem in row_metadata])
            if(raw_header):
                cleanr = re.compile('<.*?>')
                header = re.sub(cleanr, '', str(raw_header))
                metadata=re.sub(cleanr,'',raw_metadata)
                metadata=clean_string(metadata)
                data_dict[header]={"metadata":metadata}
        for row in table.findAll('div',attrs = {'class':'card-list-component aem-GridColumn aem-GridColumn--default--12'}):
            raw_link_headers=row.findAll('h3')
            raw_link_data=row.findAll('p')
            raw_link=row.findAll('a')
            for i in range(len(raw_link_headers)):
                cleanr = re.compile('<.*?>')
                header = re.sub(cleanr, '', str(raw_link_headers[i]))
                metadata=re.sub(cleanr, '', str(raw_link_data[i]))
                link=str(raw_link[i]).split("href")[1][2:].split('"')[0]
                data_dict[header]={}
                data_dict[header]["metadata"]=metadata
                data_dict[header]["link"]=link
        
    return data_dict

    


# In[12]:


def clean_string(s):
    s=s.replace('\n','')
    cleanr = re.compile('\\*')
    s=re.sub(cleanr,'',s)
    s=s.replace("  ","")
    s.replace('\\','')
    return s[1:]


# In[13]:


def get_pages_data(i):
    if(i>=len(links_array)):
        return
    response = requests.get(links_array[i])
    get_links_from_page(response.content)
    data=get_data(response.content)
    final_data[links_map[links_array[i]]]=data
    get_pages_data(i+1)


# In[ ]:


get_pages_data(0)


# In[ ]:


final_data


# In[ ]:





'''
Created on Jun 7, 2017

@author: admin_user
'''
import xml.etree.ElementTree as ET
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

print ("test file")
dir_name = 'C:/Users/admin_user/data_sets/ASL - Kinect XML'
file_name_list = [f for f in os.listdir(dir_name) if f.endswith('.xml')]
print ("number of files {}".format(len(file_name_list)))

file_list = ['SECRET+_1990', 'SECRET_2_1991']
col_ct = -1
fig = plt.figure()
gs = gridspec.GridSpec(2, 3)
for _file in file_list:
    col_ct += 1
    tree = ET.parse(dir_name+'/'+_file+'.xml')
    root = tree.getroot()
    
#     print (root.tag)
#     print (root.attrib)
#     print (root[0][0][0].tag, root[0][0][0].attrib)
    
    _position = 'ThumbRight'
    row_cnt = 0
    x_data = []
    y_data = []
    z_data = []
    for fm in root.iter('frame'): 
        for row in fm.iter('joint'):
            row_cnt += 1
            if row.attrib['name']==_position:
                print (row_cnt, row.attrib)
                x_data.append(float(row.attrib['x']))
                y_data.append(float(row.attrib['y']))
                z_data.append(float(row.attrib['z']))
    
#     print (len(x_data))
#     print (len(y_data))
#     print (len(z_data))
    
    plot_ct = -1
    time_data = np.linspace(0,3,len(x_data))        # assuming 3 secs per sample
    plot_ct += 1
    plt.subplot(gs[col_ct,plot_ct])
    plt.plot(time_data, x_data)
    plt.title(_file+'_'+_position+'_'+'x_component', fontsize = 8)
    
    plot_ct += 1
    plt.subplot(gs[col_ct,plot_ct])
    plt.plot(time_data, y_data)
    plt.title(_file+'_'+_position+'_'+'y_component', fontsize = 8)
    
    plot_ct += 1
    plt.subplot(gs[col_ct,plot_ct])
    plt.plot(time_data, z_data)
    plt.title(_file+'_'+_position+'_'+'z_component', fontsize = 8)
    


plt.show()

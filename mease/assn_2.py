# -*- coding: utf-8 -*-
"""
Created on Mon May 20 13:43:46 2019

@author: Srikanth
"""

from common import *

data = pd.read_csv(os.path.join(data_dir, 'more_stats202_logs.csv'), header=None, names=['ip', 'data'])

ip_x = '65.57.245.11'
data_x = 'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.3) Gecko/20070309 Firefox/2.0.0.3'

support_ip = data['ip'].value_counts()[ip_x]

# Unneeded
# support_data = data['data'].value_counts()[data_x]

support_combined = len(data[data['ip'] == ip_x][data['data'] == data_x])


support_rule = support_combined / len(data)
confidence_rule = support_combined / support_ip
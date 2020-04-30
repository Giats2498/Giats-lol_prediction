# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 20:56:07 2020

@author: Giats
"""
import riot_scraper as rs
server_names = ['eun1','na1','euw1','kr','tr1','jp1']

for server in server_names:
    rs.get_stats('RGAPI-1abff89a-295c-4b7d-b518-f1644504b421',server,['challengerleagues','grandmasterleagues','masterleagues'])
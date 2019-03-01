'''
Created on Mar 1, 2019

@author: Daniel Procopio
'''

import requests
import json
import datetime

class oci_status():
    '''
    Deserialization of https://ocistatus.oraclecloud.com/api/v2/summary.json
    '''
    _page = {}
    _components = []
    _incidents = []
    _scheduled_maintenances = []
    _services = []
    _services_regions_status = []
    _global_status = ''
    _last_update_date = ''
    
    def __init__(self, region, service):
        '''
        Constructor
        '''
        
        url = 'https://ocistatus.oraclecloud.com/api/v2/summary.json'
        resp = requests.get(url)
        data = json.loads(resp.content.decode('utf-8'))
        self._get_status_objects(data, region, service)
        
    def _get_status_objects(self, data, reg, svc):
        '''
        Move data into specific variables
        '''

        self._page = data['page']
        self._incidents = data['incidents']
        self._scheduled_maintenances = data['scheduled_maintenances']
        self._global_status = data['status']['description']
        # self._last_update_date = datetime.datetime.strptime(data['page']['updated_at'],'%Y-%m-%dT%H:%M:%S.%f%z').strftime('%Y-%m-%d %H:%M:%S (%z)')
        self._last_update_date = data['page']['updated_at']
        
        for component in data['components']:
            '''
            Checking whether it's a service - if it has sub 'components' - or it's a single components 
            '''
            if 'components' in component:
                '''
                It's a service
                '''
                self._services.append(component)
            else:
                '''
                It's a single component
                '''
                self._components.append(component)
              
        for service in self._services:
            for component in service['components']:
                component = self._search(self._components,'id',component)
                if (svc is None) or (svc in service['name']):
                    if (reg is None) or (reg in component['name']):
                        self._services_regions_status.append({'service':service['name'], 'region':component['name'], 'status': component['status']})

    def _search(self, mylist, key, value): 
        for item in mylist: 
            if item[key] == value: 
                return item                   
        return None 
    
    def get_data(self):  
        return self._last_update_date, self._services_regions_status, self._incidents   
            
                

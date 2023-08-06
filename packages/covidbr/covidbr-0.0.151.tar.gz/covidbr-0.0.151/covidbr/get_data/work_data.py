#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from covidbr.api_io.api_io_request import get_data_covid
from covidbr.log import log
from covidbr.statistical_functions.bases import mov_average, per_size,percent_basic

import pandas as pd
import numpy as np
import os


#api_io = login_io.API_io

############### tratamento de dados ############
class get_data_city:
    def __init__(self,city_state:str):
        self.type = 'covid_dataframe'
        self.city,self.state = tuple(city_state.split())
        #self.api_io = login_io.API_io()
        data_covid = get_data_covid(city=self.city,state=self.state)
        self.data_content, self.date_upload = data_covid['content_data'],data_covid['date_upload']
        if(os.path.isdir('data')):
            self._path_cache = 'data/'
            file_cache_data = self._path_cache+f'data_.csv'
            with open(self._path_cache+f'data_.csv','wb') as file_data:
                file_data.write(self.data_content)
            self.data = pd.read_csv(file_cache_data)
            os.system(f'rm {file_cache_data}')
        else:
            os.system('mkdir data')
            self._path_cache = 'data/'
        
        log('organizando dados do DataFrame...')
        self.dados_dict = self.miner_data(self.data)
        
        log('construindo um novo DataFrame...')
        self.dados = pd.DataFrame(self.dados_dict,index=self.dados_dict['date'])
        log('DataFrame construido com sucesso!')
        log('criando excel com os dados...')
        self.dados.to_excel(f'{self._path_cache}dados_{self.city}_{self.state}.xlsx')
        print('Excel criado com sucesso')
        print('dados ok!')
        
        log('mining statistical data...')
        self.mining_statistical_data(limit_period=15)
        log('statistical data mined! ')
    
    
    
    def mining_statistical_data(self,limit_period:int=15):
        self.date_update = self.date[-1]
        size = limit_period
        #### deaths ####
        ## making string ##
        all_deaths_string = list(str(self.mortes[-1]))
        if len(all_deaths_string) >= 4:
            all_deaths_string.insert(-3,'.')
        print(all_deaths_string)
        self.all_deaths_string = ''.join(all_deaths_string)
        ## others estatistic of this ##
        self.deaths_movel = mov_average(self.mortes_diarias,7)
        percent_deaths = per_size(self.deaths_movel,size)
        self.percent_deaths = round(percent_deaths,2)
        self.percent_all_deaths = percent_basic(self.mortes,size)
        param_per_deaths = 'up' if(percent_deaths > 0) else 'down'
        self.deaths_24h = self.mortes_diarias[-1]
        self.deaths_on_period = sum(self.mortes_diarias[-size:])
        
        ### cases ###
        ## making string for fluctuate point ##
        all_cases_string = list(str(self.casos[-1]))
        if len(all_cases_string) >= 4:
            all_cases_string.insert(-3,'.')
        print(all_cases_string)
        self.all_cases_string = ''.join(all_cases_string)
        ## others estimates of this ##
        self.cases_movel = mov_average(self.casos_diarios,7)
        percent_cases = per_size(self.cases_movel,size)
        self.percent_cases = round(percent_cases,2)
        self.percent_all_cases = percent_basic(self.casos,size) 
        param_per_cases = 'up' if(percent_cases > 0) else 'down'
        self.cases_24h = self.casos_diarios[-1]
        self.deaths_on_period = sum(self.mortes_diarias[-size:])
        
    


    def miner_data(self,data):
        self.casos = np.array(self.data['last_available_confirmed'][::-1])
        self.mortes = np.array(self.data['last_available_deaths'][::-1])
        self.casos_diarios = np.array(self.data['new_confirmed'][::-1])
        self.mortes_diarias = np.array(self.data['new_deaths'][::-1])
        self.population = np.array(self.data['estimated_population'][::-1])

        meses = ['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez']
        date = self.data['date'][::-1]
        years = [i[4:] for i in date]
        self.date = [i.split('-') for i in date]
        print(self.date)
        self.date = [('/').join([i[2],meses[int(i[1])-1],i[0]]) for i in self.date]
        dados = {'casos':np.array(self.casos),
            'mortos':np.array(self.mortes),
            'mortes_diarias':abs(np.array(self.mortes_diarias)),
            'casos_diarios':abs(np.array(self.casos_diarios)),
            'population':np.array(self.population),
            'date':self.date}
        log('dados do DataFrame organizadas!')
        return dados
        #file_name_data = api_io.file_data_excel



    def get_media_movel_deaths(self,smaPeriod:int):
        j = next(i for i, x in enumerate(abs(np.array(self.mortes_diarias))) if x is not None)
        data = abs(np.array(self.mortes_diarias))
        our_range = range(len(data))[j + smaPeriod - 1:]
        empty_list = [None] * (j + smaPeriod - 1)
        sub_result = [np.mean(data[i - smaPeriod + 1: i + 1]) for i in our_range]

        self.media_movel_deaths = np.array(empty_list + sub_result)
        return self.media_movel_deaths



    def get_media_movel_cases(self,smaPeriod:int):
        j = next(i for i, x in enumerate(abs(np.array(self.casos_diarios))) if x is not None)
        data = abs(np.array(self.mortes_diarias))
        our_range = range(len(data))[j + smaPeriod - 1:]
        empty_list = [None] * (j + smaPeriod - 1)
        sub_result = [np.mean(data[i - smaPeriod + 1: i + 1]) for i in our_range]

        self.media_movel_cases = np.array(empty_list + sub_result)
        return self.media_movel_cases


    
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import covidbr as cb



def publish_painel_covid(data,user:str,password:str,limit_period:int=15):
        
    if(os.path.isdir('config')):
        terminal = os.system
        print('apagando pasta config...')

        #apagando a pasta config
        terminal('rm config/*')
        terminal('rm config/log/*')
        terminal('rmdir config/log')
        terminal('rmdir config')

    from instabot import Bot
    #from instabot import InstaBot as 
    bot = Bot()

    
        #print((bot.get_timeline_medias()))
    #print(f'são {len(bot.followers)} seguidores no total')
    log = cb.logging.log
    #limit_period = 30
    data_city_covid = data #cb.data_from_city(city)
    path_file_img = f'{data.city}_painel.jpg'
    cb.painel_covid(data_city_covid,limit_period=limit_period,path_file=path_file_img,show=False)
    bot.login(username=user,password=password)#,use_cookie=True)
    bot.upload_photo(photo=path_file_img,caption=f'covid-19 na cidade de {data.city}-{data.state} {data.date_upload} \n#{data.city} #{data.state} #covid #data #python')
    os.system(f'rm {path_file_img}.REMOVE_ME')
    bot.logout()

'''
log(f'publicando media movel de casos nos útimos {limit_period} dias')
plt = cb.plot_media_cases(data=data_city_covid, show=False,
                          color_bar='#4ea286', color_line='black', limit_period=limit_period)
plt.title(f'média móvel de casos da covid-19 na cidade de {city} em {limit_period}')
#plt.grid()
path_img_cases = f'plot_media_cases_pet.png'
plt.savefig(path_img_cases, dpi=800)
bot.upload_photo(photo=path_img_cases,caption=f'plotagem de casos da covid-19 nos últimos {limit_period} dias na cidade de {city} {data_city_covid.date_upload} \n#petrolina #covid #data #python')

log(f'publicando media movel de mortes nos últimos {limit_period} dias')
plt = cb.plot_media_cases(data=data_city_covid, show=False,
                          color_bar='#8e43b5', color_line='black', limit_period=limit_period)
plt.title(f'média móvel de mortes da covid-19 na cidade de {city} em {limit_period}')
#plt.grid()
path_img_cases = f'plot_media_deaths_pet.png'
plt.savefig(path_img_cases, dpi=800)
bot.upload_photo(photo=path_img_cases,caption=f'plotagem dos números de mortes da covid-19 nos últimos {limit_period} dias na cidade de {city} {data_city_covid.date_upload} \n#petrolina #covid #data #python')
log('feito!')
'''

from covidbr.log.logging import log
from covidbr.log import date_base
from covidbr.get_data import get_data_city as dc
from covidbr.statistical_functions.bases import mov_average
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker

############### plotting media in the maxim period limited ###################
def plot_media_cases(data:dc,limit_period:int=0,color_line:str='red',
    title:str=None,show:bool=True,color_bar:str='black',
    path_dir:str=f'',path_file:str='plot_media.png',label_line:str='',label_bar:str='',
    grid_y:bool=False,grid_x:bool=False):
    plt.cla()
    plt.clf()
    '''
    sumary:

    '''
    #verification of data input is a data_from_city classtype
    if(data.type=='covid_dataframe'):
        pass
    else:
        raise Exception(f'[{date_base()}] Error! dataFrame is not a covid_br.get_data_covid')

    if limit_period:
        dados_bar = data.dados[-limit_period:]
        casos_diarios = data.dados['casos_diarios']
        media = mov_average(casos_diarios,7)
        media = media[-limit_period:]
        print('0 == False')
    else:
        dados_bar = data.dados
        casos_diarios = data.dados['casos_diarios']
        media = mov_average(casos_diarios,7)
        media_casos = media
        print('oks')

        limit_period = len(dados_bar.index)
    dados = data.dados
    city = data.city
    state = data.state

    ax = dados_bar.plot(x='date',y='casos_diarios',label=label_bar,kind='bar',color=color_bar)
    print(f'encontrando a média móvel de casos confirmados em {city}-{state}...')
    
    #media = calcSma(casos_diarios,7)
    media_casos = media
    #print((media.max))
    plt.ylim((0,max(casos_diarios[-limit_period:])+10))
    if grid_x:
        plt.grid(axis='x')
    if grid_y:
        plt.grid(axis='y')
    date = dados_bar['date']
    plt.plot(date,media,label=label_line,c=color_line)
    #plt.grid()

    ticklabels = ['']*len(dados_bar.index)
    ticklabels[::int(limit_period/10)] = dados_bar['date'][::int(limit_period/10)]
    ax.xaxis.set_major_formatter(ticker.FixedFormatter(ticklabels))
    plt.gcf().autofmt_xdate()

    plt.legend()
    plt.grid(axis='y')
    if title:
        plt.tile(f'{title}')
    elif(title=='pt-br'):
        plt.title(f'casos diarios em covid-19 em {city}-{state} nos últimos {limit_period} dias')
    if path_file:
        plt.savefig(f'{path_dir}{path_file}',dpi=900)
    if(show):
        plt.show()

    plt_casos = plt

    return plt_casos



################ tools for plotting of deaths data period limited ############### 
def plot_media_deaths(data:dc,limit_period:int=0,
title:str=None,show:bool=True,path_dir:str='',path_file:str='',
color_line:str='red',color_bar:str='black',
label_line:str='',label_bar:str=''):
    plt.cla()
    plt.clf()
    '''
    sumary:

    '''
    #verification of data input is a data_from_city classtype
    if(data.type=='covid_dataframe'):
        pass
    else:
        raise Exception(f'[{date_base()}] Error! dataFrame is not a covid_br.get_data_covid')

    if limit_period:
        dados_bar = data.dados[-limit_period:]
        deaths_day = data.dados['mortes_diarias']
        media = mov_average(deaths_day,7)
        media_casos = media
        media = media[-limit_period:]
        print('0 == False')
    else:
        dados_bar = data.dados
        deaths_day = data.dados['mortes_diarias']
        media = mov_average(deaths_day,7)
        media_casos = media
        print('oks')

        limit_period = len(dados_bar.index)
    dados = data.dados
    city = data.city
    state = data.state

    ax = dados_bar.plot(x='date',y='mortes_diarias',label=label_bar,kind='bar',color=color_bar)
    date = dados_bar['date']
    plt.plot(date,media,label=label_line,c=color_line)

    ticklabels = ['']*len(dados_bar.index)
    ticklabels[::int(limit_period/10)] = dados_bar['date'][::int(limit_period/10)]
    ax.xaxis.set_major_formatter(ticker.FixedFormatter(ticklabels))
    plt.gcf().autofmt_xdate()
    plt.grid(axis='y')
    plt.legend()

    if path_file:
        plt.savefig(f'{path_dir}{path_file}',dpi=900)
    if(show):
        plt.show()

    plt_casos = plt
    return plt_casos


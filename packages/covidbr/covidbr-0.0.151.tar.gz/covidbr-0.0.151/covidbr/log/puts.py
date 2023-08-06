from .date import date_base as date
from .info import ram

from translate import Translator

__cpu_show__ = False

def puts(*args,sep:str=' ',path_file:str=None)->None:
  input = ''
  for i in args:
    input += i+sep
  cpu = f'[CPU: {ram()[2]}%_{ram()[3]}ms]\n' if(__cpu_show__) else ''
  text = (f'{cpu}[{date()}]: {input}')
  print(text)
  if path_file:
    path = open(path_file,'a',encoding='utf-8')
    with open(path,'a') as file_p:
      file_p.write(text+'\n')
      # TODO: write code...
 

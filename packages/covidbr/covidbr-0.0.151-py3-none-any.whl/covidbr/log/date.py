
#data
def date_base(base_str:str='%d/%m/%Y %H:%M:%S'):
  from datetime import datetime as dt
  dt = dt.now()
  return dt.strftime(base_str)


#def get_date():

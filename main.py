import numpy as np 
import pandas as pd
from datetime import datetime
import logging
import logging.handlers


FILE_NAME = './log/chat.txt'

# Defined Keyword 

txt_dic = {
    'exit' : ['quit', 'exit'],
    'help' : ['help', '?']
}

data_dic = {
    'class' : ['A', 'B', 'C', 'D', 'E'],
    'start' : ['Berlin', 'Frankfurt', 'Munich', 'Nuremberg', 'Zurich', 'Stuttgart'],
    'end' : ['Bern', 'Vien', 'Barcelona', 'Paris', 'Amsterdam', 'Milano', 'Prague'],
    'time' : [],
    'number' : []
}

class PrintText:

    def __init__(self, input_name, filename=FILE_NAME):
        self._input_name = input_name
        self._filename = filename
        self._file_open()
    
    def _file_open(self):
        self._f = open(self._filename, 'a')

    def _file_close(self):
        self._f.close()

    def Print(self, text):
        print (text)
        file_text = str(datetime.now())+"|"+self._input_name+"|"+text+"\n"
        self._f.write(file_text)


def generating_data(num=50):

    data = pd.DataFrame()
    for key, values in data_dic.items():
      if key == 'time':
        data[key] = np.random.randint(0,24,num)
      elif key == 'number':
        arr_num = np.arange(num)
        np.random.shuffle(arr_num)
        data[key] = arr_num
      else:
        data[key] = np.random.choice(values, num)
    return data

def save_log(filename):
    pass

def main():
    
    input_text = None
    # get current time
    now = datetime.now()
    timestamp = datetime.timestamp(now)

    data = generating_data()
    print ("- this is chatbot -")
    print ("> What's your name?")
    input_name = input()
    pt = PrintText(input_name)
    pt.Print("> Hello "+input_name)
    pt.Print("> What do you want? (If you need to exit, type exit or quit)")

    while input_text not in txt_dic['exit']:
        input_text = input()
        if input_text not in txt_dic['exit']:
            print ("Input text :", input_text)
        else:
            pt.Print('- Exit the chatting - ')


if __name__=="__main__":
    main()  
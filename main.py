import numpy as np 
import pandas as pd
from datetime import datetime
import logging
import logging.handlers
import re


# Defined Keyword 
txt_dic = {
    'exit' : ['quit', 'exit'],
    'help' : ['help', '?'],
    'search' : ['find', 'look', 'search', 'get', 'browser', 'which', 'what'],
    'time' : ['when', 'time'],
    'lo_start' : ['departure', 'from', 'start'],
    'lo_end' : ['destination', 'toward', 'end']

}

feature_dic = {
    'class' : ['A', 'B', 'C', 'D', 'E'],
    'start' : ['Berlin', 'Frankfurt', 'Munich', 'Nuremberg', 'Zurich', 'Stuttgart'],
    'end' : ['Bern', 'Vien', 'Barcelona', 'Paris', 'Amsterdam', 'Milano', 'Prague'],
    'time' : ['am', 'pm', 'hour'],
    'number' : [],
}

HELLO_TEXT = "> What do you want? (If you need to exit, type exit or quit)"

def process_text(list_text):
    """
    Process input text
    Detect the key feature of list and store to dictionary

    Parameters
    ----------
    list_text : list of string
        list of input text
    
    Returns
    -------
    input_dic : Dictionary
        Dictionary that takes the feature as key and
        the corresponding information as a value
    """
    input_dic = {}
    for key, _ in feature_dic.items():
        input_dic[key] = None

    # Action trigger
    input_dic['action'] = False

    if len(set(list_text).intersection(set(txt_dic['lo_start'])))>0:
        input_dic['action'] = True
        for txt in list_text:
            if txt.capitalize() in feature_dic['start']:
                input_dic['start'] = txt.capitalize()
                

    return input_dic
        
def find_data(data, input_dic):
    """
    Find the data
    return the list of searching result from the input_dic
    WIP : add more feature searching

    Parameters
    ----------
    data : pandas DataFrame
        datasets
    
    input_dic : Dictionary
        Dictionary that takes the feature as key and
        the corresponding information as a value
    
    Returns
    -------
    search_list : list of string
        list of trucks
    """
    data_select = data[(data['start']==input_dic['start'])]

    if len(data_select) > 0:
        search_list = []
        for i in range(0, len(data_select)):
            items = data_select.iloc[i].to_list()
            txt_str = []
            for key, item in zip(data_select.columns, items):
                txt_str.append(key+':'+str(item))
            search_list.append(' '.join(map(str, txt_str)))
    else:
        search_list = None

    return search_list


class PrintText:
    """Print text and write to file 

    Parameters
    ----------
    input_name : string
        user name
    
    filename : string, default = './log/chat.txt'
        filename to save chat history

    """
    FILE_NAME = './log/chat.txt'

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


def generating_data(num=10):
    """generating random datasets

    Parameters
    ----------
    num : integer, default = 10
        Number of data that generated

    Returns
    -------
    data : pandas DataFrame
        generated datasets
    """
    data = pd.DataFrame()
    for key, values in feature_dic.items():
      if key == 'time':
        data[key] = np.random.randint(0,24,num)
      elif key == 'number':
        arr_num = np.arange(num)
        np.random.shuffle(arr_num)
        data[key] = arr_num
      else:
        data[key] = np.random.choice(values, num)
    return data

def main():
    
    input_text = None
    # get current time
    now = datetime.now()
    timestamp = datetime.timestamp(now)

    # Get data
    data = generating_data()
    print ("- this is chatbot -")
    print ("> What's your name?")
    input_name = input()
    pt = PrintText(input_name)
    pt.Print("> Hello "+input_name)
    
    while input_text not in txt_dic['exit']:
        pt.Print(HELLO_TEXT)
        input_text = input()
        if input_text not in txt_dic['exit']:
            # Processing input text
            # split the text 
            list_text = [x.lower() for x in input_text.split()]

            # Searching DB trigger
            if len(set(list_text).intersection(set(txt_dic['search'])))>0:
                input_dic = process_text(list_text)
                
                if input_dic['action']:
                    # Find the results
                    result = find_data(data, input_dic)
                    pt.Print("> Result....")
                    if result is None:
                        pt.Print("> There is no data")
                    else:
                        for rst in result:
                            pt.Print("> "+str(rst))
            else:
                pt.Print("> Hmm")
        else:
            pt.Print('- Exit the chatting - ')

if __name__=="__main__":
    main()  
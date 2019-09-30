import numpy as np 
import pandas as pd

# Defined Keyword 

txt_dic = {
    'exit' : ['quit', 'exit'],
    'help' : ['help', '?']
}

data_dic = {
    'class' : ['A', 'B', 'C', 'D', 'E'],
    'start' : ['BER', 'HAM', 'FRA', 'MUC', 'NUM', 'ZUR', 'BOR'],
    'end' : ['BEN', 'VIE', 'BAR', 'PAR', 'NIC', 'MIL', 'POR', 'MAL'],
    'time' : [],
    'number' : []
}

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

def main():
    
    input_text = None
    data = generating_data()
    print ("- Hello this is chatbot -")
    print ("> What do you want? (If you need to exit, type exit or quit)")

    while input_text not in txt_dic['exit']:
        input_text = input()
        if input_text not in txt_dic['exit']:
            print ("Input text :", input_text)
        else:
            print ('- Exit the chatting - ')


if __name__=="__main__":
    main()
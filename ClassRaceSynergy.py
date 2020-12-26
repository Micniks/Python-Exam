import DnD_Dataset_Handler as dh
import pandas as pd

default_dataframe_link = 'https://raw.githubusercontent.com/oganm/dndstats/master/docs/charTable.tsv'

class ClassRaceSynergy:
    
    def __init__(self, dataframe):
        if dataframe is not None:
            self.dataset = dataframe
        else:
            data_handler = dh.DND_Dataset_handler(default_dataframe_link)
            self.dataset = data_handler.dataset
        self.__total_datarow_count = len(self.dataset.index)
        
        
    def __get_table_data(self):
        
        # Get List of single class strings, not including any multiclasses
        class_list = [c.split('|') for c in self.dataset['justClass'].drop_duplicates()]
        single_class_list = []
        for c in class_list:
            for single_c in c:
                single_class_list.append(single_c)
        self.__single_class_list = list(dict.fromkeys(single_class_list))
        self.__single_class_list.sort()

        #Get List of single race strings, removing subtypes
        self.__full_race_list = list(r for r in self.dataset['race'].drop_duplicates())
        self.__full_race_list.sort()

        # Adding strings for total
        self.__full_race_list.append('Total')
        self.__single_class_list.append('Total')

        # Counting each cross value of class and race
        cross_count = {c:{r:0 for r in self.__full_race_list} for c in self.__single_class_list}

        for index, row in self.dataset.iterrows():
            cross_count['Total'][row['race']] += 1
            for c in row['justClass'].split('|'):
                cross_count[c]['Total'] += 1
                cross_count[c][row['race']] += 1
        return cross_count
        
        
    # To get a table where each synergy is counted, messured in the counts as ints
    def get_count_table(self):    
        # Setting up the data_dict
        cross_count = self.__get_table_data()
        result_data = {}
        for c in self.__single_class_list:
            result_data[c] = []
            for r in self.__full_race_list:
                result_data[c].append(cross_count[c][r])
        result_data['Total'][len(result_data['Total'])-1] = self.__total_datarow_count
        result = pd.DataFrame(result_data, columns = self.__single_class_list, index=self.__full_race_list).sort_values('Total', ascending=True)
        return result
        
        
    # To get a table where each synergy is counted, messured in percentage of the counts as floats 
    def get_percentage_table(self): 
        # Setting up the data_dict
        cross_count = self.__get_table_data()
        result_data = {}
        for c in self.__single_class_list:
            result_data[c] = []
            for r in self.__full_race_list:
                result_data[c].append(round((cross_count[c][r]/self.__total_datarow_count)*100, 2))
        result_data['Total'][len(result_data['Total'])-1] = None
        result = pd.DataFrame(result_data, columns = self.__single_class_list, index=self.__full_race_list).sort_values('Total', ascending=False)
        return result
        
        
    # To get a table where each point shows how often the race(row) picks that class(colum) in the dataset
    def get_class_picked_by_race_percentage_table(self): 
        # Setting up the data_dict
        cross_count = self.__get_table_data()
        result_data = {}
        for c in self.__single_class_list:
            if(c == 'Total'):
                break
            else:
                result_data[c] = []
                for r in self.__full_race_list:
                    if(r == 'Total'):
                        break
                    else:
                        result_data[c].append(round((cross_count[c][r]/cross_count['Total'][r]), 2))
        
        # Remove the row and colum for total
        self.__single_class_list.remove('Total')
        self.__full_race_list.remove('Total')
        
        result = pd.DataFrame(result_data, columns = self.__single_class_list, index=self.__full_race_list)
        return result
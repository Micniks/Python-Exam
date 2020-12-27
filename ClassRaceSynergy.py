import DnD_Dataset_Handler as dh
import pandas as pd

default_dataframe_link = 'https://raw.githubusercontent.com/oganm/dndstats/master/docs/charTable.tsv'

class ClassRaceSynergy:
    """
    This class shows datatables for synergy between race and class choices from the given dataset
    """
    
    def __init__(self, dataset):
        """
        Initiate the class with either a dataset pulled from the default source, or use a given dataset.
        """
        
        if dataset is not None:
            self.dataset = dataset
        else:
            data_handler = dh.DND_Dataset_handler(default_dataframe_link)
            self.dataset = data_handler.dataset
        self.__total_datarow_count = len(self.dataset.index)
        
        
    def __get_table_data(self):
        """
        This method is for setting up values for any of the table methods, by counting the races, classes and synergies in between.
        """
        
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
        
        
    def get_count_table(self):
        """
        Returns a dataframe for a table, where each choice of race(row) and class(column) combination in shown numerically.
        """
        
        cross_count = self.__get_table_data()
        result_data = {}
        for c in self.__single_class_list:
            result_data[c] = []
            for r in self.__full_race_list:
                result_data[c].append(cross_count[c][r])
        result_data['Total'][len(result_data['Total'])-1] = self.__total_datarow_count
        result = pd.DataFrame(result_data, columns = self.__single_class_list, index=self.__full_race_list).sort_values('Total', ascending=True)
        return result
        
        
    def get_percentage_table(self):
        """
        Returns a dataframe for a table, where each choice of race(row) and class(column) combination in shown in percentage, 
        relative to the total amount of choices.
        """
        
        cross_count = self.__get_table_data()
        result_data = {}
        for c in self.__single_class_list:
            result_data[c] = []
            for r in self.__full_race_list:
                result_data[c].append(round((cross_count[c][r]/self.__total_datarow_count)*100, 2))
        result_data['Total'][len(result_data['Total'])-1] = None
        result = pd.DataFrame(result_data, columns = self.__single_class_list, index=self.__full_race_list).sort_values('Total', ascending=False)
        return result
        
        
    def get_class_picked_by_race_percentage_table(self):
        """
        Returns a dataframe for a table, where each choice of class(column) combination in shown in percentage, 
        relative to the total amount of choices within that race(row).
        """
        
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
                        result_data[c].append(round((cross_count[c][r]/cross_count['Total'][r])*100, 2))
        
        # Remove the row and colum for total
        self.__single_class_list.remove('Total')
        self.__full_race_list.remove('Total')
        
        result = pd.DataFrame(result_data, columns = self.__single_class_list, index=self.__full_race_list)
        return result
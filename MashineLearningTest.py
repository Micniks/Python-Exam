import pandas as pd
import numpy as np
import argparse
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

data = pd.read_csv('https://raw.githubusercontent.com/oganm/dndstats/master/docs/charTable.tsv', sep='\t')
#display(data)

class DNDClassPredictor:
    def __init__(self, dataset):
        #Get data from dataset
        if dataset is None:
            self.dataset = pd.read_csv('https://raw.githubusercontent.com/oganm/dndstats/master/docs/charTable.tsv', sep='\t')
        else:
            self.dataset = dataset
        self.__features = self.dataset[['Str','Dex','Con','Wis','Int','Cha']]
        targets = self.dataset[['justClass']]

        #Get List of single class strings, not including any multiclasses
        classes_list = targets.drop_duplicates()
        single_class_list = [c for c in classes_list['justClass'] if '|' not in c]
        single_class_list.sort()
        
        #Replace all class strings with number
        self.__classes_dict = {}
        for idx in range(len(single_class_list)):
            dnd_class = single_class_list[idx]
            self.__classes_dict[dnd_class] = idx
            
        numeric_targets = targets.replace(self.__classes_dict) 
        targets = numeric_targets

        #Removing all multiclass strings, that was not removed above, and replace with single value
        numeric_targets = targets.replace("^\w.*$", len(self.__classes_dict), regex=True)
        self.__targets = numeric_targets
        
        #Finalizing the dict, and adding an opposite dict for classes
        self.__classes_dict['Multiclassing'] = len(self.__classes_dict)
        self.__classes_numeric_dict = {y:x for x,y in self.__classes_dict.items()}
        
        #Using another class method to make a fit a model for prediction, and check if the model has good test results
        min_test_score = 0.6
        test_score = 0
        found_good_model = False
        for num in (range(1,101)):
            test_score = self.fit_class_model()
            if (test_score >= min_test_score):
                found_good_model = True
                #print('Found a good model after', num, 'attempts')
                break
        if(not found_good_model):
            print('WARNING: The model could not achive a good test score, and is only', test_score*100, 'accurate in test')
        
    def fit_class_model(self):
        #Setting up the model, and testing with classification
        x_train,x_test,y_train,y_test = train_test_split(self.__features,self.__targets,test_size=0.3)
        
        self.__model = DecisionTreeClassifier()
        self.__model.fit(x_train, y_train)

        #Display the score for the model from the dataset
        test_score = self.__model.score(x_test, y_test)
        return test_score
        
        #print('Train Score:', self.__model.score(x_train, y_train))
        #print('Testing Score', self.__model.score(x_test, y_test))     
        
    def predict_class_from_ability_scores(self, ability_scores):
        numeric_result = self.__model.predict([ability_scores])[0]
        result = self.__classes_numeric_dict[numeric_result]
        return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This program allows you to input 6 ability scores for dungeons and dragons 5th edition, and get a suitable class for those ability scores as output')

    parser.add_argument('-ab','--abilityScores', nargs='+', help='<Required> Give a list of the ability scores in the following order: Strength(Str) Dexterity(Dex) Constitution(Con) Intelligence(Int) Wisdom(Wis) Charisma(Cha)', required=True)
    args = parser.parse_args()
    input = args.abilityScores
    
    if(len(input) == 6):
        try:         
            ability_scores = []
            for score in input:
                ability_scores.append(int(score)) 

            classPredictor = DNDClassPredictor(None)
            result = classPredictor.predict_class_from_ability_scores(ability_scores)
            msg = "The given ability scores would work well with a class choice of " + result
            print(msg) 
        except ValueError:
            print("One or more of the ability scores could not be read as a numbers") 
    else:
        print("The given input needs exactly 6 arguments, seperated by space, representing, in order: Strength(Str) Dexterity(Dex) Constitution(Con) Intelligence(Int) Wisdom(Wis) Charisma(Cha)")
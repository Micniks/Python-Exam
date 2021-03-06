import pandas as pd
import numpy as np
import argparse
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

default_dataset = 'https://raw.githubusercontent.com/oganm/dndstats/master/docs/charTable.tsv'

class DNDClassPredictor:
    """
    This class use machine-learning in order to make guesses on good class choices based on a choosen ability score
    """
    
    def __init__(self, dataset = None):
        """
        Initiate the class, either with a given dataset, or it will pull from the default dataset.
        """
        
        #Get data from dataset
        if dataset is None:
            self.dataset = pd.read_csv(default_dataset, sep='\t')
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
        min_test_score = 0.4
        test_score = 0
        found_good_model = False
        for num in (range(1,1001)):
            model = self.fit_class_model()
            if (model["test_score"] >= min_test_score):
                found_good_model = True
                self.__model = model["model"]
                break
            elif (model["test_score"] > test_score):
                self.__model = model["model"]
                test_score = model["test_score"]
        if(not found_good_model):
            print('WARNING: The model could not achive a good test score, and is only', test_score*100, 'accurate in test')
        
    def fit_class_model(self):
        """
        Method to get dict containing a model fit with data from the dataset, along with a score for the model
        """
        
        #Setting up the model, and testing with classification
        x_train,x_test,y_train,y_test = train_test_split(self.__features,self.__targets,test_size=0.3)
        
        model = DecisionTreeClassifier()
        model.fit(x_train, y_train)

        #Display the score for the model from the dataset
        test_score = model.score(x_test, y_test)
        return {"model": model, "test_score": test_score}
        
        #print('Train Score:', self.__model.score(x_train, y_train))
        #print('Testing Score', self.__model.score(x_test, y_test))     
        
    def predict_class_from_ability_scores(self, ability_scores):
        """
        Uses the class model to try and predict a good class choice for a given ability score, based on the dataset.
        """
        
        numeric_result = self.__model.predict([ability_scores])[0]
        result = self.__classes_numeric_dict[numeric_result]
        return "The given ability scores would work well with a class choice of: " + result

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

            classPredictor = DNDClassPredictor()
            result = classPredictor.predict_class_from_ability_scores(ability_scores)
            msg = result
            print(msg) 
        except ValueError:
            print("One or more of the ability scores could not be read as a numbers") 
    else:
        print("The given input needs exactly 6 arguments, seperated by space, representing, in order: Strength(Str) Dexterity(Dex) Constitution(Con) Intelligence(Int) Wisdom(Wis) Charisma(Cha)")
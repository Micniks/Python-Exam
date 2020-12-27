import pandas as pd
import os

default_link = 'https://raw.githubusercontent.com/oganm/dndstats/master/docs/charTable.tsv'
default_fileName = 'CharacterDataset'
dataset_folder = 'Datasets'
official_dnd_classes = ['Artificer', 'Barbarian', 'Bard', 'Blood hunter', 'Cleric', 'Druid', 'Fighter', 'Monk', 'Paladin', 'Ranger', 'Rogue', 'Sorcerer', 'Warlock', 'Wizard']
official_dnd_races = ['Dragonborn', 'Dwarf', 'Elf', 'Gnome', 'Half-Elf', 'Halfling', 'Half-Orc', 'Human', 'Tiefling', 'Aasimar', 'Bugbear', 'Firbolg', 'Goblin', 'Hobgoblin', 'Kenku', 'Kobold', 'Lizardfolk', 'Orc', 'Tabaxi','Triton', 'Changeling', 'Kalashtar', 'Shifter', 'Warforged']

class DND_Dataset_handler:
    """
    This class is responsible for getting and preparing the dataset/dataframe for the other classes used in the main program.
    """
    
    def __init__(self, link = default_link, cleanData = True):
        """
        Initiate the class, either pulling from a given link, or pulling from the default dataset. 
        Gives the option of cleaning the data of things like dublicates or unofficial data.
        """
    
        self.dataset = self.__pull(link)
        if cleanData:
            self.clean_dataset()
    
    
    def __pull(self, link):
        """
        Private method that pulls the dataset from the given link.
        """
    
        if link is None:
            dataset = pd.read_csv(default_link, sep='\t')
        else:
            dataset = pd.read_csv(link, sep='\t')
        return dataset
    
    
    def clean_dataset(self):
        """
        Clean the dataset for the following:
            -Characters with missing data vital for the program (race, level, classes)
            -Characters with out of bound levels (below 1 or above 20)
            -Characters with unofficial class choices
            -Characters with unofficial race choices
            -Removal of dublicate characters
        """    
    
        # Remove characters with missing vital values
        self.dataset.dropna(subset=['race', 'level', 'justClass'], inplace=True)

        
        # Remove characters with a total level over 20 and below 1
        indexes_to_remove = self.dataset[self.dataset['level'] > 20].index
        self.dataset.drop(indexes_to_remove, inplace=True)
        indexes_to_remove = self.dataset[self.dataset['level'] < 1].index
        self.dataset.drop(indexes_to_remove, inplace=True)
        
        
        # Remove all characters with a non-official class choice
        indexes_to_remove = []
        all_index = self.dataset[self.dataset['level'] > 0].index
        for idx in all_index:
            classes = self.dataset['justClass'][idx]
            class_list = classes.split("|")
            for c in class_list:
                if c.capitalize() not in official_dnd_classes:
                    indexes_to_remove.append(idx)
                    break
        self.dataset.drop(indexes_to_remove, inplace=True)
        
        
        # Remove all characters with a non-official race choice
        indexes_to_remove = []
        all_index = self.dataset[self.dataset['level'] > 0].index
        for idx in all_index:
            full_race = self.dataset['race'][idx]
            race = full_race.split()[len(full_race.split())-1]
            self.dataset.loc[idx, ('race')] = race.capitalize()
            if race.capitalize() not in official_dnd_races:
                indexes_to_remove.append(idx)
        self.dataset.drop(indexes_to_remove, inplace=True)
        
        
        # Remove dublicate characters, keeping the last one
        self.dataset.drop_duplicates(subset='name', keep='last', inplace=True)
    
    
    def getSpecificCharacters(self, category, value):
        """
        Returns a dataframe with just the characters fitting the search critiria.
            -Parameter category referce to a column name from the main dataset.
            -Parameter value referce to the search value within the above category.
        """
    
        if category in ['race', 'name', 'justClass', 'class']:
            return self.dataset.loc[self.dataset[category].str.contains(value)]
        else:
            return self.dataset.loc[self.dataset[category] == value]
    
    def saveToFile(self, fileName = default_fileName): 
        """
        Save the dataset under a given filename, inside the folder 'Datasets' next to this file.
        """
    
        if not os.path.exists(dataset_folder):
            os.makedirs(dataset_folder)
        path = dataset_folder + '/' + fileName + '.tsv'
        self.dataset.to_csv(path, sep = '\t')
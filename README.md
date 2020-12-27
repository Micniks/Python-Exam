# Gruppe 3 - Uptight Wealth
*Ikke vores valg af gruppenavn*

**Gruppemedlemmer:**
- Cahit
- Marcus
- Michael

## Eksamensprojekt

*Vores tema ligger indenfor statistik om rollespil, specifikt for 5th edition Dungeon and Dragons.*


### Beskrivelse af problemstillingen

Problemstillingen for projektet har været, at når man er ny til et rollespilssytem, som "5th edition Dungeons and Dragons", så kan der være mange muligheder, hvor man ikke helt ved hvad man bør vælge.

Ud fra dette, har vi ville samle en masse statistik på hvad der er populært ud fra et kendt datasæt [her](https://github.com/oganm/dndstats/blob/master/docs/charTable.tsv), for at hjælpe nye spillere med at træffe mere informerede valg.


### Hvilke teknologier benyttes
Vi benytter os af Python og benytter følgende imports i vores kode:
- pandas
- numpy
- argparse
- sklearn
- os
- matplotlib.pyplot
- bs4
- selenium
- networkx

Vi har primært arbejdet i dét docker-miljø vi har brugt i undervisningen i løbet af semesteret, som bl.a. har påvirket brugen af webscrabing ved fx path til geckodriver. Dette miljø kan findes [her](https://github.com/Hartmannsolution/docker_notebooks)


### Hvordan køres projektet
Vores program er lavet til at blive kørt gennem notebook fra filen [Main.ipynb](https://github.com/Micniks/Python-Exam/blob/main/Main.ipynb), som læser de andre filer, vi har lavet, ind, og som er delt efter formål og tanker på læringsmål.

Følgende filer kan køres direkte som sin egen main:
* [AbilityScoreAndClassMashineLearning](https://github.com/Micniks/Python-Exam/blob/main/AbilityScoreAndClassMashineLearning.py)


### Noter til projekt-forløbet
Efter at have begyndt på projektet, begyndte vi at identificere fejl og mangler i datasættet, men kunne ikke finde et godt alternative til datasættet. Dette har ledt til en smule ekstra arbejde, og et mindre datasæt, som vi selv ikke syntes har været optimalt. Programmet fungere stadig efter hensigt, men ville fungere meget bedre, med et større/mere gennemfør datasæt.

Derudover har vi benyttet den officielle hjemmeside for Dungeon and Dragons 5th Edition, [dndbeyond](https://www.dndbeyond.com/), samt en populær side, [Roll20](https://roll20.net/compendium/dnd5e/BookIndex), til f.eks. brug af webscrabing.
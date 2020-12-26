# Gruppe 3 - Uptight Wealth
*Ikke vores valg af gruppenavn*

**Gruppemedlemmer:**
- Cahit
- Marcus
- Michael

## Exam Projekt

*Vores tema ligger inde for statestik om rollespil, specifikt for 5th edition Dungeon and Dragons.*


### Beskrivelse af problemstillingen

Problemstillingen for projektet har været at når man er ny til et rollespilssytem, som 5th edition Dungeon and Dragons, så kan der være mange muligheder, hvor man ikke helt ved hvad man bør vælge.

Ud fra dette, har vi ville samle en masse statestik på hvad der er populært ud fra et kendt dataset [her](https://github.com/oganm/dndstats/blob/master/docs/charTable.tsv), for at hjælpe til at lave mere informerede valg.


### Hvilke teknologier benyttes
Vi benytter os af Python med følgende imports brugt i vores kode:
- pandas
- numpy
- argparse
- sklearn
- os
- matplotlib.pyplot
- bs4
- requests
- selenium
- networkx
- re

Vi har primært arbejdet i et docker-miljø brugt i undervisning i løbet af semesteret, som bl.a. har påvirket brug af webscrabing ved fx path til geckodriver. Dette miljø kan findes [her](https://github.com/Hartmannsolution/docker_notebooks)


### Hvordan køres projektet
Vores program er lavet til at blive kørt gennem notebook fra filen [Main.ipynb](https://github.com/Micniks/Python-Exam/blob/main/Main.ipynb), som læser de andre filer vi har lavet ind, som er delt efter formål og tanker på læringsmål.

Følgende filer kan køres direkte som egne main:
* [AbilityScoreAndClassMashineLearning](https://github.com/Micniks/Python-Exam/blob/main/AbilityScoreAndClassMashineLearning.py)

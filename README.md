# LaTeCH-CLfL-2020

Repository associated with *History to Myths: Social Network Analysis for Comparison of Stories over Time* paper.

## Data
Texts:
- *Decem libros historium* (**DLH**) by Gregory of Tours
- *Nibelungenlied* (**NIB**)
- *Völsunga saga* (**VOL**)

**DLH** is the historical reference.
**NIB** and **VÖL** are fiction works.

## Installation

Tested on Windows 10 and Ubuntu 16.04. 
Tested with Python 3.7 and 3.8.

```shell script
$ git clone https://github.com/clemsciences/LaTeCH-CLfl-2020-besnier.git
$ cd LaTeCH-CLfl-2020-besnier
$ virtualenv -p /usr/bin/python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt 
```

## Reproducing results

1. Download resources
Run `$ python -m -m latechclfl2020.models.initiate latechclfl2020/models/initiate.py`
2. Generating graphs.
Run `$ python -m latechclfl2020.models.scripts latechclfl2020/models/scripts.py`
3. Generating character feature table in paper.
Run `$ python -m latechclfl2020.models.reconstruction latechclfl2020/models/reconstruction.py` 
4. Generating Brynhildr ego-graphs.
Run `$ python -m latechclfl2020.models.paper.graph_visualisation latechclfl2020/models/paper/graph_visualisation.py`
5. Corpus observation.
Run `$ python -m latechclfl2020.models.paper.corpus_observation latechclfl2020/models/paper/corpus_observation.py`



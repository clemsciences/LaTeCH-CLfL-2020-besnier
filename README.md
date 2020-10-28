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

```shell script
$ git clone https://github.com/clemsciences/LaTeCH-CLfl-2020-besnier.git
$ pip install -r requirements.txt 
```

## Reproducing results

1. Generating graphs.
Run `$ python3 latechclfl2020/models/scripts.py`
2. Generating character feature table in paper.
Run `$ python3 latechclfl2020/models/reconstruction.py` 
3. Generating Brynhildr ego-graphs.
Run `$ python3 latechclfl2020/models/paper/graph_visualisation.py`
4. Corpus observation.
Run `$ python3 latechclfl2020/models/paper/corpus_observation.py`

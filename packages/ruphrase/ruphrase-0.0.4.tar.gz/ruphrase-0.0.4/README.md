# ruphrase

Build the correct turn of phrase in Russian



## Installation

Run `pip install ruphrase`
or `python -m pip install --user ruphrase`



## Usage

```
>>> from ruphrase import ruphrase
>>> 
>>> ruphrase('Опубликован/а/ы', 42, 'новост/ь/и/ей')
Опубликованы 42 новости

>>> ruphrase(None, 15, '/сияющая звезда/сияющие звезды/сияющих звезд')
15 сияющих звезд

>>> ruphrase('Заселен/ы', 3001, 'дом/а/ов', '')
Заселен 3001 дом

```

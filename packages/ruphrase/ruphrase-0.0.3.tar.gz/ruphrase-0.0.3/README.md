# ruphrase

Build the correct turn of phrase in Russian


## Installation

Run `pip install ruphrase`
or `python -m pip install --user ruphrase`


## Usage

```
>>> from ruphrase impport ruphrase
>>> ruphrase('ќпубликован/а/ы', 42, 'новост/ь/и/ей')
ќпубликованы 42 новости

>>> ruphrase(None, 15, '/си€юща€ звезда/си€ющие звезды/си€ющих звезд')
15 си€ющих звезд

>>> ruphrase('«аселен/ы', 3001, 'дом/а/ов', '')
«аселен 3001 дом

```

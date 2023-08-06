# ruphrase

Build the correct turn of phrase in Russian


## Installation

Run `pip install ruphrase`
or `python -m pip install --user ruphrase`


## Usage

```
>>> from ruphrase impport ruphrase
>>> ruphrase('�����������/�/�', 42, '������/�/�/��')
������������ 42 �������

>>> ruphrase(None, 15, '/������� ������/������� ������/������� �����')
15 ������� �����

>>> ruphrase('�������/�', 3001, '���/�/��', '')
������� 3001 ���

```

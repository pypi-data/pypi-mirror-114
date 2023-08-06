"""Functions for ruphrase"""


def ruphrase(prefix_forms, number, noun_forms='', grouping_symbol='`'):
    """
    Build the correct turn of phrase in Russian
    [prefix word] [number] [noun]

    Parameters
    ----------
    prefix_forms : str
        Declensions of prefix word for 101, 102 and 105
    number : int
        Number
    noun_forms : str
        Declensions of noun for 101 and 102
    grouping_symbol : str
        Digit grouping symbol

    Returns
    -------
    str
        Phrase with correct declensions [prefix word] [number] [noun]. 
        The digit grouping symbol is applied to the number.

    Examples
    -------
    >>> ruphrase('ќпубликован/а/ы', 42, 'новост/ь/и/ей')
    ќпубликованы 42 новости

    >>> ruphrase(None, 15, '/си€юща€ звезда/си€ющие звезды/си€ющих звезд')
    15 звезд

    >>> ruphrase('—пасен/ы', 3001, 'кот/а/ов', '')
    —пасен 3001 кот
    """

    if prefix_forms is None:
        prefix_forms = ''

    prefix = prefix_forms.split('/')
    if len(prefix) == 0:
        prefix = ['', '']
    elif len(prefix) == 1:
        prefix = [prefix[0]+' ', prefix[0]+' ']
    elif len(prefix) == 2:
        prefix = [prefix[0]+' ', prefix[0]+prefix[1]+' ']
    else:
        prefix = [prefix[0]+prefix[1]+' ', prefix[0]+prefix[2]+' ']

    if noun_forms is None:
        noun_forms = ''

    noun = noun_forms.split('/')
    if len(noun) == 0:
        noun = ['', '', '']
    elif len(noun) == 1:
        noun = [' '+noun[0], ' '+noun[0], ' '+noun[0]]
    elif len(noun) == 2:
        noun = [' '+noun[0], ' '+noun[0]+noun[1], ' '+noun[0]+noun[1]]
    elif len(noun) == 3:
        noun = [' '+noun[0], ' '+noun[0]+noun[1], ' '+noun[0]+noun[2]]
    else:
        noun = [' '+noun[0]+noun[1], ' '+noun[0]+noun[2], ' '+noun[0]+noun[3]]

    n = f'{number:,}'.replace(',', grouping_symbol)
    form_prefix = 1
    form_noun = 1
    if (n[-1] == '0') or (n[-1] > '4') or ((len(n) > 1) and (n[-2] == '1')):
        form_noun = 2
    elif n[-1] == '1':
        form_prefix = 0
        form_noun = 0

    return f'{prefix[form_prefix]}{n}{noun[form_noun]}'.strip()

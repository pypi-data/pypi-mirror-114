#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 21:20:38 2021

@author: tyler
"""

#%%
Mcode = {'.-' : 'A', '-...' : 'B','-.-.' :'C','-..' :'D',
       '.':'E','..-.':'F','--.':'G','....':'H','..':'I',
       '.---':'J','-.-':'K','.-..':'L','--':'M','-.':'N',
       '---':'O','.--.':'P','--.-':'Q','.-.':'R','...':'S',
       '-':'T','..-':'U','...-':'V','.--':'W','-..-':'X',
       '-.--':'Y','--..':'Z','.---':'1','..---':'2','...--':'3','....-':'4',
       '.....':'5','-....':'6','--...':'7','---..':'8','----.':'9','-----':'0'}


reversed_Mcode = {value : key for (key, value) in Mcode.items()}

def decodeMorse(morse_code):
    mistake = 'Not recognised: '
    # ToDo: Accept dots, dashes and spaces, return human-readable message
    for space in morse_code:
        if space != ' ':
            morse_code = morse_code[morse_code.index(space):]
            break
    morse_code = morse_code.replace('   ',' * ')
    sentence = ''
    for word in morse_code.split(' '):
        if (word == '*'):
            sentence += ' '
        elif word == '...---...':
            sentence += 'SOS'
        elif word == '':
            continue
        elif word not in Mcode:
            mistake += word
            sentence += word
        else :
            sentence += (Mcode[word])
    return sentence,mistake

#%%

def codeMorse(normal_code):
    # ToDo: Accept dots, dashes and spaces, return human-readable message
    for space in normal_code:
        if space != ' ':
            normal_code = normal_code[normal_code.index(space):]
            break
    normal_code = normal_code.replace(' ','*')
    sentence = ''
    for word in list(normal_code):
        if (word == '*'):
            sentence += '   '
        elif word == 'SOS':
            sentence += '...---...'
        else :
            sentence += (reversed_Mcode[word]+' ')
    return sentence


#%%

import sys

def main():
    
    print(
     '#     #                                 #####                       ','\n'
     '##   ##  ####  #####   ####  ######    #        ####  #####  ###### ','\n'
     '# # # # #    # #    # #      #         #       #    # #    # #      ','\n'
     '#  #  # #    # #    #  ####  #####     #       #    # #    # #####  ','\n'
     '#     # #    # #####       # #         #       #    # #    # #      ','\n'
     '#     # #    # #   #  #    # #         #       #    # #    # #      ','\n'
     '#     #  ####  #    #  ####  ######     #####   ####  #####  ###### ','\n')
    
    print('Welcom to Morse Code')
    print('Designed by Tylerastro')
    print('Enter q to exit')

    run = True
    while run:
        translate = str(input('Enter your word here and I translate for you: '))
        if translate == 'q':
            sys.exit()
        else:
            translate_upp = translate.upper()
            try:
                print( codeMorse(translate_upp))
            except:
                print( decodeMorse(translate_upp))
                
if __name__ == "__main__":
    main()


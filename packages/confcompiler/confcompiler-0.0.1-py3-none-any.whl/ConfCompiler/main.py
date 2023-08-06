#
#   ____             __  ____                      _ _           
#  / ___|___  _ __  / _|/ ___|___  _ __ ___  _ __ (_) | ___ _ __ 
# | |   / _ \| '_ \| |_| |   / _ \| '_ ` _ \| '_ \| | |/ _ \ '__|
# | |__| (_) | | | |  _| |__| (_) | | | | | | |_) | | |  __/ |   
#  \____\___/|_| |_|_|  \____\___/|_| |_| |_| .__/|_|_|\___|_|   
#                                           |_|                  
#     Github: https://github.com/NotReeceHarris/DotConfCompiler
#     Dev   : https://github.com/NotReeceHarris

# Config file:
#       Dont directly edit this file unless you know what your doing,
#       Editing this file may cause errors and issues later on.
#
#       Editing this file directly may also cause security issues
#       if someone told you to edit this THINK FIRST before editing
#       this may De-anonymiseing you or open you to data leaks.
# 
# Config syntax:
#       Commenting - All comments must start with '#' and must be on
#                    there on line, you cannot comment a line with 
#                    data involved.
#
#       Variables  - Data must start with a variable name then continued
#                    with '=' after that the data.
#     
#       Data Types - Boolen, String

def ConfRead(FilePath):

    # Creates a dict of all lines in conf file.
    # Excluding:
    #       lines starting with '#'
    #       lines containing nothing
    # Including:
    #       lines containing data

    conf = [x for x in open(FilePath).read().splitlines() if not x.startswith('#')]
    VarNames = []
    Data = []

    while '' in conf: conf.remove('')

    # Removes variable name from dict and adds the
    # data back to the list minus the variable name

    for idx, x in enumerate(conf):
        index = x.find('=')
        VarNames.append(x[:index])
        Data.append(x[index:][1:])
    
    ConfForm = '{'

    # Converts string values into boolens and nil value if 
    # data equal to 'True', 'False', 'None'

    for x in range(len(VarNames)):
        if Data[x].lower() == 'true' or Data[x] == True:
            ConfForm += f'"{VarNames[x]}":true'
        elif Data[x].lower() == 'false' or Data[x] == False:
            ConfForm += f'"{VarNames[x]}":false'
        elif Data[x].lower() == 'none' or Data[x] == None:
            ConfForm += f'"{VarNames[x]}":null'
        else:
            ConfForm += f'"{VarNames[x]}":"{Data[x]}"'

        try:
            VarNames[x+1]
            ConfForm += ','
        except:
            ConfForm += '}'

    # Method to convert homebrew dict into a dict type.
    # Method:
    #   Temporarily create a 'temp.json' file and writing 
    #   the homebrew dict into the file, use the json
    #   package to compile the json into a dict type.

    import json
    import os

    w = open('./temp.json', 'w')
    w.write(ConfForm)
    w.close()
    x = json.load(open('./temp.json'))
    os.remove('./temp.json')

    return x

def ConfWrite(FilePath, VarName, Data):

    # Creates a dict of all lines in conf file.

    conf = [x for x in open(FilePath).read().splitlines()]

    # Open and read the config file

    r = open(FilePath, 'r')
    fc = ''

    # iterate through all lines in the file and search for an '='
    # within the line, if the data before the '=' is equal to the
    # variable name then update that line with the new data.

    for x in r.readlines():
        index = x.find('=')
        if x[:index] == VarName:
            fc += f'{VarName}={Data}\n'
        else:
            fc += x

    # Open and write the 'fc' data

    w = open(FilePath, 'w')
    w.write(fc)

    # Close r and w

    r.close()
    w.close()

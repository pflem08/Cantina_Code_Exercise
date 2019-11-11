import json;
import collections.abc;
from enum import Enum;

#enum for selector attributes
class Attribute(Enum):
    CLASS = 1;
    CLASSNAME = 2;
    IDENTIFIER = 3;

#enum for selectors
class Selector(Enum):
    SINGLE = 1;
    COMPOUND = 2;
    CHAIN = 3;

#function to check if the selector attribute is a class, classname, or an identifier
def getAttributeType(selectorName):
    if(selectorName[0] == "."):
        return Attribute.CLASSNAME;
    elif(selectorName[0] == "#"):
        return Attribute.IDENTIFIER;
    else:
        return Attribute.CLASS;

#function to check if the key is a class, classname, or an identifier
def getKeyAttributeType(selectorName):
    if(selectorName == "className"):
        return Attribute.CLASSNAME;
    elif(selectorName == "identifier"):
        return Attribute.IDENTIFIER;
    elif(selectorName == "class"):
        return Attribute.CLASS;
    else:
        return -1;

#given a string, this function will determine if it is a single selector, a compound selector, or a chained selector
def getSelectorType(selector):
    compSel = 0;#bool for checking if the selector is compound or not

    if ((' ' in selector) == True):
        return Selector.CHAIN;
    else:
        iterSel = iter(selector)#skip first iteration
        next(iterSel)
        for c in selector:
            if(c == "#" or c == "."):#if one of the chars is somewhere inside the string then it is a compound selector
                compSel = 1;
        if(compSel == 1):
            return Selector.COMPOUND;
        else:
            return Selector.SINGLE;

#this function takes of string representing a single, compound, or chain selector and splits it up and stores it in the given array
def selectorBreakup(selectorString, splitSelectors):
    startPoint = 0;#this var is used to hold the starting point for a single selector
    for x in range(len(selectorString)):
        if(((selectorString[x] == ".") or (selectorString[x] == "#")) and (x != 0)):#skip if '.' or '#' is the first character
            splitSelectors.append(selectorString[startPoint:x]);
            startPoint = x;#new starting point
        if(x+1 == len(selectorString)):#for the very last character
            splitSelectors.append(selectorString[startPoint:x+1]);
    return 0;


#recursive function that takes a dictionary(JSON) and uses a given selector to find dictionaries
#The function treats a JSON like and tree data structure where each node is a dictionary
#The function takes 5 arguments:
    # The JSON data: IMPORTANT- the data has to follow the same form and patterns as the example data
    # A list to contain the matched dictionaries
    # The list containing the selectors
    # The number of parent selectors (for chain and compound selectors)
    # And a bool with 1 being a chain selector
def searchViewsCompound(dict, matchedViews, selectors, parentSelectors, isChain):
    matchNum = 0;# holds the number of selectors that matched the compound selectors;

    if(isinstance(dict, str)):#if the parent is a string (no children)
        for sel in selectors:#check to see if the ID matches the selector
            if (dict == sel):#check for match
                if(len(selectors == 1 and parentSelectors == 0)):#if the desired selector was only one and all parent selectors have been found
                    matchedViews.append(dict);#then this view matches the search
                    return 0;#definite end of branch so return
    else:
        dictKeys = dict.keys();

        for key in dictKeys:#check each child in the dictionary
                if((isinstance(dict[key], list)) and (key != "classNames")):#if the child is a list and not a className list,
                    for d in dict[key]: #call the recursive function on each dictionary inside the list
                            searchViewsCompound(d, matchedViews, selectors, parentSelectors, isChain);
                elif((isinstance(dict[key], list)) and (key == "classNames")):#if the child is a list and is a classnames list and classnames are being searched for
                        for cn in dict[key]:
                            for sel in selectors:  # compare with each selector
                                if (cn == sel[1:len(sel)]):#compare with the selecter's '.' removed
                                    if(parentSelectors > 0):#if there are remaining parents to be found
                                        parentSelectors -= 1;#one less to find
                                        selectors.pop(0);  # remove the parent from the list of ones to find
                                    matchNum += 1;  # a matching class name so save the dictionary


                elif (isinstance(dict[key], collections.abc.Mapping)):#if the child is a dictionary
                    searchViewsCompound(dict[key], matchedViews, selectors, parentSelectors, isChain);

                #at this point the child or children are either a class or a id (strings)

                elif(getKeyAttributeType(key) == Attribute.CLASS):#if it's a class
                        for sel in selectors:#go through the selectors
                            if(dict[key] == sel):
                                if (parentSelectors > 0):  # if there are remaining parents to be found
                                    parentSelectors -= 1;  # one less to find
                                    selectors.pop(0);#remove the parent from the list of ones to find
                                matchNum += 1;  # a matching class name so save the dictionary
                elif(getKeyAttributeType(key) == Attribute.IDENTIFIER):#it's an ID and therefore the first char (#) in the selector must be truncated
                        for sel in selectors:#go through the selectors
                            if(dict[key] == sel[1:len(sel)]):#remove '#'
                                if (parentSelectors > 0):  # if there are remaining parents to be found
                                    parentSelectors -= 1;  # one less to find
                                    selectors.pop(0);#remove the parent from the list of ones to find
                                matchNum += 1;  # a matching class name so save the dictionary

    if(matchNum >= len(selectors)):#if the selector is single or compound and was found in the dictionary
        matchedViews.append(dict);#the dictionary matches the selector

    return 0;

#-----program begins here by opening the json file-----
with open("SystemViewController.json", "r") as read_file:
    data = json.load(read_file);

    splitSelectors = [];# array to hold the split selectors
    matchedViews = [];#array of matching views in json form

    selectors = input();#user input

    if(getSelectorType(selectors) == Selector.CHAIN):
        selectors = selectors.split();
        searchViewsCompound(data, matchedViews, selectors, len(selectors)-1, 1);
    else:
        selectorBreakup(selectors, splitSelectors);#selector is single or compound
        searchViewsCompound(data, matchedViews, splitSelectors, 0, 0);

    for v in matchedViews:#output results
        print(v);
        print("\n");
    print("{} results were found.".format(len(matchedViews)));

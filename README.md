# Cantina Code Exercise

Overview:
The purpose of this project is to parse data from a JSON file representing a view hierarchy.
Once parsed, any views matching the selectors will be outputed.
The program is run in the command line.

Usage: 
Users give the the program either a single, compound, or chain selector.
Selectors can be made up of Class, ClassNames, or Identifiers.
Class must come first if included and Classnames and Identifiers must start with '.'or '#' characters respectively.

Notes:
The program assumes a JSON file with the name "SystemViewController.json" is in the same folder as the code.
The JSON file must be structed in the same way as the sample one.

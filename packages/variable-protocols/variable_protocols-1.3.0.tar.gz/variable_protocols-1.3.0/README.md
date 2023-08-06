# Variable Protocols
A way to specify common variables of data inputs in the field of data science and machine learning.

## Installation
`pip install variale_protocols`

## Specifications:
### Principles
* Only one representation for each variable type
* See `variable_protocols/variable_protocols.py`
### Guideline
* Use functions in `variables.py` to create variables
* 'VariableGroup' groups different type of Variables
* 'VariableTensor' groups same type of Variables

## Examples
see `test/examples.py`

## Goals
* specify common variables of data inputs in the field of data science and machine learning.
* structural typing, only sum types and product types (In the general sense, not ML family ADT)
* there should be one way to type one variable group
* good error messages
  * error (messages) oriented programming
* serialization in the future (probably in Dhall)

## NonGoals
* compatability with any current stuff
* easy to optimize with current computer architectures
* easy to comprehend (simple is not easy)
* support nominal typing(only labels)
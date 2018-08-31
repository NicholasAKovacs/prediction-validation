# My Solution to the Insight Data Engineering - Coding Challenge
This is a quick solution to the coding challenge offered by Inight to be considered further to become a Inight Data Engineering fellow

## Approach
1.) Read in 3 files as inputs with the descriptions:
* Window : Integer of window length
* Actual : Actual prices for stocks, arranged as Hour|Stock|Price
* Predicted : Predicted prices for stocks, arranged as Hour|Stock|Price

2.) Make 2 nested dictionaries, one for actual prices and the other for predicted prices arranged as follows:

{Hour1: {Stock1 : Price1}, {Stock2: Price2}, ... }{Hour2: {Stock1 : Price1}, {Stock2: Price2}, ... }

3.) Calculate the diffence in price (error) for each stock at every hour. Nested dictionary structure is same as above. This dictionary does not contain stocks for which there is not data for both the actual and predicted as a particular hour.

4.) For each window length, sum all the prices of the stocks and divide by the total number of stocks calculated. This is the error over the entire window.

5.) Write to output file arranged as follows:

Hour|Hour+Window|Error

## Dependenencies
Written in Python3 and uses the module:
Argparse

## Run Instructions
In the root directory of this repo run:
$ ./run.sh
If you have both python2 and python3, you will need to specify which one in ./run.sh

## Comments
This code did not pass the test because my calculations were off by 0.01 in some instances due to rounding differences between my algorithm and Inights algorithm. To imporove this code I would have used pandas, especially the groupby and merge functions.

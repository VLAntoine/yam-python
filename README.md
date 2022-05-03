# Yam's game in Python   

The yam's game in solo.

## Rules   

The objective of the game is to score points by rolling dice and filling a grid.

Every turn :
- you start rolling all the dices ;
- you can choose some dices and roll them again ;
- when you want or when you've already rolled the dices 3 times (1rst roll included), you choose a box to fill in the grid (you must fill one and only one box which is not filled yet) :
  -  in the "free" column : as you want ;
  -  in the "ascending" column : from the bottom ("yahtzee") to the top ("one") ;
  -  in the "descending" column : from the top ("one") to the bottom ("yahtzee") ;
  -  in the "bet" column : after the first roll, you choose a box in this column which will be filled after the 3 rolls. If you choose a box to bet on, you must fill this box at the end of the turn (you can't choose another box to fill) ;   

The grid is filled as followed :
- the upper section : 
  - the score in each of these boxes is determined by adding the total number of dice matching that box 
  - you get a bonus of 30 points if the sum of all the filled boxes in the column is greater than 60 ;
- the medium section :
  - the score of this boxes consist in the sum of all the dices at the end of the turn ;
  - if the minimum score box is greater or equal than the maximum score box in one column, the total medium section score of this colum is equal to zero ;
- the lower section :
  - fullhouse : 20 if the dices hand at the end contains 3 dices of one value and 2 of another (this 2 values can be the same, i.e a yahtzee is a fullhouse, 0 otherwise ;
  - four-of-a-kind : 30 if the dices hand at the end contains 4 dices of the same value (a yahtzee is a four-of-a-kind), 0 otherwise ;
  - straight : 40 if the dices hand at the end contains 1, 2, 3, 4, and 5, or 2, 3, 4, 5 and 6, 0 otherwise ;
  - yahtzee : 50 if the dices hand at the end contains 5 dices of the same value, 0 otherwise.

The game ends when the grid is fully filled.
Your final score is the sum of all the intermediate scores.

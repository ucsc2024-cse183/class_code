In your class-assigned github repo, in the assignment3 folder, create a file `index.html` (and a file `tictactoe.js`). The file should implement a tic-tac-toe game using only HTML, CSS, and JS. The user will be able to play against the computer.

The internal state of the game will be represeted by an object
```
board = [["", "", ""], ["", "", ""], ["", "", ""]];
```
When the user clicks on cell 1,2 then `board[1][2] = 'X'.
When the computer clicks on cell 2,0 then `board[2][0] = 'O'.

- it chould be made of valid HTML and CSS. (1 point)
- it should use vue.js (1 point)
- the UI of the game should consists of 9 cells organized in 3 rows of 3 columns each. (1 point)
- each cell chould contain a button of class `cell-i-j` where i,j is the cell index. (1 point)
- each button should display the state of the correspoding cell '', 'X' or 'O'. (1 point)
- users can only play empty cells (1 point)
- computers will play immediately after the user. (1 point)
- it should not be possible to play the same cell twice or play a cell already plyed by the other party (1 point)
- the computer should never lose. (2 point)
- there should be a button of class "reset" that when clicked, resets the game. (2 point)


Within these requirements you can be creative.
Commit your code and push it to your class-assigned github repo.

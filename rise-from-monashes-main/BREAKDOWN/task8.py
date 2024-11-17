                         # array of dollar indicators
BERYL_MAZE = [
  [300, -13, 189, -15, -12, 203, -23, 587, -78, 321, -46],
  [300, -11, -13, -24, 365, 198, -34, -21, 789, -81, -53],
  [300, -12, 112, -46, -76, -11, -23, -59, 321, 204, -32],
  [300, -23, 235, -12, -89, -62, -34, 212, -56, -67, -89],
  [300, 376, -23, -77, 227, -99, 134, 289, -12, 476, -51]
]

# getting the location of the agent.
location = input("Enter a row and column location for your character in the format x,y:\n").split(",")

row = int(location[0]); column = int(location[1])

# getting the desired direction the agent wants to move in.
desiredDirection = input("Choose a direction:\n")

# getting the dollar indicator digit to find within the maze.
dollarIndicator = input("Choose a Dollar Indicator digit to find:\n")

# storing coordinates and dollar indicators 
coordinates = []; indicators = []
foundDigit = False # sentinel

# if the user chooses to go right.
if desiredDirection == "right":
  
  for index in range(column + 1, len(BERYL_MAZE[row])): # looping through each column of the same row.
    if dollarIndicator not in str(BERYL_MAZE[row][index]): 
      coordinates.append( (row, index) )
      indicators.append( BERYL_MAZE[row][index] )
    
    else:
      coordinates.append( (row, index) )
      indicators.append( BERYL_MAZE[row][index] )
      print(f"Visited {coordinates} with corresponding Dollar Indicators {indicators}")
      print(f"Found digit at location {(row, index)}")
      foundDigit = True
      break
  
  if not foundDigit:
    print(f"Entered restricted area!\nReturned to location {(row,column)}")
    
# if the user chooses to go up.    
elif desiredDirection == "up":
  for index in range(row-1, -1,-1):  # looping through each row of the same column, upwards.
    if dollarIndicator not in str(BERYL_MAZE[index][column]):
      coordinates.append( (index, column) )
      indicators.append( BERYL_MAZE[index][column] )
      
    else:
      coordinates.append( (index, column) )
      indicators.append( BERYL_MAZE[index][column] )
      print(f"Visited {coordinates} with corresponding Dollar Indicators {indicators}")
      print(f"Found digit at location {(index, column)}")
      foundDigit = True
      break
  
  if not foundDigit:
    print(f"Entered restricted area!\nReturned to location {(row,column)}")

# if the user chooses to go down.  
elif desiredDirection == "down":
  for index in range(row+1, len(BERYL_MAZE)):  # looping through each row of the same column, downwards.
    if dollarIndicator not in str(BERYL_MAZE[index][column]):
      coordinates.append( (index, column) )
      indicators.append( BERYL_MAZE[index][column] )
      
    else:
      coordinates.append( (index, column) )
      indicators.append( BERYL_MAZE[index][column] )
      print(f"Visited {coordinates} with corresponding Dollar Indicators {indicators}")
      print(f"Found digit at location {(index, column)}")
      foundDigit = True
      break
  
  if not foundDigit:
    print(f"Entered restricted area!\nReturned to location {(row,column)}")

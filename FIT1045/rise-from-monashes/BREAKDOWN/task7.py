# array of dollar indicators
BERYL_MAZE = [
  [300, -13, 189, -15, -12, 203, -23, 587, -78, 321, -46],
  [300, -11, -13, -24, 365, 198, -34, -21, 789, -81, -53],
  [300, -12, 112, -46, -76, -11, -23, -59, 321, 204, -32],
  [300, -23, 235, -12, -89, -62, -34, 212, -56, -67, -89],
  [300, 376, -23, -77, 227, -99, 134, 289, -12, 476, -51]
]

# getting the desired position the user wants, and then creating a list that stores the row and column of the desired position.
desiredPosition = list(map(int, input("Enter a row and column location for your character in the format x,y:\n").split(",")))

# reprompting users to enter correct position if the row and/or column is out of range.
while(desiredPosition[0] < 0 or desiredPosition[1] < 0 or desiredPosition[0] >= len(BERYL_MAZE) or desiredPosition[1] >= len(BERYL_MAZE[0])):
    desiredPosition = list(map(int, input("Position chosen is invalid. Try again!\nEnter a row and column location for your character in the format x,y:\n").split(",")))

# getting the user's input and appending it to the desired position of the dollar indicators array.
characterName = input("Enter a character name:\n")
BERYL_MAZE[desiredPosition[0]][desiredPosition[1]] = "<" + characterName.upper()[0] + ">"

# printing the overall array with the new changes.
for i in range(len(BERYL_MAZE)):
    for j in range(len(BERYL_MAZE[0])):
        print(BERYL_MAZE[i][j], end="   ")
    print()

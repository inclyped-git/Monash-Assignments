/*
* @author inclyped
*/


import java.util.Scanner;

public class GameDriver {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in); // instantiating a new Scanner object
        Team[] teamsCreated = new Team[6]; // Declaring and defining an array to store 6 teams.

        // asking the user to enter the names for all the six teams created.
        for (int i = 0; i < teamsCreated.length; i++)
        {
            System.out.println("Enter the name of team " + (i+1));
            teamsCreated[i] = new Team(sc.next());
        }

        // Loops through each team element by element inside the teamsCreated[]
        for (Team firstTeam: teamsCreated)
        {
            for (Team secondTeam: teamsCreated)
            {
                // we do not want the same team to play itself.
                if (firstTeam.equals(secondTeam)) {continue;}

                // if they are different teams, then create a Game object that enables the two teams to play against each other.
                Game currentGame = new Game(firstTeam, secondTeam);

                currentGame.playGame(); // play game method is called.
                currentGame.finalScoreBoard(secondTeam, firstTeam); // printing the final scoreboard of each game.
            }
        }

        for (Team team: teamsCreated)
        {
            System.out.println(team.toString()); // printing the team names and statistics.
        }
    }
}


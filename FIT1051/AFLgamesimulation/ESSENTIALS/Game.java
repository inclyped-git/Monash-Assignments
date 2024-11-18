/**
 * Description: This class contains the attributes that simulate a game being played in the AFL. The
 *              class keeps track of the two teams playing during the game, and their current scores
 *              during the game.
 * @author inclyped
 * @version 21.0.1
 */

public class Game {

    // attributes of a Game object.
    private final Team TEAM_1;
    private final Team TEAM_2;
    private int currentScoreTeam1;
    private int currentScoreTeam2;

    // Class variable.
    private static Team winner;

    // constructors for Game class.
    /**
     * Description: Default constructor to set default states for all attributes of a Game object.
     */
    public Game()
    {
        this.TEAM_1 = null;
        this.TEAM_2 = null;
        this.currentScoreTeam1 = 0;
        this.currentScoreTeam2 = 0;
    }

    /**
     * Description: Non-default constructor to set non-default states for all attributes of a Game object.
     This constructor is useful when a new game is created.d
     * @param Team team1: Team 1 playing the game.
     * @param Team team2: Team 2 playing the game.
     */
    public Game(Team team1, Team team2)
    {
        this.TEAM_1 = team1;
        this.TEAM_2 = team2;
        this.currentScoreTeam1 = 0;
        this.currentScoreTeam2 = 0;
    }

    /**
     * Description: Non-default constructor to set non-default states for all attributes of a Game object.
     This constructor is useful when a game is already occurring, and we would want to continue
     simulating the game.
     * @param Team team1: Team 1 playing the game.
     * @param Team team2: Team 2 playing the game.
     * @param int currentScoreTeam1: Current score for Team 1.
     * @param int currentScoreTeam2: Current score for Team 2.
     */
    public Game(Team team1, Team team2, int currentScoreTeam1, int currentScoreTeam2) // if the game already exists.
    {
        this.TEAM_1 = team1;
        this.TEAM_2 = team2;
        this.currentScoreTeam1 = currentScoreTeam1;
        this.currentScoreTeam2 = currentScoreTeam2;
    }

    // accessor methods for Game class.
    /**
     * Description: Getter method for the attribute 'TEAM_1'
     * @return Team: One of the teams playing in the game.
     */
    public Team getTeam1() {
        return TEAM_1;
    }

    /**
     * Description: Getter method for the attribute 'TEAM_2'
     * @return Team: The other team that is playing in the game.
     */
    public Team getTeam2() {
        return TEAM_2;
    }

    /**
     * Description: Getter method for the attribute 'currentScoreTeam1'
     * @return int: The current score for team 1.
     */
    public int getCurrentScoreTeam1() {
        return currentScoreTeam1;
    }

    /**
     * Description: Getter method for the attribute 'currentScoreTeam2'
     * @return int: The current score for team 2.
     */
    public int getCurrentScoreTeam2() {
        return currentScoreTeam2;
    }

    // mutator methods for Game class.
    /**
     * Description: Setter method for the attribute 'currentScoreTeam1'
     * @param int currentScoreTeam1: The current score for team 1.
     */
    public void setCurrentScoreTeam1(int currentScoreTeam1) {
        this.currentScoreTeam1 = currentScoreTeam1;
    }

    /**
     * Description: Setter method for the attribute 'currentScoreTeam2'
     * @param int currentScoreTeam2: The current score for team 2.
     */
    public void setCurrentScoreTeam2(int currentScoreTeam2) {
        this.currentScoreTeam2 = currentScoreTeam2;
    }

    /**
     * Description: Represent the state of the Game object in a String format.
     * @return String: A string representation of the Game object.
     */
    public String toString()
    {
        return String.format("-----%nScoreboard:%n%s:   %d%n%s:   %d%n-----",this.getTeam1().getTeamName(), this.getCurrentScoreTeam1(), this.getTeam2().getTeamName(), this.getCurrentScoreTeam2());
    }

    /**
     * Description: This method allows to simulate an AFL game, where it is played for 80 minutes.
     *              It simulates the game, and prints out if any team scores a goal or a behind
     *              during the game.
     */
    public void playGame()
    {
        int minutes = 0; // keeps track of the minutes of the game.
        String finalString = "";
        System.out.println("KICKOFF STARTS!");
        while (minutes < 81)
        {
            int randomNumber = this.randomChanceGenerator(); // generates a random integer from 1-100

            if (randomNumber >= 1 && randomNumber <= 14) // if the number is between 1-14, team 1 scores a goal.
            {
                this.scoreGoal(this.getTeam1());
                finalString = String.format("%s scores a goal against %s%n", getTeam1().getTeamName(), getTeam2().getTeamName());
            }
            else if (randomNumber >= 15 && randomNumber <= 32) // if the number is between 15-32, team 1 scores a behind.
            {
                this.scoreBehind(this.getTeam1());
                finalString = String.format("%s scores a behind against %s%n", getTeam1().getTeamName(), getTeam2().getTeamName());
            }
            else if (randomNumber >= 50 && randomNumber <= 63) // if the number is between 50-63, team 2 scores a goal.
            {
                this.scoreGoal(this.getTeam2());
                finalString = String.format("%s scores a goal against %s%n", getTeam2().getTeamName(), getTeam1().getTeamName());
            }
            else if (randomNumber >= 64 && randomNumber <= 81) // if the number is between 64-81, team 2 scores a behind.
            {
                this.scoreBehind(this.getTeam2());
                finalString = String.format("%s scores a behind against %s%n", getTeam2().getTeamName(), getTeam1().getTeamName());
            }
            System.out.println(finalString);
            System.out.println(this.toString());
            minutes++; // incrementing minutes
        }

        // if team 1 has a higher score than team 2, update team 1 wins and team 2 losses
        if (this.getCurrentScoreTeam1() > this.getCurrentScoreTeam2())
            { this.updateWins(this.getTeam1()); this.updateLosses(this.getTeam2()); winner = this.getTeam1(); }
        else if (this.getCurrentScoreTeam1() == this.getCurrentScoreTeam2()) // if team 1 and team 2 has the same score, update draws for both teams.
            { this.updateDraws(this.getTeam1()); this.updateDraws(this.getTeam2()); }
        else // otherwise, update team 1 wins and update team 2 losses
            { this.updateWins(this.getTeam2()); this.updateLosses(this.getTeam1()); winner = this.getTeam2(); }
    }


    /**
     * Description: Updates a team's points when they score a goal.
     * @param Team team: The team that scored a goal.
     */
    public void scoreGoal(Team team)
    {
        if (team.equals(this.TEAM_1)) { this.currentScoreTeam1 = this.getCurrentScoreTeam1() + 6; }
        else { this.currentScoreTeam2 = this.getCurrentScoreTeam2() + 6; }
    }

    /**
     * Description: Updates a team's points when they score a behind.
     * @param Team team: The team that scored a behind.
     */
    public void scoreBehind(Team team)
    {
        if (team.equals(this.TEAM_1)) { this.currentScoreTeam1 = this.getCurrentScoreTeam1() + 1; }
        else { this.currentScoreTeam2 = this.getCurrentScoreTeam2() + 1; }
    }

    /**
     * Description: Returns a random number from 1 - 100
     * @return int: A random integer from 1-100.
     */
    public int randomChanceGenerator()
    {
        return (int) ( Math.random() * 100 + 1);
    }

    /**
     * Description: Updates the team wins by incrementing them.
     * @param Team team: The team that won the game.
     */
    public void updateWins(Team team)
    {
        team.setTeamWins(team.getTeamWins() + 1);
    }

    /**
     * Description: Updates the team losses by incrementing them.
     * @param Team team: The team that lost the game.
     */
    public void updateLosses(Team team)
    {
        team.setTeamLosses(team.getTeamLosses() + 1);
    }

    /**
     * Description: Updates the team draws by incrementing them.
     * @param Team team: The team that drew the game.
     */
    public void updateDraws(Team team)
    {
        team.setTeamDraws(team.getTeamDraws() + 1);
    }

    /**
     * Description: Prints a string that consists of the final scoreboard for teams to see.
     * @param Team team1: Team 1 that played the game.
     * @param Team team2: Team 2 that played the game.
     */
    public void finalScoreBoard(Team team1, Team team2)
    {
        System.out.println(String.format("Final Scoreboard:%n%s: %d points%n%s: %d points%n%n", team1.getTeamName(), this.getCurrentScoreTeam1(), team2.getTeamName(), this.getCurrentScoreTeam2()) +
                String.format("Winner: %s%n%n", winner.getTeamName()));
    }

}

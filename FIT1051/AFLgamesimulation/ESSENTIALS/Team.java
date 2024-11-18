/**
 * Description: This class contains the attributes that simulate a team playing in the AFL. The class
 *              keeps track of each team's name, and their overall statistics (wins/losses/draws).
 * @author inclyped
 * @version 21.0.1
 */

public class Team {

    // attributes of a Team object.
    private final String TEAM_NAME; // never mutates
    private int teamWins;
    private int teamLosses;
    private int teamDraws;

    // constructors for Team class.
    /**
     * Description: Default constructor to set default states for all attributes of a Team object.
     */
    public Team()
    {
        this.TEAM_NAME = "";
        this.teamWins = 0;
        this.teamLosses = 0;
        this.teamDraws = 0;
    }

    /**
     * Description: Non-default constructor to set non-default states for all attributes of a Team object.
     This constructor is useful when a new team is created.

     * @param String teamName: The name of the team.
     */
    public Team(String teamName)
    {
        this.TEAM_NAME = teamName;
        this.teamWins = 0;
        this.teamLosses = 0;
        this.teamDraws = 0;
    }

    /**
     * Description: Non-default constructor to set non-default states for all attributes of a Team object.
     This constructor is useful when an existing team exists, and a Team object is required
     to create.

     * @param String teamName: The name of the team.
     * @param int teamWins: The number of wins the team has.
     * @param int teamLosses: The number of losses the team has.
     * @param int teamDraws: The number of draws the team has.
     */
    public Team(String teamName, int teamWins, int teamLosses, int teamDraws)
    {
        this.TEAM_NAME = teamName;
        this.teamWins = teamWins;
        this.teamLosses = teamLosses;
        this.teamDraws = teamDraws;
    }

    // accessor methods for Team class.
    /**
     * Description: Getter method for the attribute 'TEAM_NAME'
     * @return String: String format of the team name.
     */
    public String getTeamName() {
        return TEAM_NAME;
    }

    /**
     * Description: Getter method for the attribute 'teamWins'
     * @return int: The number of wins for a team.
     */
    public int getTeamWins() {
        return teamWins;
    }

    /**
     * Description: Getter method for the attribute 'teamLosses'
     * @return int: The number of losses for the team.
     */
    public int getTeamLosses() {
        return teamLosses;
    }

    /**
     * Description: Getter method for the attribute 'teamDraws'.
     * @return int: The number of draws for the team.
     */
    public int getTeamDraws() {
        return teamDraws;
    }

    // mutator methods
    /**
     * Description: Setter method for the attribute 'teamWins'
     * @param int teamWins: The number of wins for the team.
     */
    public void setTeamWins(int teamWins) {
        this.teamWins = teamWins;
    }

    /**
     * Description: Setter method for the attribute 'teamLosses'
     * @param int teamLosses: The number of losses for the team.
     */
    public void setTeamLosses(int teamLosses) {
        this.teamLosses = teamLosses;
    }

    /**
     * Description: Setter method for the attribute 'teamDraws'
     * @param int teamDraws: The number of draws for the team.
     */
    public void setTeamDraws(int teamDraws) {
        this.teamDraws = teamDraws;
    }

    /**
     * Description: toString() method to print the details and information about a Team object.
     * @return String: The states of the object presented in the form of a String.
     */
    public String toString()
    {
        return String.format("*****%nTeam Name: %s%nTeam Statistics: %d wins, %d losses, %d draws%n*****", this.getTeamName(), this.getTeamWins(), this.getTeamLosses(), this.getTeamDraws());
    }
}

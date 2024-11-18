/**
 * FoodItem abstract class contains the template that is inherited and implemented
 * by child classes.
 * @author inclyped
 * @version 21.0.1
 */

public abstract class FoodItem implements Usable {

    /**
     * The function returns the total cost of the pizza or pasta.
     * @return double: The total cost.
     */
    abstract double getItemCost();

    /**
     * The function sets the item cost for a pizza or pasta.
     * @param cost: The cost of the pizza or pasta.
     */
    abstract void setItemCost(double cost);

    /**
     * Gets the food type of the food item.
     * @return MEAL_TYPE: The food type of the food item.
     */
    abstract MEAL_TYPE getItemType();

    /**
     * The function sets the meal type of the food item.
     * @param type: The type of the food item the program sets.
     */
    abstract void setItemType(MEAL_TYPE type);

    /**
     * Returns the states of the object in a string format.
     * @return String: The states of the object are visible in a string format.
     */
    public abstract String toString();

    /**
     * Checks if the food item is a meat or not.
     * @return boolean: Returns true if the food item is a meat or not.
     */
    abstract boolean isItemMeat();

    /**
     * Checks if the food item is a vegetarian or not.
     * @return boolean: Returns true if the food item is vegetarian.
     */
    abstract boolean isItemVegetarian();

    /**
     * Finds the type of the food item and returns the food type.
     * @return MEAL_TYPE: Returns the food type.
     */
    abstract MEAL_TYPE findItemType();

}

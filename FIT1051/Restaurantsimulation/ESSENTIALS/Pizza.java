/**
 * Pizza subclass of the FoodItem class contains the attributes and behaviours
 * that represent pizza in the Restaurant Simulation.
 * @author inclyped
 * @version 21.0.1
 */

// importing arraylist object to the program
import java.util.ArrayList;

public class Pizza extends FoodItem implements Usable {

    // non-static fields.
    private ArrayList<PIZZA_TOPPINGS> pizzaToppings;
    private MEAL_TYPE pizzaType;
    private double pizzaCost;

    // default constructor for the Pizza class.
    public Pizza()
    {
        this.pizzaToppings = new ArrayList<>();
        this.pizzaType = MEAL_TYPE.VEGAN;
        this.pizzaCost = basePrice;
    }

    // non-default constructor for the Pizza class.
    public Pizza(ArrayList<PIZZA_TOPPINGS> toppings, MEAL_TYPE type, double cost)
    {
        this.pizzaToppings = toppings;
        this.pizzaType = type;
        this.pizzaCost = cost;
    }

    // Mutators for the Pizza class.
    public void setPizzaToppings(ArrayList<PIZZA_TOPPINGS> toppings)
    {
        this.pizzaToppings = toppings;
    }

    public void setItemType(MEAL_TYPE type)
    {
        this.pizzaType = type;
    }

    public void setItemCost(double cost)
    {
        this.pizzaCost = cost;
    }

    // Accessors for the Pizza class.
    public ArrayList<PIZZA_TOPPINGS> getPizzaToppings()
    {
        return this.pizzaToppings;
    }

    public MEAL_TYPE getItemType()
    {
        return this.pizzaType;
    }

    public double getItemCost()
    {
        return this.pizzaCost;
    }

    // toString() method for the Pizza class.
    public String toString()
    {
        String finalString = "";
        finalString += String.format("Pizza%nType: %s%nCost: %f%nList of toppings: ", this.pizzaType, this.pizzaCost);

        for (PIZZA_TOPPINGS topping: this.pizzaToppings)
        {
            finalString += topping.name() + "\n";
        }

        return finalString;
    }

    // Extra behaviours for the Pizza class.

    /**
     * Adds toppings to the pizza if it is not already added.
     * @param topping: The topping to be added.
     */
    public void addPizzaTopping( PIZZA_TOPPINGS topping )
    {
        // if the topping is not in the pizza,
        if (!this.pizzaToppings.contains(topping))
        {
            // updating states accordingly.
            this.pizzaToppings.add(topping);
            this.pizzaCost += this.findPizzaToppingCost(topping);
            this.pizzaType = this.findItemType();
            System.out.println("Added " + topping.name());
        }
        else // otherwise print a warning.
        {
            System.out.println("Topping already added!");
        }
    }

    /**
     * Finds the topping added on the pizza, and returns the price of the topping
     * accordingly.
     * @param topping: The topping being added to the pizza.
     * @return double: The price of the topping.
     */
    private double findPizzaToppingCost( PIZZA_TOPPINGS topping )
    {
        if (topping.equals(PIZZA_TOPPINGS.PINEAPPLE))
            return 2.50;
        else if (topping.equals(PIZZA_TOPPINGS.SEAFOOD))
            return 3.50;
        else
            return 2.00;
    }

    /**
     * Finds the pizza type.
     * @return MEAL_TYPE: The food type of the pizza object.
     */
    public MEAL_TYPE findItemType()
    {
        if (this.isItemMeat())
        {
            return MEAL_TYPE.MEAT;
        }
        else if (this.isItemVegetarian())
        {
            return MEAL_TYPE.VEGETARIAN;
        }
        else
        {
            return MEAL_TYPE.VEGAN;
        }
    }

    /**
     * Checks if the pizza object is a meat item or not.
     * @return boolean: True if the pizza is meat.
     */
    public boolean isItemMeat()
    {
        boolean containsMeat = false;
        for (PIZZA_TOPPINGS topping: this.pizzaToppings)
        {
            // if the pizza topping has meat, containsMeat is changed to true.
            if (topping.equals(PIZZA_TOPPINGS.HAM) || topping.equals(PIZZA_TOPPINGS.SEAFOOD)) {
                containsMeat = true;
                break;
            }
        }
        return containsMeat; // else return false.
    }

    /**
     * Checks if the pizza object is a vegetarian, given that there is no meat.
     * @return boolean: Returns true if the item is a vegetarian, given that there is no meat
     * topping.
     */
    public boolean isItemVegetarian()
    {
        boolean containsVegetarian = false;
        for (PIZZA_TOPPINGS topping: this.pizzaToppings)
        {
            // if the food item is not a meat and if its cheese, return true.
            if (!this.isItemMeat() && (topping.equals(PIZZA_TOPPINGS.CHEESE)))
            {
                containsVegetarian = true;
            }
        }
        return containsVegetarian; // else return false.
    }

}

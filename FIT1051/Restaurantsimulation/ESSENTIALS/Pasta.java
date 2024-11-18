/**
 * Pasta subclass of the FoodItem class contains the attributes and behaviours that
 * represent pasta in the Restaurant Simulation.
 * @author inclyped
 * @version 21.0.1
 */
public class Pasta extends FoodItem implements Usable {

    // non-static fields
    private PASTA_TOPPINGS pastaTopping;
    private MEAL_TYPE pastaType;
    private double pastaCost;

    // default constructor for the Pasta class.
    public Pasta()
    {
        this.pastaTopping = null;
        this.pastaType = MEAL_TYPE.VEGAN;
        this.pastaCost = basePrice;
    }

    // non-default constructor for the Pasta class.
    public Pasta(PASTA_TOPPINGS topping, MEAL_TYPE type, double cost)
    {
        this.pastaTopping = topping;
        this.pastaType = type;
        this.pastaCost = cost;
    }

    // Mutator methods for the Pasta class.
    public void setPastaTopping(PASTA_TOPPINGS topping)
    {
        this.pastaTopping = topping;
    }

    public void setItemType(MEAL_TYPE type)
    {
        this.pastaType = type;
    }

    public void setItemCost(double cost)
    {
        this.pastaCost = cost;
    }

    // Accessor methods for the Pasta class.
    public PASTA_TOPPINGS getPastaTopping()
    {
        return this.pastaTopping;
    }

    public MEAL_TYPE getItemType()
    {
        return this.pastaType;
    }

    public double getItemCost()
    {
        return this.pastaCost;
    }

    // toString() method for the Pasta class.
    public String toString()
    {
        return String.format("Pasta%nType: %s%nCost: %f%nTopping: %s", this.pastaType, this.pastaCost, this.pastaTopping);
    }

    /**
     * Adds a pasta topping if there is no topping.
     * @param topping: Pasta topping the customer wants.
     */
    public void addPastaTopping (PASTA_TOPPINGS topping )
    {
        if (this.pastaTopping == null) // if there is no topping.
        {
            this.setPastaTopping(topping);
            this.pastaCost += this.findPastaToppingCost(topping);
            this.pastaType = this.findItemType();
            System.out.println("Added " + topping.name());
        }
        else // otherwise print a warning.
        {
            System.out.println("Topping is already on the pasta!");
        }
    }

    /**
     * Finds the pasta topping cost from the topping added to the pasta.
     * @param topping: The topping added to the pasta.
     * @return double: The cost of the topping.
     */
    private double findPastaToppingCost( PASTA_TOPPINGS topping )
    {
        if(topping.equals(PASTA_TOPPINGS.TOMATO))
            return 4.00;
        else if (topping.equals(PASTA_TOPPINGS.BOLOGNESE) || topping.equals(PASTA_TOPPINGS.PRIMAVERA))
            return 5.20;
        else
            return 6.80;
    }

    /**
     * Checks if the pasta contains meat.
     * @return boolean: Returns true if the pasta contains meat.
     */
    public boolean isItemMeat()
    {
        return this.pastaTopping.equals(PASTA_TOPPINGS.BOLOGNESE) || this.pastaTopping.equals(PASTA_TOPPINGS.MARINARA);
    }

    /**
     * Checks if the pasta contains vegetarian given that it is not meat.
     * @return boolean: True if the topping contains vegetarian and not meat.
     */
    public boolean isItemVegetarian()
    {
        return !this.isItemMeat() && this.pastaTopping.equals(PASTA_TOPPINGS.PRIMAVERA);
    }

    /**
     * Finds the food type of the pasta based on its toppings.
     * @return MEAL_TYPE: The type of pasta ordered.
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

}

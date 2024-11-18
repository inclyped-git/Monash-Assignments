/**
 * Order class contains attributes and behaviours that represents a
 * Customer object's order of a list of pizzas and/or pastas.
 * @author inclyped
 * @version 21.0.1
 */

// Importing Arraylist object to the program.
import java.util.ArrayList;

public class Order implements Usable {

    // non-static fields for the Order class.
    private ArrayList<FoodItem> orderFoodItems;
    private Customer orderCustomer;
    private MEAL_TYPE orderType;
    private double orderTotalCost;

    // Default Order constructor.
    public Order()
    {
        this.orderFoodItems = new ArrayList<>();
        this.orderCustomer = new Customer();
        this.orderType = null;
        this.orderTotalCost = 0;
    }

    // Non-default Order constructor.
    public Order(String customerName, String customerContactNumber, String customerDeliveryAddress)
    {
        this.orderFoodItems = new ArrayList<>();
        this.orderCustomer = new Customer(customerName, customerContactNumber, customerDeliveryAddress);
        this.orderType = null;
        this.orderTotalCost = 0;
    }

    // Mutators for the Order class.
    public void setFoodItems(ArrayList<FoodItem> foodItems)
    {
        this.orderFoodItems = foodItems;
    }

    public void setCustomer(Customer customer)
    {
        this.orderCustomer = customer;
    }

    public void setType(MEAL_TYPE type)
    {
        this.orderType = type;
    }

    public void setCost(double cost)
    {
        this.orderTotalCost = cost;
    }

    // Accessors for the Order class.
    public ArrayList<FoodItem> getFoodItems()
    {
        return this.orderFoodItems;
    }

    public Customer getCustomer()
    {
        return this.orderCustomer;
    }

    public MEAL_TYPE getType()
    {
        return this.orderType;
    }

    public double getCost()
    {
        return this.orderTotalCost;
    }

    // Order toString() method.
    public String toString()
    {
        String finalString = "";
        finalString += this.orderCustomer.toString() + "\n";
        finalString += String.format("Order type: %s%n", this.orderType);
        finalString += String.format("Total cost: %f%n", this.orderTotalCost);
        finalString += "Food items ordered: \n\n";

        // Printing each food item in the arraylist.
        for (FoodItem item: this.orderFoodItems)
        {
            finalString += item.toString() + "\n";
        }

        return finalString;
    }

    // Extra behaviours for the Order class.

    /**
     * Adds an unique food item to the object's arraylist.
     * @param item: The food item that is being stored inside the arraylist.
     */
    public void addFoodItem(FoodItem item)
    {
        // Does not add the food item if it already exists inside the arraylist.
        if (this.orderFoodItems.contains(item))
        {
            System.out.println("This item already exists in the order!");
        }
        else // if it is a distinct food item, add the item and update the object states.
        {
            this.orderFoodItems.add(item);
            this.orderTotalCost = this.getTotalFoodItemCost();
            this.orderType = this.findOrderType();
            System.out.println("Item added: " + item.toString());
        }
    }

    /**
     * Gets the total cost of the order by getting the sum of individual food item
     * prices.
     * @return double: The total cost of the order.
     */
    private double getTotalFoodItemCost()
    {
        // Assigning the state to 0 to prevent additional summation.
        this.orderTotalCost = 0;
        for (FoodItem item: this.orderFoodItems)
        {
            this.orderTotalCost += item.getItemCost();
        }
        return this.getCost();
    }

    /**
     * Checks if at least one food item in the order contains meat or not.
     * @return boolean: Returns True if there is any meat meal.
     */
    private boolean isOrderMeat()
    {
        for (FoodItem item: this.orderFoodItems)
        {
            if (item.getItemType().equals(MEAL_TYPE.MEAT))
            {
                return true; // if the item retrieved is a type of MEAT.
            }
        }
        return false; // return false if none of the FoodItem objects have type MEAT.
    }

    /**
     * Checks if there is any vegetarian meal, given that there is no meat meal.
     * @return boolean: Returns true if the description above is true.
     */
    private boolean isOrderVegetarian()
    {
        // only loops if there is no meat.
        while(!this.isOrderMeat())
        {
            for (FoodItem item: this.orderFoodItems)
            {
                if (item.getItemType().equals(MEAL_TYPE.VEGETARIAN))
                    return true; // returns true if there is at least one vegetarian.
            }
        }
        return false; // otherwise, return false.
    }

    /**
     * Finds the order type based on the food items stored inside the arraylist.
     * @return MEAL_TYPE: Returns the order type based on the food items.
     */
    private MEAL_TYPE findOrderType()
    {
        if (this.isOrderMeat())
            return MEAL_TYPE.MEAT;
        else if (this.isOrderVegetarian())
            return MEAL_TYPE.VEGETARIAN;
        else
            return MEAL_TYPE.VEGAN;
    }

}

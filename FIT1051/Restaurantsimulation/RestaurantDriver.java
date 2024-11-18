/**
 * Main driver class that runs the simulation.
 * @author inclyped
 * @version 21.0.1
 */

// import statements
import java.util.ArrayList;
import java.util.Scanner;

public class RestaurantDriver implements Usable {

    static Scanner sc = new Scanner(System.in); // variable sc allows the user to input in the console.
    private static ArrayList<Order> restaurantOrder = new ArrayList<Order>(); // Arraylist of order objects.

    public static void main(String[] args) {

        boolean wantsToExit = false; // sentinel variable that controls the while loop; used to check if the user wants to exit.

        System.out.println("Welcome to the Restaurant Simulation!\n");

        while (!wantsToExit) {

            // prints out the main menu
            System.out.println(printMainMenu());

            System.out.print("Choose your option: ");
            int optionChosen = sc.nextInt(); // asking user for choosing their option.

            if (optionChosen == 1) {
                takeOrder(); // take order
            } else if (optionChosen == 2) {
                deliverOrder(); // deliver order
            } else if (optionChosen == 3) {
                printAllOrder(); // print out the current orders.
            }
            else if (optionChosen == 4) {
                wantsToExit = true; // exit while loop.
            }
            else {
                System.out.println("Enter correct number again!"); // validation check.
            }
        }
    }

    /**
     * Creates a new Order object and adds it to the arraylist.
     */
    public static void takeOrder() {
        // adds the new order to the arraylist.
        Order order = createOrder();
        restaurantOrder.add(order);

        boolean wantsMoreToOrder = true; // sentinel variable that checks if the user wants to order more.

        while (wantsMoreToOrder) {

            System.out.print("\nChoose what you want: [1] - Pizza [2] - Pasta: ");
            int optionChosen = sc.nextInt();

            // validation check
            while (optionChosen < 1 || optionChosen > 2) {
                System.out.print("Wrong number entered. Enter again: [1] - Pizza [2] - Pasta: ");
                optionChosen = sc.nextInt();
            }

            // if option 1, they selected pizza.
            if (optionChosen == 1)
            {
                order.addFoodItem(orderPizza());
            }
            else // if option 2, they selected pasta.
            {
                order.addFoodItem(orderPasta());
            }

            System.out.print("\nDoes the customer want more to order: [1] - Yes [2] - No:  ");
            optionChosen = sc.nextInt(); // asks user if they want to order more.

            // validation check
            while (optionChosen < 1 || optionChosen > 2)
            {
                System.out.print("\nWrong number entered. Enter again: ([1] - Yes [2] - No): ");
                optionChosen = sc.nextInt();
            }

            if (optionChosen == 2) // if option 2, end the while loop.
            {
                wantsMoreToOrder = false;
            }
        }
    }

    /**
     * Creates a new pizza object and returns it to the arraylist.
     * @return Pizza: Pizza object with toppings of choice.
     */
    public static Pizza orderPizza()
    {
        System.out.println("Customer is ordering Pizza!");
        Pizza pizza = new Pizza();

        boolean wantsMoreTopping = true; // sentinel value that checks if the user keeps wanting to add more toppings.

        while (wantsMoreTopping) {

            // printing the topping options.
            String options = "";
            options += "[1] - Ham\n[2] - Cheese\n[3] - Pineapple\n[4] - Mushrooms\n[5] - Tomato\n[6] - Seafood\n";
            options += "Choose your topping preference: ";
            System.out.println(options);

            int optionChosen = sc.nextInt(); // asking user to choose their option.

            // validation check
            while (optionChosen < 1 || optionChosen > 6) {
                System.out.print("\nEnter the correct number: ");
                optionChosen = sc.nextInt();
            }

            // adding the pizza topping depending on the choice.
            pizzaToppingMethod(pizza, optionChosen);

            // printing the states of the pizza object.
            System.out.println(pizza.toString());

            // asking the user if they want more topping.
            System.out.print("\nDoes the customer want more topping? -> ([1] - Yes [2] - No): ");
            optionChosen = sc.nextInt();

            // validation check.
            while (optionChosen < 1 || optionChosen > 2)
            {
                System.out.print("\nEnter the correct number - ([1] - Yes [2] - No): ");
                optionChosen = sc.nextInt();
            }

            // if option 2, break the while loop.
            if(optionChosen == 2)
                wantsMoreTopping = false;
        }

        return pizza; // return pizza object.
    }

    /**
     * Creates a new pasta object and returns it to the arraylist.
     * @return Pasta: A pasta object with preferred topping.
     */
    public static Pasta orderPasta()
    {
        System.out.println("Customer is ordering Pasta!");
        Pasta pasta = new Pasta();

        // printing out the toppings options
        String options = "";
        options += "[1] - Bolognese\n[2] - Marinara\n[3] - Primavera\n[4] - Tomato\n";
        options += "Choose your topping preference: ";
        System.out.println(options);

        // asking the user to input.
        int optionChosen = sc.nextInt();
        while (optionChosen < 1 || optionChosen > 4)
        {
            System.out.print("\nEnter the correct number: ");
            optionChosen = sc.nextInt();
        }

        pastaToppingMethod(pasta, optionChosen);

        // printing the states of the pasta object.
        System.out.println(pasta.toString());
        return pasta;
    }

    /**
     * Delivers an order by removing the first element of the arraylist.
     */
    public static void deliverOrder() {
        System.out.printf("Order delivered : %n%s%n", restaurantOrder.remove(0).toString()); // removing the first element of the arraylist, since that is the first order.
    }

    /**
     * Prints all the orders of customers.
     */
    public static void printAllOrder()
    {
        if (restaurantOrder.isEmpty())
        {
            System.out.println("There are no orders!");
        }
        else
        // looping through each order object and printing their states.
        {
            for (Order order : restaurantOrder) {
                System.out.println(order.toString());
            }
        }
    }

    /**
     * Prints the main menu of the program.
     * @return String: Main menu.
     */
    public static String printMainMenu()
    {
        // printing the main menu
        String mainMenu = "";
        mainMenu += "Press the following numbers for preferred options: \n";
        mainMenu += "[1] - Take new order\n";
        mainMenu += "[2] - Deliver order\n";
        mainMenu += "[3] - Print all orders\n";
        mainMenu += "[4] - Exit program\n";
        return mainMenu;
    }

    /**
     * Asks the user about customer details and creates a new order accordingly.
     * @return Order: An order object.
     */
    public static Order createOrder()
    {
        // creates a new order from the customer details entered.
        System.out.print("Enter the customer name: ");
        String customerName = sc.next();
        System.out.print("\nEnter the customer phone number: ");
        String customerPhoneNumber = sc.next();
        System.out.print("\nEnter the customer delivery address: ");
        String customerDeliveryAddress = sc.next();

        return new Order(customerName, customerPhoneNumber, customerDeliveryAddress);

    }

    /**
     * Adds the toppings to the pizza object depending on the options chosen.
     * @param pizza: Pizza object
     * @param optionChosen: Option chosen.
     */
    public static void pizzaToppingMethod (Pizza pizza, int optionChosen)
    {
        switch (optionChosen) {
            case 1:
                pizza.addPizzaTopping(PIZZA_TOPPINGS.HAM);
                break;

            case 2:
                pizza.addPizzaTopping(PIZZA_TOPPINGS.CHEESE);
                break;

            case 3:
                pizza.addPizzaTopping(PIZZA_TOPPINGS.PINEAPPLE);
                break;

            case 4:
                pizza.addPizzaTopping(PIZZA_TOPPINGS.MUSHROOMS);
                break;

            case 5:
                pizza.addPizzaTopping(PIZZA_TOPPINGS.TOMATO);
                break;

            case 6:
                pizza.addPizzaTopping(PIZZA_TOPPINGS.SEAFOOD);
                break;
        }
    }

    /**
     * Adds the pasta topping to the pasta depending on the option chosen.
     * @param pasta: Pasta object
     * @param optionChosen: Option chosen
     */
    public static void pastaToppingMethod (Pasta pasta, int optionChosen)
    {
        switch(optionChosen){
            case 1:
                pasta.addPastaTopping(PASTA_TOPPINGS.BOLOGNESE);
                break;

            case 2:
                pasta.addPastaTopping(PASTA_TOPPINGS.MARINARA);
                break;

            case 3:
                pasta.addPastaTopping(PASTA_TOPPINGS.PRIMAVERA);
                break;

            case 4:
                pasta.addPastaTopping(PASTA_TOPPINGS.TOMATO);
                break;
        }
    }

}

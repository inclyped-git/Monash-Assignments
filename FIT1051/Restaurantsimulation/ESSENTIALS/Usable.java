/**
 * Usable interface contains all the constants that is required to be used by the
 * classes.
 * @author Sharvan Saikumar
 * @version 21.0.1
 */

public interface Usable {

    // base price of pasta and pizza.
    double basePrice = 11.50;

    // pasta toppings
    enum PASTA_TOPPINGS { BOLOGNESE, MARINARA, PRIMAVERA, TOMATO }

    // pizza toppings
    enum PIZZA_TOPPINGS { HAM, CHEESE, PINEAPPLE, MUSHROOMS, TOMATO, SEAFOOD }

    // meal types
    enum MEAL_TYPE { MEAT, VEGETARIAN, VEGAN }

}


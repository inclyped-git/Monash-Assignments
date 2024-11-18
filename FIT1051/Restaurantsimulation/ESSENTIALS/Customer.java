/**
 * Customer class contains the attributes and behaviours that represent
 * a Customer in the Restaurant Simulation.
 * @author inclyped
 * @version 21.0.1
 */
public class Customer {

    // non-static fields.
    private String customerName;
    private String customerContactNumber;
    private String customerDeliveryAddress;

    // Default constructor for the Customer class.
    public Customer()
    {
        this.customerName = "";
        this.customerContactNumber = "";
        this.customerDeliveryAddress = "";
    }

    // Non-default Customer class constructor.
    public Customer(String name, String number, String address)
    {
        this.customerName = name;
        this.customerContactNumber = number;
        this.customerDeliveryAddress = address;
    }

    // Customer class mutators.
    public void setName(String name)
    {
        this.customerName = name;
    }

    public void setContactNumber(String number)
    {
        this.customerContactNumber = number;
    }

    public void setDeliveryAddress(String address)
    {
        this.customerDeliveryAddress = address;
    }


    // Customer class accessors.
    public String getName()
    {
        return this.customerName;
    }

    public String getContactNumber()
    {
        return this.customerContactNumber;
    }

    public String getDeliveryAddress()
    {
        return this.customerDeliveryAddress;
    }

    // Customer class toString() method.
    @Override
    public String toString()
    {
        return String.format("Customer name: %s%nContact no: %s%nDelivery address: %s%n", this.customerName, this.customerContactNumber, this.customerDeliveryAddress);
    }

}

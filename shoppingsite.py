"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken.
"""


from flask import Flask, render_template, redirect, flash, session, request, g
import jinja2
import customers
import melons


app = Flask(__name__)

# Need to use Flask sessioning features

app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html", melon_list=melon_list)


@app.route("/melon/<int:melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)

    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def shopping_cart():
    """Display content of shopping cart."""

    # TODO: Display the contents of the shopping cart.

    # The logic here will be something like:
    #
    # - get the list-of-ids-of-melons from the session cart
    # - loop over this list:
    #   - keep track of information about melon types in the cart
    #   - keep track of the total amt ordered for a melon-type
    #   - keep track of the total amt of the entire order
    # - hand to the template the total order cost and the list of melon types
    
   
    # TODO: turn the session to have a key of cart, value is a dictionary
    # session = cart{
    #                {id {quantity: 1}}
                    # {id {quantity: 1}}
        
    # print "session[cart] is", session["cart"]
    # sum = 0
    if 'cart' not in session:
        session["cart"] = {} 

    total_cart =0 

    for id in session["cart"]:
        # import pdb; pdb.set_trace()
        common_name = melons.get_by_id(int(id)).common_name
        price_int = melons.get_by_id(int(id)).price
        price = "${:.2f}".format(melons.get_by_id(int(id)).price)
        quantity = session["cart"][str(id)]["quantity"]
        total = "${:.2f}".format(price_int * quantity)
        session["cart"][str(id)] = {"common_name": common_name, "price": price, "quantity": quantity, "total": total}
    
        total_cart += price_int * quantity       
    
    return render_template("cart.html", total_cart=total_cart)
    # return redirect("/")


@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Successfully added to cart'.
    """
    ######### TOASK: WHY DO WE HAVE TO CONVERT TO INTS?

    # TODO: turn the session to have a key of cart, value is a dictionary
    # session = cart{
    #                {id {quantity: 1}}
                    # {id {quantity: 1}}
    #                       }
    
    if 'cart' not in session:
        session["cart"] = {} 
   
    if str(id) not in session["cart"]:
        session["cart"][str(id)] = {"quantity": 1}
    else:
        session["cart"][str(id)]["quantity"] += 1
        print "current quantity: ", session["cart"][str(id)]

    flash("Successfully added to cart")

    # import pdb; pdb.set_trace()

    print "CART", session["cart"]
    
    return redirect("/cart")

    # TODO: Finish shopping cart functionality

    # The logic here should be something like:
    #
    # - add the id of the melon they bought to the cart in the session


@app.route("/logout")
def logout():
    """Logout and clear sessions."""

    session.clear()


    return redirect("/")


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/new_account")
def create_account():
    """Create new account."""

    return render_template("new_account.html")


@app.route("/success", methods=["POST", "GET"])
def successful():
    """flashes successful account."""

    flash("Account successfully created")
    g.new_customer_dictionary = {}
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    email = request.form["email"]
    password = request.form["password"]
    
    with open("customers.txt", "a") as myfile:
        myfile.write("\n{}|{}|{}|{}".format(first_name, last_name, email, password))
        # myfile.close()

    return redirect("/login")

    
@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """
    email = request.form["email"]
    password = request.form["password"]
    customer_dictionary = customers.get_all_customers()

    # checks to see if the email mataches the password stored for our three customers
    if email in customer_dictionary and password == customer_dictionary[email].password:
        session["login"] = email
        return redirect("/")
    # elif email in g.new_customer_dictionary:
    #     session["login"] = email
    #     return redirect("/")
    else:
        flash("You are not a valid user")
        return redirect("/login")
 

@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True)

"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken.
"""
# PROBLEMS:

# Questions!
# What's the best way to make global variables?  Need first name for nav bar, never render_template("base.html"), so need it to "pass through" without ever being called.  Is there a better way than using @app.context_processor functions?
# What would have been a more concise way to make the pages where I change first name / last name / email / password?  Could I have pased the pages through as parameters in my @app?  like @app.route/change/<str:xyz>?

from flask import Flask, render_template, redirect, flash, session, request
import jinja2
import customers
import melons
import sys
import fileinput


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
    # # sum = 0
    if 'cart' not in session:
        session["cart"] = {} 

    shopping_cart = {}

    total_cart =0 
 
    for id in session["cart"]:
        # import pdb; pdb.set_trace()
        common_name = melons.get_by_id(int(id)).common_name
        price_int = melons.get_by_id(int(id)).price
        price = "${:.2f}".format(melons.get_by_id(int(id)).price)
        quantity = session["cart"][id]
        total = "${:.2f}".format(price_int * quantity)
        shopping_cart[id] = {"common_name": common_name, "price": price, "quantity": quantity, "total": total}

        total_cart += price_int * quantity       
    
    return render_template("cart.html", shopping_cart=shopping_cart, total_cart=total_cart)
    # return redirect("/")


@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Successfully added to cart'.
    """

    if 'cart' not in session:
        session["cart"] = {} 
    
    session["cart"][str(id)] = session["cart"].get(str(id), 0)
    session["cart"][str(id)] += 1

    flash("Successfully added to cart")

    return redirect("/cart")



@app.route("/logout")
def logout():
    """Logout and clear sessions."""

    session.clear()


    return redirect("/")



@app.route("/new_account")
def create_account():
    """Create new account."""

    return render_template("new_account.html")


@app.route("/new_account", methods=["POST"])
def successful():
    """flashes successful account and writes the new account to the txt file"""

    flash("Account successfully created")
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    email = request.form["email"]
    password = request.form["password"]
    
    with open("customers.txt", "a") as myfile:
        myfile.write("\n{}|{}|{}|{}".format(first_name, last_name, email, password))
        myfile.close()

    return redirect("/login")


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")

    
@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """
    email = request.form["email"]
    password = request.form["password"]
    customer_dictionary = customers.read_customers_from_file("customers.txt")

    # checks to see if the email mataches the password stored
    if email in customer_dictionary and password == customer_dictionary[email].password:
        session["login"] = email
        return redirect("/melons")
    
    else:
        flash("You are not a valid user")
        return redirect("/login")

@app.route("/profile") 
def profile_page():
    """Displays profile page of user.  Provides links to change fields."""


    if "login" in session:
        first_name = customers.get_by_email(session["login"]).first_name
        last_name = customers.get_by_email(session["login"]).last_name
        email = customers.get_by_email(session["login"]).email
        password = customers.get_by_email(session["login"]).password

    return render_template("profile.html", first_name=first_name, last_name=last_name, email=email, password=password)


@app.route("/change_first_name", methods=["GET"]) 
def edit_first_name_form():
    
    return render_template("change_first_name.html")


@app.route("/change_first_name", methods=["POST"]) 
def edit_first_name():

    first_name = customers.get_by_email(session["login"]).first_name
    last_name = customers.get_by_email(session["login"]).last_name
    email = customers.get_by_email(session["login"]).email
    password = customers.get_by_email(session["login"]).password

    desired_first_name = request.form.get("desired-first-name")
    submitted_password = request.form.get("password")

    if password == submitted_password:    
        for i, line in enumerate(fileinput.input('customers.txt', inplace=1)):
            sys.stdout.write(line.replace(first_name+"|"+last_name+"|"+email+"|"+password, desired_first_name+"|"+last_name+"|"+email+"|"+password))
        
        flash("Your first name has been updated")

    else:
        flash("Incorrect password")
    
    return redirect("/profile")

@app.route("/change_last_name", methods=["GET"]) 
def edit_last_name_form():
    
    return render_template("change_last_name.html")


@app.route("/change_last_name", methods=["POST"]) 
def edit_last_name():

    first_name = customers.get_by_email(session["login"]).first_name
    last_name = customers.get_by_email(session["login"]).last_name
    email = customers.get_by_email(session["login"]).email
    password = customers.get_by_email(session["login"]).password

    desired_last_name = request.form.get("desired-last-name")
    submitted_password = request.form.get("password")

    if password == submitted_password:    
        for i, line in enumerate(fileinput.input('customers.txt', inplace=1)):
            sys.stdout.write(line.replace(first_name+"|"+last_name+"|"+email+"|"+password, first_name+"|"+desired_last_name+"|"+email+"|"+password))
        
        flash("Your last name has been updated")

    else:
        flash("Incorrect password")
    
    return redirect("/profile")


@app.route("/change_password", methods=["GET"]) 
def edit_password_form():
    
    return render_template("change_password.html")


@app.route("/change_password", methods=["POST"]) 
def edit_password_name():

    first_name = customers.get_by_email(session["login"]).first_name
    last_name = customers.get_by_email(session["login"]).last_name
    email = customers.get_by_email(session["login"]).email
    password = customers.get_by_email(session["login"]).password

    confirm_password = request.form.get("confirm-password")
    desired_password = request.form.get("desired-password")
    
    if password == confirm_password:
        for i, line in enumerate(fileinput.input('customers.txt', inplace=1)):
            sys.stdout.write(line.replace(first_name+"|"+last_name+"|"+email+"|"+password, first_name+"|"+last_name+"|"+email+"|"+desired_password))
        
        flash("Your password has been updated")

    else:
        flash("Incorrect password")
    
    return redirect("/profile")


@app.context_processor
def first_name_creation():
    if "login" in session:
        first_name = customers.get_by_email(session["login"]).first_name
        return dict(first_name=first_name)
    else:
        return dict(first="hello")


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True)

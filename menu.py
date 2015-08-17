from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)


from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# create Session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Displays all the restaurants in a list. Home page of the application.
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)


# Form for creating a new restaurant.
@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name = request.form['name'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')


# Form for editing a restaurant already in the list.
@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    editedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
        session.add(editedRestaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html', restaurant=editedRestaurant)


# Page to confirm deleting selected restaurant.
@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    deleteRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        session.delete(deleteRestaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant=deleteRestaurant)


# Displays all menu items for selected restaurant in a list.
@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)


# form for creating new menu item for selected restaurant.
@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], description=request.form['description'], price=request.form['price'], course=request.form['course'], restaurant_id =
            restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id =
            restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant =
            restaurant)

# form for editing menu item for selected restaurant.
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/',
 methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    editItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return render_template('editMenuItem.html', restaurant=restaurant,
     editItem=editItem)

# form for deleting menu item from selected restaurant.
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/',
 methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    deleteItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return render_template('deleteMenuItem.html', restaurant=restaurant,
     deleteItem=deleteItem)


if __name__ == '__main__':
    app.debug = True
    app.run()
    #if vagrant use: app.run(host = '0.0.0.0', port = 5000)
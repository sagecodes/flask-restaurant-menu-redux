from flask import Flask, render_template

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
@app.route('/restaurant/new/')
def newRestaurant():
    return render_template('newRestaurant.html')


# Form for editing a restaurant already in the list.
@app.route('/restaurant/<int:restaurant_id>/edit/')
def editRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    return render_template('editRestaurant.html', restaurant=restaurant)


# Page to confirm deleting selected restaurant.
@app.route('/restaurant/<int:restaurant_id>/delete/')
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    return render_template('deleteRestaurant.html', restaurant=restaurant)


# Displays all menu items for selected restaurant in a list.
@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)


# form for creating new menu item for selected restaurant.
@app.route('/restaurant/<int:restaurant_id>/menu/new/')
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    return render_template('newMenuItem.html', restaurant=restaurant)

# form for editing menu item for selected restaurant.
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    editItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return render_template('editMenuItem.html', restaurant=restaurant, editItem=editItem)

# form for deleting menu item from selected restaurant.
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    deleteItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return render_template('deleteMenuItem.html', restaurant=restaurant, deleteItem=deleteItem)


if __name__ == '__main__':
    app.debug = True
    app.run()
    #if vagrant use: app.run(host = '0.0.0.0', port = 5000)
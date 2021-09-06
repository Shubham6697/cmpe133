## HTML file

    ecommerce/templates/html

## CSS file + picture + File html

    static/assests : css
        1. For navigation bar - other files inherit from this file: nav.html - nav.css
        2. For display the product and home page =>  homeMain.html - no css yet
        3. For information company: about.html - No file css yet. 
        4. register and signin: 
                + register.html - register.css
                + signin.html - signin.css
        6. To display a unique product. => product.html - no css yet
        7. To result of searching items. => search.html - no css yet
> You should change to a folder of carts if looking for functions. HTML file is still in the same place in the template folder in "cart". 
        8. A cart => cart.html - no css yet
    static/images : picture
    media: for the picture of products
        9. To checkout product => checkout.html in "checkout" folder - no css yet
        10. To contact => newaddress.html in accounts folder and views.py in ecommerce folder
## back-end

    models.py : database elements
    urls.py: path/ link
    views : connect to html, functions
    forms : form input

## To run server
    1. Open terminal 
    2. Go to the directory of Grocery_store
    3. python manage.py runserver or python3 manage.py
> ``` Note: ``` 
        > If you can't run:  you should activate "venv" unless try to download all the libraries it required on terminal. 
            

## To manage database

   The link of database: [Press here !](http://127.0.0.1:8000/admin/)

- Account: admin11
- password: @team0011
## If the database has a bug. Reset migration
- python3 manage.py makemigrations <app_name> --empty
- python3 manage.py migrate

## To add admin account

    Way 1: terminal => python3 manage.py createsuperuser or python manage.py createsuperuser
    Way 2: access to account above => users => add => create your own account with checkingall choices to become superuser.

## Update database

    python3 manage.py makemigrations
    python3 manage.py migrate

## Check the sqlite3

    python3 manage.py shell
```Recommendation: Please note here about your code's knowledge or  at least comment on what your functions represent. That will help teammates to understand better and catchup easily.```

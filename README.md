# CS50x-commerce
CS50x Web Programming - Project 2 - Commerce

Design an eBay-like e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”

[Specifications](https://cs50.harvard.edu/web/2020/projects/2/commerce/)

[Specifications Screencast](https://www.youtube.com/watch?v=tjUzX2EC7hQ)

## Live Demo

[Live Demo](https://acampos-cs50x-commerce.herokuapp.com/)


## Installation

1. Clone the project

2. Install all necessary dependencies
    ```python
        pip3 install -r requirements.txt
    ```

3. Migrate database
    ```python
        python3 manage.py migrate
    ```

4. Run Django server
    ```python
        python3 manage.py runserver
    ```
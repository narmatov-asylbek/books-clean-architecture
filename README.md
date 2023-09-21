# Used technologies
- Python 3.10
- Django 4.2
- Django REST Framework 3.14
- drf-yasg


# Installation steps
1. Clone the repo
2. Create and activate virtual environment

``` shell
virtualenv -p python3.10 .venv
source .venv/bin/activate
```
3. Install requirements

``` shell
pip install -r requirements.txt
```
4. Export Environment variables

``` shell
export SECRET_KEY=your-super-mega-secret-key
```
5. Migrate

``` shell
python manage.py migrate
```
6. Go to the documentation in `localhost:8000/swagger/`

# Usage

## Authorization and authentication
`/api/v1/login` Takes an email and password and returns token. Token should be in headers for requests. Example: `Authorization: Token some-token`.

## Endpoints

`/api/v1/books` gets the list of the books.

Query parameters:
- created_before. Example: `2023-09-22`
- created_after. Example: `2023-09-15`
- categories. Example: `classics, romance`
- authors. Example: `1,2,3,4`

`/api/v1/books/{book_id}` Get the detail of the book

`/api/v1/books/favourites` Add book to the favourites

`/api/v1/books/reviews` Create a review for a book.


# Architecture
- Repositories. Interface over data storage. The only way to access the database.
- Use cases. Contains the main logic of the application
- dtos. Data Transfer objects. Used to pass data from one layer to another.

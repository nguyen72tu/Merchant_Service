
# Merchant_Service

This is test project build by Django-REST that about Merchant that manage Service, Product and has the information involve like Category, Hashtag, Keyword


## Requirement system key

#### Python 3.8
#### Django==4.2.7
#### djangorestframework==3.14.0
#### Mysql 8.0

## Acknowledgements

 - [Django REST](https://www.django-rest-framework.org/)


## Features

- User
- Merchant
- Service & Product
- Taxonomy (Category, Hashtag, Keyword)


## Optimizations

Some feature not fully completed but the structure of project is accomplished

## Features status

| Feature             | Status of CRUD                                                                |
| ----------------- | ------------------------------------------------------------------ |
| User | ![#008000](https://via.placeholder.com/10/008000?text=+) Create, Retrieve, Delete |
| Merchant | ![#ffa500](https://via.placeholder.com/10/ffa500?text=+) Create, Retrieve |
| Service & Product | ![#ff0000](https://via.placeholder.com/10/FF0000?text=+)  |
| Taxonomy | ![#008000](https://via.placeholder.com/10/008000?text=+) Create, Retrieve, Update, Delete |


## Run Locally

Clone the project

```bash
  git clone https://link-to-project
```

Go to the project directory

```bash
  cd MerchantServices
```


```bash
Install dependencies

```bash
  source venv/bin/activate (Ubuntu)
  pip install -r requirements.txt
```

Start the server

```bash
  python3 manage.py runserver 8000
```


## Usage

```
Access to swagger of project
http://localhost:8000/swagger/

Find API sign/up and regester account
Then sign/in to get {access} token
Authorize with Value: Bearer {access}
OKE, let visit another APIs

```


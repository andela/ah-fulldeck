[![Build Status](https://travis-ci.org/andela/ah-fulldeck.svg?branch=ch-travisCI-integration-162948983)](https://travis-ci.org/andela/ah-fulldeck) 
[![Coverage Status](https://coveralls.io/repos/github/andela/ah-fulldeck/badge.svg?branch=develop)](https://coveralls.io/github/andela/ah-fulldeck?branch=develop)



Authors Haven - A Social platform for the creative at heart.
=======

## Vision
Create a community of like minded authors to foster inspiration and innovation
by leveraging the modern web.

---

## API Spec
The preferred JSON object to be returned by the API should be structured as follows:

## Links to the Mockup Designs
1. [Sign Up, Log In and Create Article](https://wireframepro.mockflow.com/view/M15c07edf891b45f0dfaa1f5cc85c68c61547577768098#/page/D31452032c99b79d208bf34f194933048)
    
2. [Homepage, Landing page and Profile](https://wireframepro.mockflow.com/view/M724c1af1281229c8914e2f1e3b9e2a201547621799851)
   

## Hosting
Staging - https://ah-fulldeck-staging.herokuapp.com/

## API Documentation
https://ah-fulldeck-staging.herokuapp.com/api/v1/docs

## How to setup and test the application
1. Install pip first using this command 

    `sudo apt-get install python3-pip`

1. Install virtualenv using pip3 `sudo pip3 install virtualenv `

1. Create a virtual environment `virtualenv venv `

1. Activate your virtual environment: `source venv/bin/activate`

1. Clone this repo with the following command:

    `git clone https://github.com/andela/ah-fulldeck.git`

1. Cd into the ah-fulldeck directory:
`cd ah-fulldeck`

1. Install the requirements by running the command:

      `pip install -r requirements.txt`

1. Create a database:
  In the terminal run the following after installing postgres and setting up:  
  
    `psql`
  `create DATABASE <name_of_your_database>`
1. Create a .env file in the project folder and and the following exports:  
   
   `export DATABASE="<name of your database>"`  
   
   `export USER="<your postgres username>"`  
   
   `export HOST="<localhost>"`
   
   `export PASSWORD="<your postgres password>"`
   
   `export EMAIL_SENDER="ahfulldeck@gmail.com"`

   `export EMAIL_HOST="smtp.gmail.com"`

   `export EMAIL_HOST_USER="ahfulldeck"`

   `export EMAIL_HOST_PASSWORD="Ful!deck1234"`

   `export EMAIL_PORT=587`

   `export GOOGLE_OAUTH2_KEY='473249897631-qg1s7bbg9a2gflq7omjk3r7qhnqmmamh.apps.googleusercontent.com'`
    
   `export GOOGLE_OAUTH2_SECRET='Z_3MSVULXNPSkwUPRv-dYQ53'`

   `export FACEBOOK_KEY='336617310278979'`

   `export FACEBOOK_SECRET='342f823250b66a873a9a795c90c215b5'`

   `export TWITTER_KEY='YawQxOxPWFGYTeASKViC9FtGi'`

   `export TWITTER_SECRET='LiZZrg8X5mEK4Pc0iDFcSBzilEnoJ7AhCtMNQ4fTKZWf9BhVbh'`

   `export FACEBOOK_TOKEN='EAAEyJtM0VUMBAH3GbEZA3wZBuboZApAKrHVPXX7Fwi3F50tj9c6GGgNyU8EeYPq8hrZC1zTpqG9KcypSl8VYHyZCcwZCmeALqf1rcBjHdJ0kyMlVJNLZBTbvV1UvseknVYrWaXqZAfGInAZCtWOePvfhwp81ymGvqdLkNS38OaQDkXsUm8JhZBPFYPeFkIL0BCfZANdDrd9woc1fo3TeDSJU2NBccjmyBNCvSEZD'`

   `export TWITTER_TOKEN='1087685693659332609-9ZPBbVerMEDUrcIKHGhyC8fzv1bpeh'`

   `export TWITTER_TOKEN_SECRET='3hUSleVtoFTZzfxVSsUTZTQgCxtM7IZWQM0ExJh4PJj2n'`

1. Export the settings by running the command: `source .env`

1. Migrate the database:
 
    `python manage.py migrate`
1. Run the server:
    
    `python manage.py runserver`

### Users (for authentication)
```source-json
{
  "user": {
    "email": "jake@jake.jake",
    "token": "jwt.token.here",
    "username": "jake",
    "bio": "I work at statefarm",
    "image": null
  }
}
```
### Profile
```source-json
{
  "profile": {
    "username": "jake",
    "bio": "I work at statefarm",
    "image": "image-link",
    "following": false
  }
}
```
### Single Article
```source-json
{
  "article": {
    "slug": "how-to-train-your-dragon",
    "title": "How to train your dragon",
    "description": "Ever wonder how?",
    "body": "It takes a Jacobian",
    "tagList": ["dragons", "training"],
    "createdAt": "2016-02-18T03:22:56.637Z",
    "updatedAt": "2016-02-18T03:48:35.824Z",
    "favorited": false,
    "favoritesCount": 0,
    "author": {
      "username": "jake",
      "bio": "I work at statefarm",
      "image": "https://i.stack.imgur.com/xHWG8.jpg",
      "following": false
    }
  }
}
```
### Multiple Articles
```source-json
{
  "articles":[{
    "slug": "how-to-train-your-dragon",
    "title": "How to train your dragon",
    "description": "Ever wonder how?",
    "body": "It takes a Jacobian",
    "tagList": ["dragons", "training"],
    "createdAt": "2016-02-18T03:22:56.637Z",
    "updatedAt": "2016-02-18T03:48:35.824Z",
    "favorited": false,
    "favoritesCount": 0,
    "author": {
      "username": "jake",
      "bio": "I work at statefarm",
      "image": "https://i.stack.imgur.com/xHWG8.jpg",
      "following": false
    }
  }, {

    "slug": "how-to-train-your-dragon-2",
    "title": "How to train your dragon 2",
    "description": "So toothless",
    "body": "It a dragon",
    "tagList": ["dragons", "training"],
    "createdAt": "2016-02-18T03:22:56.637Z",
    "updatedAt": "2016-02-18T03:48:35.824Z",
    "favorited": false,
    "favoritesCount": 0,
    "author": {
      "username": "jake",
      "bio": "I work at statefarm",
      "image": "https://i.stack.imgur.com/xHWG8.jpg",
      "following": false
    }
  }],
  "articlesCount": 2
}
```
### Single Comment
```source-json
{
  "comment": {
    "id": 1,
    "createdAt": "2016-02-18T03:22:56.637Z",
    "updatedAt": "2016-02-18T03:22:56.637Z",
    "body": "It takes a Jacobian",
    "author": {
      "username": "jake",
      "bio": "I work at statefarm",
      "image": "https://i.stack.imgur.com/xHWG8.jpg",
      "following": false
    }
  }
}
```
### Multiple Comments
```source-json
{
  "comments": [{
    "id": 1,
    "createdAt": "2016-02-18T03:22:56.637Z",
    "updatedAt": "2016-02-18T03:22:56.637Z",
    "body": "It takes a Jacobian",
    "author": {
      "username": "jake",
      "bio": "I work at statefarm",
      "image": "https://i.stack.imgur.com/xHWG8.jpg",
      "following": false
    }
  }],
  "commentsCount": 1
}
```
### List of Tags
```source-json
{
  "tags": [
    "reactjs",
    "angularjs"
  ]
}
```
### Errors and Status Codes
If a request fails any validations, expect errors in the following format:

```source-json
{
  "errors":{
    "body": [
      "can't be empty"
    ]
  }
}
```
### Other status codes:
401 for Unauthorized requests, when a request requires authentication but it isn't provided

403 for Forbidden requests, when a request may be valid but the user doesn't have permissions to perform the action

404 for Not found requests, when a resource can't be found to fulfill the request


Endpoints:
----------

### Authentication:

`POST /api/users/login`

Example request body:

```source-json
{
  "user":{
    "email": "jake@jake.jake",
    "password": "jakejake"
  }
}
```

No authentication required, returns a User

Required fields: `email`, `password`

### Registration:

`POST /api/users`

Example request body:

```source-json
{
  "user":{
    "username": "Jacob",
    "email": "jake@jake.jake",
    "password": "jakejake"
  }
}
```

No authentication required, returns a User

Required fields: `email`, `username`, `password`

### Get Current User

`GET /api/user`

Authentication required, returns a User that's the current user

### Update User

`PUT /api/user`

Example request body:

```source-json
{
  "user":{
    "email": "jake@jake.jake",
    "bio": "I like to skateboard",
    "image": "https://i.stack.imgur.com/xHWG8.jpg"
  }
}
```

Authentication required, returns the User

Accepted fields: `email`, `username`, `password`, `image`, `bio`

### Get Profile

`GET /api/profiles/:username`

Authentication optional, returns a Profile

### Follow user

`POST /api/profiles/:username/follow`

Authentication required, returns a Profile

No additional parameters required

### Unfollow user

`DELETE /api/profiles/:username/follow`

Authentication required, returns a Profile

No additional parameters required

### List Articles

`GET /api/articles`

Returns most recent articles globally by default, provide `tag`, `author` or `favorited` query parameter to filter results

Query Parameters:

Filter by tag:

`?tag=AngularJS`

Filter by author:

`?author=jake`

Favorited by user:

`?favorited=jake`

Limit number of articles (default is 20):

`?limit=20`

Offset/skip number of articles (default is 0):

`?offset=0`

Authentication optional, will return multiple articles, ordered by most recent first

### Feed Articles

`GET /api/articles/feed`

Can also take `limit` and `offset` query parameters like List Articles

Authentication required, will return multiple articles created by followed users, ordered by most recent first.

### Get Article

`GET /api/articles/:slug`

No authentication required, will return single article

### Create Article

`POST /api/articles`

Example request body:

```source-json
{
  "article": {
    "title": "How to train your dragon",
    "description": "Ever wonder how?",
    "body": "You have to believe",
    "tagList": ["reactjs", "angularjs", "dragons"]
  }
}
```

Authentication required, will return an Article

Required fields: `title`, `description`, `body`

Optional fields: `tagList` as an array of Strings

### Update Article

`PUT /api/articles/:slug`

Example request body:

```source-json
{
  "article": {
    "title": "Did you train your dragon?"
  }
}
```

Authentication required, returns the updated Article

Optional fields: `title`, `description`, `body`

The `slug` also gets updated when the `title` is changed

### Delete Article

`DELETE /api/articles/:slug`

Authentication required

### Add Comments to an Article

`POST /api/articles/:slug/comments`

Example request body:

```source-json
{
  "comment": {
    "body": "His name was my name too."
  }
}
```

Authentication required, returns the created Comment
Required field: `body`

### Get Comments from an Article

`GET /api/articles/:slug/comments`

Authentication optional, returns multiple comments

### Delete Comment

`DELETE /api/articles/:slug/comments/:id`

Authentication required

### Favorite Article

`POST /api/articles/:slug/favorite`

Authentication required, returns the Article
No additional parameters required

### Unfavorite Article

`DELETE /api/articles/:slug/favorite`

Authentication required, returns the Article

No additional parameters required

### Get Tags

`GET /api/tags`





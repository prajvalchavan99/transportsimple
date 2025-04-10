# TransportSimple Q&A Forum

## Steps to Run the Project

1. Unzip or clone the repository  
2. Navigate to the project directory:
   ```bash
   cd transportsimple
   ```
3. ```bash
   virtualenv env
   ```
4. ```bash
   env\Scripts\activate
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```

Note: The project includes a preloaded database with questions and answers, so migrations are not required.

## Project Description

A simple Quora-inspired Q&A forum built with Django.

## Features

1. User Registration and Login  
2. Post a Question  
3. View All Questions  
4. Answer a Question  
5. Like an Answer  
6. Logged-in user dashboard  
7. Search functionality  
8. Smart login redirection using `next` parameter

## Additional Features

1. SEO-friendly URLs for questions (e.g., /questions/5/how-to-learn-django)  
2. "Liked by Author" badge for answers liked by the original question author

## Known Limitation

- Page reload on like action  
  - Currently, liking an answer causes a page reload. This can be optimized using AJAX with an API endpoint for smoother user experience.

## Existing Users

You can log in with the following usernames. All users share the same password:

Password: password123

- transportsimple  
- alice  
- bob  
- carol  
- dave  

You can also register new users via the app.

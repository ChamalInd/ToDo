# ToDo

### Project Overview
This is a simple ToDo application to help user manage their tasks efficiently. This allows user to create, and maintain thier tasks in a clear and structred way. This app gurentees security and privacy of personal data by using user authentication and data encryptions.

### Features
- Enables managing tasks efficiently
- Clean UI
- User authentications and encryptions

### Tech Stack
- Front End: HTML, CSS, JavaScript, Bootstrap5
- Back End: Flask, Python
- DataBase: SQLite3

### Project Structure
- `app.py`: Holds the functions for the routes and backend logic for Flask
- `helper.py`: Contains the utility functions to help the main `app.py` program
- `/static`:
    - `style.css`: Contains the stylings for the HTML elements
    - `script.js`: Contains the JS functions to help with front end operations
    - `todo.png`: Website Logo
- `/templates`:
    - `layout.html`: Boiler plate HTML file for the whole project
    - `index.html`: Contains the HTML elements of the home page
    - `login.html`: Contains the HTML elements of the login page
    - `register.html`: Contains the HTML elements of the signin page
    - `profile.html`: Contains the HTML elemts of the user's profile page
- `requirements.txt`: Contains the external python libreries required
- `todo.db`: Database that holds all the data of the application
- `README.md`: Markdown file for project explanation

### Getting Started
#### Prerequisites
- Make sure you have python installed. you can check by running, 
```
python --version
```

#### Installing
- Clone the repository into your local machine by running,
```
git clone https://github.com/ChamalInd/ToDo.git
```
- Move into the project folder
```
cd ToDo
```
- (optional) Create a virtual environment
```
python -m venv venv
source venv/bin/activate
```
- Install requirements
```
pip install -r requirements.txt
```

### Running The Application
Run `flask run` on your terminal and click on the link provided.

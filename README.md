# Full-Time

Full-Time is a football match score prediction application written in Python (BE) and Flutter (FE) for mobile devices.

## Installation

1. Create a python virtual environment `python -m venv venv`
2. Activate the virtual environment
   - Windows: `venv\Scripts\activate`
   - Linux: `source venv\Scripts\activate`
3. Install required packages / modules `pip install -r requirements.txt`
4. Add a `.env` file
   1. This file should have the below (check `src.config.config`) for the full list in case I forgot to update the README
   2. Remember to remove any `#` comments

```
FLASK_ENV = Local | Development | Production
FLASK_DEBUG = True | False
FLASK_TESTING = True | False
FLASK_SECRET_KEY = # A really long hard-to-guess text

# Mongo DB URL / URI
MONGO_URI = mongodb+srv://{user_name}:{password}@main.tydga.mongodb.net/{database}?retryWrites=true&w=majority

# 0=All, 10=Debug+, 20=Info+, 30=Warning+, 40=Error+, 50=Critical
LOGGING_LEVEL = 0 | 10 | 20 | 30 | 40 | 50

FOOTBALL_DATA_KEY = # Your football-data.org API key

FIREBASE_JSON = # The path to your firebase service account json
```

## Running the application

1. Open a new terminal / cmd window (in root folder of this project)
2. Type in `python app.py`

### Running / Debugging in VS-Code

Use this as your `launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Flask",
      "type": "python",
      "request": "launch",
      "module": "flask",
      "env": {
        "FLASK_APP": "app.py"
      },
      "args": ["run"],
      "jinja": true
    }
  ]
}
```

## License

Copyright &copy; Jakub Zurakowski 2020 - Please see License.md

from dashboard import app
from dashboard.config import config

if __name__ == "__main__":
    app.run(debug=config["flask_debug"])

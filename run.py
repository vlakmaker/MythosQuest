# run.py

from app import create_app
# *** Import the init_db function ***
from app.models import init_db
from dotenv import load_dotenv

load_dotenv()

print("Creating Flask app instance...")
app = create_app()
print("Flask app instance created.")

# *** Add this block to initialize DB ***
with app.app_context():
    print("Entering app context to initialize database...")
    init_db()
    print("Database initialization attempted.")
# *** End DB initialization block ***

if __name__ == "__main__":
    print("Starting Flask development server...")
    # Note: host="0.0.0.0" makes it accessible on your network
    # Use host="127.0.0.1" for local access only
    app.run(host="0.0.0.0", port=5000, debug=True)
import sys
import os

# Ensure the directory containing the 'database' package is in the system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import initialize_database, seed_database  # Adjusted import

if __name__ == "__main__":
    initialize_database()
    seed_database()
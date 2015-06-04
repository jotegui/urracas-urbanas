import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

from urracas import app

if __name__ == "__main__":
    app.run(debug=True)

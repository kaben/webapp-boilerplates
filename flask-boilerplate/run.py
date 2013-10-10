#!/usr/bin/env python
from webapp import app

# If this script is being executed instead of imported, run the webapp.
if __name__ == "__main__": app.run(debug=True)


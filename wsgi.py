import os
from index import app


if __name__ == "__main__":
    port_number = os.getenv("PORT", 5000)
    app.run(host='0.0.0.0', port=port_number, debug=False)
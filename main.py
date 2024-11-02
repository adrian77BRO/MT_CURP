from flask import Flask
from flask_cors import CORS
from controllers.validate_curp import validate_curp_bp
from controllers.generate_curp import generate_curp_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(validate_curp_bp)
app.register_blueprint(generate_curp_bp)

if __name__ == '__main__':
    app.run(debug=True)
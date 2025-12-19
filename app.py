from flask import Flask, redirect, url_for, render_template
from controllers.parents_controller import parents_bp
from controllers.enfants_controller import enfants_bp
from controllers.educateurs_controller import educateurs_bp
from controllers.activites_controller import activites_bp
from controllers.presence_controller import presence_bp
from controllers.paiements_controller import paiements_bp

app = Flask(__name__)
app.secret_key = "change_this_secret"

# register blueprints with prefixes
app.register_blueprint(parents_bp, url_prefix="/parents")
app.register_blueprint(enfants_bp, url_prefix="/enfants")
app.register_blueprint(educateurs_bp, url_prefix="/educateurs")
app.register_blueprint(activites_bp, url_prefix="/activites")
app.register_blueprint(presence_bp, url_prefix="/presences")
app.register_blueprint(paiements_bp, url_prefix="/paiements")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

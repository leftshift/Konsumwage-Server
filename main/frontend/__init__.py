from flask import Blueprint, render_template


frontend = Blueprint('frontend', __name__, template_folder='templates',
                     static_folder="static", static_url_path='/frontend')


@frontend.route("/")
def dashboard():
    return render_template("dashboard.html")

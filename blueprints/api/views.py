from flask import Blueprint, render_template
api = Blueprint('api', __name__, template_folder="templates")


@api.route("/")
def index():
    return render_template("api/home.html")

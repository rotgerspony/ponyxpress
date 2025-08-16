from flask import Blueprint, render_template

bp = Blueprint("simple_pages", __name__)

@bp.get("/about")
def about_page():
    return render_template("about.html")

@bp.get("/help")
def help_page():
    return render_template("help.html")

@bp.get("/docs")
def docs_page():
    return render_template("docs.html")

@bp.get("/contact")
def contact_page():
    return render_template("contact.html")

@bp.get("/privacy")
def privacy_page():
    return render_template("privacy.html")

@bp.get("/terms")
def terms_page():
    return render_template("terms.html")

@bp.get("/changelog")
def changelog_page():
    return render_template("changelog.html")

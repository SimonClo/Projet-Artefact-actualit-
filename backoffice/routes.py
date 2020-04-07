from flask import render_template, request
from app import app, db
from models import RecentArticle

@app.route("/add_article", methods=["GET", "POST"])
def add_article():
    if request.method == "POST":
        article = RecentArticle(title=request.form.get("title"), published_date=request.form.get("published_date"), 
            article_text=request.form.get("text"), newspaper=request.form.get("newspaper"), url=request.form.get("url"))
        db.session.add(article)
        db.session.commit()
        added = True
    return render_template("form.html",inserted_article=added)

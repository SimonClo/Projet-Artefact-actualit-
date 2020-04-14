from flask import render_template, request, jsonify
from app import app, db
from models import RecentArticle

@app.route("/")
def article_form():
    return render_template("form.html")

@app.route("/add_article", methods=["POST"])
def add_article():
    article = RecentArticle(title=request.form.get("title"), published_date=request.form.get("published_date"), 
        article_text=request.form.get("text"), newspaper=request.form.get("newspaper"), url=request.form.get("url"))
    db.session.add(article)
    db.session.commit()
    data = {"msg": "henlo"}
    return jsonify(data), 200
    

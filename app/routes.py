from flask import request, render_template, redirect, url_for
from app import app, db
from app.forms import ItemForm, AuthorForm
from app.models import items, Author




@app.route("/", methods=["GET", "POST"])
def index():
    return redirect(url_for("items_list"))


@app.route("/items/", methods=["GET", "POST"])
def items_list():
    form = ItemForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            items.create(form.data)
        return redirect(url_for("items_list"))

    return render_template("items.html", form=form,
                           items=items.all(), error=error)


@app.route("/items/<int:item_id>/", methods=["GET", "POST"])
def item_details(item_id):
    def __init__():
        pass

    item = items.get(item_id - 1)
    form = ItemForm(data=item)

    if request.method == "POST":
        if request.form.get('delete'):
            items.delete(item_id - 1)
        elif form.validate_on_submit():
            if item_id > 0:
                items.update(item_id - 1, form.data)
            else:
                pass
        return redirect(url_for("items_list"))
    return render_template("item.html", form=form, item_id=item_id)


@app.route("/author/<string:author_id>/", methods=["GET", "POST"])
def author_details(author_id):
    a = Author.query.filter_by(name=author_id).first()
    if a is None:
        return "Author unknown!"

    author_dict = {
        'name': a.name,
        'desc': a.desc
    }

    form = AuthorForm(data=author_dict)

    if request.method == "POST":
        if form.validate_on_submit():
            a.name, a.desc = tuple(form.data.values())[:2]
            db.session.add(a)
            db.session.commit()

        return redirect(url_for("items_list"))
    return render_template("author.html", form=form, author_name=author_id)


if __name__ == "__main__":
    app.run(debug=True)

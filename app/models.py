from app import db
from sqlalchemy import create_engine


class Rented(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rented_status = db.Column(db.Integer, nullable=False)
    items = db.relationship("Item", backref="rented", lazy="dynamic")

    def __str__(self):
        return f"<Rent status is {self.rented_status}"


authors = db.Table('authors',
                   db.Column('author_id', db.Integer,
                             db.ForeignKey('author.id'), primary_key=True),
                   db.Column('item_id', db.Integer,
                             db.ForeignKey('item.id'), primary_key=True)
                   )


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    media = db.Column(db.Text)
    title = db.Column(db.String(100), index=True, nullable=False)
    opinion = db.Column(db.Text)
    rented_id = db.Column(db.Integer, db.ForeignKey('rented.id'))
    authors = db.relationship('Author', secondary=authors, lazy='subquery',
                              backref=db.backref('items', lazy=True))

    def __str__(self):
        return f"<Item {self.title}>"


class Author(db.Model):
    def __init__(self):
        self.author = []
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), index=True)
    desc = db.Column(db.String(1000), index=True)

    def __str__(self):
        return f"<Author {self.id} {self.name} >"


class Items:
    def __init__(self):
        self.items = []

    def all(self):
        list_elements = []
        all_items = Item.query.all()
        for item in all_items:
            list_item = {}
            list_item['id'] = item.id
            list_item['media'] = item.media
            list_item['title'] = item.title
            list_item['opinion'] = item.opinion
            for author in item.authors:
                list_item['author'] = author.name
            rented = Rented.query.get(item.rented_id).rented_status
            if rented > 0:
                list_item['rented'] = 'Hired'
            else:
                list_item['rented'] = 'Available'
            list_elements.append(list_item)
        return list_elements

    def get(self, id):
        return self.all()[id]

    def create(self, data):
        data.pop('csrf_token')
        all_items = Item.query.all()
        max_item_index = 0
        for a_item in all_items:
            max_item_index = max(max_item_index, a_item.id)
        the_item = Item()
        the_item.id = max_item_index + 1
        the_item.media = data['media']
        the_item.title = data['title']
        the_item.author = data['author']
        the_item.opinion = data['opinion']

        all_rented = Rented.query.all()
        new_rented = Rented()
        max_rented_index = 0
        for rented in all_rented:
            max_rented_index = max(max_rented_index, rented.id)
        new_rented.id = max_rented_index + 1
        new_rented.rented_status = 0 if data['rented'] is False else 1
        the_item.rented_id = new_rented.id

        all_authors = Author.query.all()
        b_author = Author()
        b_author.name = data['author']
        max_author_index = 0
        for author in all_rented:
            max_author_index = max(max_author_index, author.id)
        b_author.id = max_author_index + 1

        author_already_existed = False

        for author in all_authors:
            if b_author.name == author.name:
                author_item = authors.insert().values(author_id=author.id,
                                                      item_id=the_item.id)
                author_already_existed = True
        if author_already_existed is False:
            author_item = authors.insert().values(author_id=b_author.id,
                                                  item_id=the_item.id)
            db.session.add(b_author)

        engine = create_engine('sqlite:///library.db', echo=True)
        author_item.compile().params
        conn = engine.connect()
        conn.execute(author_item)

        db.session.add(new_rented)
        db.session.add(the_item)
        db.session.commit()

    def update(self, id, data):
        data.pop('csrf_token')
        the_item = Item.query.all()[id]
        the_item.media = data['media']
        the_item.title = data['title']
        the_item.opinion = data['opinion']

        the_author = Author.query.all()[id]
        the_author.name = data['author']

        if data['rented'] == True:
            the_item.rented.rented_status = 0
        else:
            the_item.rented.rented_status = 1
        db.session.commit()

    def delete(self, id):
        # data.pop('csrf_token')
        the_item = Item.query.all()[id]
        rented = Rented().query.get(the_item.rented_id)

        db.session.delete(rented)
        db.session.delete(the_item)
        db.session.commit()


items = Items()

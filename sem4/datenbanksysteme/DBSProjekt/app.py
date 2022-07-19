from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, desc, func, not_, or_, asc
from flask import Flask, render_template, request

from models import *

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://davyd:1234@localhost:5432/DBS_Project_Auth_Wrt"

db = SQLAlchemy(app)
db.create_all()
db.session.commit()

# queries:

###TABLES JOINED QUERY AND FILTERS###

# all tables joined


@app.route("/tables_joined/", methods=['GET', 'POST'])
def all_tables_joined():
    count = 0
    if(request.method == 'POST'):
        which_filter_asc = request.form.get("filterby asc")
        # print(which_filter_asc)
        which_filter_dsc = request.form.get("filterby dsc")
        # print(which_filter_dsc)
        what_to_filter = Article.Title  # standart aus titel

        if(which_filter_asc != None):
            order = asc
        else:
            order = desc

        if((which_filter_asc or which_filter_dsc) == "Article Title"):
            what_to_filter = Article.Title
        elif((which_filter_asc or which_filter_dsc) == "Article DOI"):
            what_to_filter = Article.DOI
        elif((which_filter_asc or which_filter_dsc) == "Article Theme"):
            what_to_filter = Article.Theme
        elif((which_filter_asc or which_filter_dsc) == "Article Year"):
            what_to_filter = Article.Year
        elif((which_filter_asc or which_filter_dsc) == "Author Names"):
            what_to_filter = Author.A_Names
        elif((which_filter_asc or which_filter_dsc) == "Journal Rank"):
            what_to_filter = Journal.Rank
        elif((which_filter_asc or which_filter_dsc) == "Journal Title"):
            what_to_filter = Journal.Title
        elif((which_filter_asc or which_filter_dsc) == "Journal ImpactFactor"):
            what_to_filter = Journal.ImpactFactor

        data = db.session.query(Article, Author, Journal)\
            .filter(Article.DOI == Write.DOI,
                    Write.A_Key == Author.A_Key,
                    Article.DOI == Publish.DOI,
                    Publish.Title == Journal.Title
                    )\
            .order_by(order(what_to_filter))\
            .all()

    data_table = []

    # print(data)
    for row in data:
        count += 1
        filter = []
        # article
        filter.append(row[0].Title)
        filter.append(row[0].DOI)
        filter.append(row[0].Theme)
        filter.append(row[0].Year)
        # author
        filter.append(row[1].A_Names)
        # journal
        filter.append(row[2].Rank)
        filter.append(row[2].Title)
        filter.append(row[2].ImpactFactor)
        # äprint(filter)
        data_table.append(filter)
    print(count)
    return render_template('index.html', data=(data_table, "Article Title", "Article DOI", "Article Theme",
                                               "Article Year", "Author Names", "Journal Rank", "Journal Title",
                                               "Journal ImpactFactor", ))

# table article


@app.route("/table_article/", methods=['GET', 'POST'])
def article_table():

    if(request.method == 'POST'):
        which_filter_asc = request.form.get("filterby asc")
        # print(which_filter_asc)
        which_filter_dsc = request.form.get("filterby dsc")
        # print(which_filter_dsc)
        what_to_filter = Article.Title  # standart aus titel

        if(which_filter_asc != None):
            order = asc
        else:
            order = desc

        if((which_filter_asc or which_filter_dsc) == "Article Title"):
            what_to_filter = Article.Title
        elif((which_filter_asc or which_filter_dsc) == "Article DOI"):
            what_to_filter = Article.DOI
        elif((which_filter_asc or which_filter_dsc) == "Article Theme"):
            what_to_filter = Article.Theme
        elif((which_filter_asc or which_filter_dsc) == "Article Year"):
            what_to_filter = Article.Year

        data = db.session.query(Article)\
            .order_by(order(what_to_filter))\
            .all()

    data_table = []

    # print(data)
    for row in data:
        filter = []
        # article
        filter.append(row.Title)
        filter.append(row.DOI)
        filter.append(row.Theme)
        filter.append(row.Year)

        data_table.append(filter)

    return render_template('index.html', data=(data_table, "Article Title", "Article DOI", "Article Theme", "Article Year"))

# table of author


@app.route("/table_author/", methods=['GET', 'POST'])
def author_table():

    if(request.method == 'POST'):
        which_filter_asc = request.form.get("filterby asc")
        # print(which_filter_asc)
        which_filter_dsc = request.form.get("filterby dsc")
        # print(which_filter_dsc)
        what_to_filter = Author.A_Names  # standart aus titel

        if(which_filter_asc != None):
            order = asc
        else:
            order = desc

        if((which_filter_asc or which_filter_dsc) == "Author Names"):
            what_to_filter = Author.A_Names
        elif((which_filter_asc or which_filter_dsc) == "Author Keys"):
            what_to_filter = Author.A_Key

        data = db.session.query(Author)\
            .order_by(order(what_to_filter))\
            .all()

    data_table = []

    # print(data)
    for row in data:
        filter = []
        # author
        filter.append(row.A_Key)
        filter.append(row.A_Names)
        # äprint(filter)
        data_table.append(filter)

    return render_template('index.html', data=(data_table, "Author Keys", "Author Names"))

# table of jounral


@app.route("/table_journal/", methods=['GET', 'POST'])
def journal_table():

    if(request.method == 'POST'):
        which_filter_asc = request.form.get("filterby asc")
        # print(which_filter_asc)
        which_filter_dsc = request.form.get("filterby dsc")
        # print(which_filter_dsc)
        what_to_filter = Journal.Rank  # standart aus titel

        if(which_filter_asc != None):
            order = asc
        else:
            order = desc

        if((which_filter_asc or which_filter_dsc) == "Journal Rank"):
            what_to_filter = Journal.Rank
        elif((which_filter_asc or which_filter_dsc) == "Journal Title"):
            what_to_filter = Journal.Title
        elif((which_filter_asc or which_filter_dsc) == "Journal ImpactFactor"):
            what_to_filter = Journal.ImpactFactor

        data = db.session.query(Journal)\
            .order_by(order(what_to_filter))\
            .all()

    data_table = []

    # print(data)
    for row in data:
        filter = []

        # journal
        filter.append(row.Rank)
        filter.append(row.Title)
        filter.append(row.ImpactFactor)
        # äprint(filter)
        data_table.append(filter)

    return render_template('index.html', data=(data_table,  "Journal Rank", "Journal Title",
                                               "Journal ImpactFactor", ))

# article, welcher rank hat das journal in dem es veröffentlicht wird


@app.route("/article_journal_rank/", methods=['GET', 'POST'])
def article_journal_rank():

    if(request.method == 'POST'):
        which_filter_asc = request.form.get("filterby asc")
        # print(which_filter_asc)
        which_filter_dsc = request.form.get("filterby dsc")
        # print(which_filter_dsc)
        what_to_filter = Journal.Rank  # standart aus titel

        if(which_filter_asc != None):
            order = asc
        else:
            order = desc

        if((which_filter_asc or which_filter_dsc) == "Article Title"):
            what_to_filter = Article.Title
        elif((which_filter_asc or which_filter_dsc) == "Journal Rank"):
            what_to_filter = Journal.Rank
        elif((which_filter_asc or which_filter_dsc) == "Journal Title"):
            what_to_filter = Journal.Title

        data = db.session.query(Article, Journal)\
            .filter(
            Article.DOI == Publish.DOI,
            Publish.Title == Journal.Title
        )\
            .order_by(order(what_to_filter))\
            .all()

    data_table = []

    # print(data)
    for row in data:
        filter = []
        # article
        filter.append(row[0].Title)
        # journal
        filter.append(row[1].Title)
        filter.append(row[1].Rank)
        # äprint(filter)
        data_table.append(filter)

    return render_template('index.html', data=(data_table, "Article Title",  "Journal Title", "Journal Rank",
                                               ))

# nur Artikel aus bestimmten jahr ausgeben lassen


@app.route("/article_year/", methods=['GET', 'POST'])
def article_year():

    if(request.method == 'POST'):
        which_filter_asc = request.form.get("filterby asc")
        # print(which_filter_asc)
        which_filter_dsc = request.form.get("filterby dsc")
        # print(which_filter_dsc)
        what_year = request.form.get("article_year")
        what_to_filter = Article.Year  # standart aus titel

        if(which_filter_asc != None):
            order = asc
        else:
            order = desc

        if((which_filter_asc or which_filter_dsc) == "Article Title"):
            what_to_filter = Article.Title
        elif((which_filter_asc or which_filter_dsc) == "Article Year"):
            what_to_filter = Article.Year

        data = db.session.query(Article)\
            .filter(
            Article.Year == what_year
        )\
            .order_by(order(what_to_filter))\
            .all()

    data_table = []

    # print(data)
    for row in data:
        filter = []
        # article
        filter.append(row.Title)
        filter.append(row.Year)
        # äprint(filter)
        data_table.append(filter)

    return render_template('index.html', data=(data_table, "Article Title",  "Article Year"
                                               ))

# nach welchem artikel wird gessucht und relationen


@app.route("/article_what/", methods=['GET', 'POST'])
def article_what():

    if(request.method == 'POST'):
        which_filter_asc = request.form.get("filterby asc")
        # print(which_filter_asc)
        which_filter_dsc = request.form.get("filterby dsc")
        # print(which_filter_dsc)
        what_article = request.form.get("article_what")
        print(what_article)
        what_to_filter = Article.Title  # standart aus titel

        if(which_filter_asc != None):
            order = asc
        else:
            order = desc

        if((which_filter_asc or which_filter_dsc) == "Article Title"):
            what_to_filter = Article.Title

        data = db.session.query(Article)\
            .filter(
            Article.Title == what_article
        )\
            .order_by(order(what_to_filter))\
            .all()

    data_table = []

    # print(data)
    for row in data:
        filter = []
        # article
        filter.append(row.Title)
        filter.append(row.DOI)
        filter.append(row.Theme)
        filter.append(row.Year)

        # äprint(filter)
        data_table.append(filter)

    return render_template('index.html', data=(data_table, "Article Title", "Article DOI", "Article Theme", "Article Year"
                                               ))


# nach welchem journal wird gessucht und relationen
@app.route("/journal_what/", methods=['GET', 'POST'])
def journal_what():

    if(request.method == 'POST'):
        which_filter_asc = request.form.get("filterby asc")
        # print(which_filter_asc)
        which_filter_dsc = request.form.get("filterby dsc")
        # print(which_filter_dsc)
        what_journal = request.form.get("journal_what")
        print(what_journal)
        what_to_filter = Journal.Title  # standart aus titel

        if(which_filter_asc != None):
            order = asc
        else:
            order = desc

        if((which_filter_asc or which_filter_dsc) == "Article Title"):
            what_to_filter = Article.Title

        data = db.session.query(Journal)\
            .filter(
            Journal.Title == what_journal
        )\
            .order_by(order(what_to_filter))\
            .all()

    data_table = []

    # print(data)
    for row in data:
        filter = []
        # article
        filter.append(row.Title)
        filter.append(row.Rank)
        filter.append(row.ImpactFactor)

        # äprint(filter
        data_table.append(filter)

    return render_template('index.html', data=(data_table, "Journal Title", "Journal Rank", "Journal ImpactFactor"
                                               ))


# nach welchem journal wird gessucht und relationen
@app.route("/journal_rank_from_then/", methods=['GET', 'POST'])
def journal_rank_from_then():

    if(request.method == 'POST'):
        which_filter_asc = request.form.get("filterby asc")
        # print(which_filter_asc)
        which_filter_dsc = request.form.get("filterby dsc")
        # print(which_filter_dsc)
        what_rank_from = request.form.get("journal_rank_from")
        what_rank_until = request.form.get("journal_rank_then")
        print(what_rank_from, what_rank_until)
        what_to_filter = Journal.Rank  # standart aus titel

        if(which_filter_asc != None):
            order = asc
        else:
            order = desc

        if((which_filter_asc or which_filter_dsc) == "Article Title"):
            what_to_filter = Article.Title
        order = asc
        data = db.session.query(Journal)\
            .filter(
            Journal.Rank >= what_rank_from,
            Journal.Rank <= what_rank_until
        )\
            .order_by(order(what_to_filter))\
            .all()

    data_table = []

    # print(data)
    for row in data:
        filter = []
        # article
        filter.append(row.Rank)
        filter.append(row.Title)
        filter.append(row.ImpactFactor)
        # äprint(filter
        data_table.append(filter)

    return render_template('index.html', data=(data_table, "Journal Rank", "Journal Title",  "Journal ImpactFactor"
                                               ))


@app.route('/', methods=['GET', 'POST'])
def index():
    data = []
    return render_template('index.html', data=data)

from treasure import app 


def create_tables():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
from app.models import db, Corpus, Text
from app import app
from pathlib import Path

corpus = {
    'c1': [
        "Test1",
        "Test2"
    ],
    'c2': [
        'Test3',
        'Test4'
    ]
}

if __name__ == '__main__':
    print("Creating mock data")
    db_dir = Path("app/db")
    if not db_dir.exists():
        print("Creating directory ./app/db")
        db_dir.mkdir()

    with app.app_context():
        db.drop_all()
        db.create_all()

        for name, texts in corpus.items():
            print(f"Creating corpus {name}")
            corpus = Corpus(name=name)
            db.session.add(corpus)
            db.session.commit()

            for t in texts:
                text = Text(text=t, corpus=corpus.id)
                db.session.add(text)
            db.session.commit()

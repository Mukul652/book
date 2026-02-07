from datetime import date
from sqlalchemy.orm import Session
from .models import Author, Book, Sale


def seed_data(db: Session):
    if db.query(Author).first():
        return

    authors = [
        Author(id=1, name="Priya Sharma", email="priya@email.com", bank_account="1234567890", ifsc="HDFC0001234"),
        Author(id=2, name="Rahul Verma", email="rahul@email.com", bank_account="0987654321", ifsc="ICIC0005678"),
        Author(id=3, name="Anita Desai", email="anita@email.com", bank_account="5678901234", ifsc="SBIN0009012"),
    ]
    db.add_all(authors)

    books = [
        Book(id=1, title="The Silent River", royalty_per_sale=45, author_id=1),
        Book(id=2, title="Midnight in Mumbai", royalty_per_sale=60, author_id=1),
        Book(id=3, title="Code & Coffee", royalty_per_sale=75, author_id=2),
        Book(id=4, title="Startup Diaries", royalty_per_sale=50, author_id=2),
        Book(id=5, title="Poetry of Pain", royalty_per_sale=30, author_id=2),
        Book(id=6, title="Garden of Words", royalty_per_sale=40, author_id=3),
    ]
    db.add_all(books)

    sales = [
        Sale(book_id=1, quantity=25, sale_date=date(2025, 1, 5)),
        Sale(book_id=1, quantity=40, sale_date=date(2025, 1, 12)),
        Sale(book_id=2, quantity=15, sale_date=date(2025, 1, 8)),
        Sale(book_id=3, quantity=60, sale_date=date(2025, 1, 3)),
        Sale(book_id=3, quantity=45, sale_date=date(2025, 1, 15)),
        Sale(book_id=4, quantity=30, sale_date=date(2025, 1, 10)),
        Sale(book_id=5, quantity=20, sale_date=date(2025, 1, 18)),
        Sale(book_id=6, quantity=10, sale_date=date(2025, 1, 20)),
    ]
    db.add_all(sales)

    db.commit()

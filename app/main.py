from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine, SessionLocal
from .seed import seed_data

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    db = SessionLocal()
    seed_data(db)
    db.close()

from fastapi import Depends
from sqlalchemy.orm import Session
from .models import Author, Withdrawal
from .database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def calculate(author):
    total = 0
    for b in author.books:
        for s in b.sales:
            total += s.quantity * b.royalty_per_sale
    withdrawn = sum(w.amount for w in author.withdrawals)
    return total, total - withdrawn


@app.get("/authors")
def get_authors(db: Session = Depends(get_db)):
    authors = db.query(Author).all()
    result = []
    for a in authors:
        total, balance = calculate(a)
        result.append({
            "id": a.id,
            "name": a.name,
            "total_earnings": total,
            "current_balance": balance
        })
    return result

from fastapi import HTTPException


@app.get("/authors/{author_id}")
def author_detail(author_id: int, db: Session = Depends(get_db)):
    author = db.query(Author).get(author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    total, balance = calculate(author)

    books = []
    for b in author.books:
        sold = sum(s.quantity for s in b.sales)
        books.append({
            "id": b.id,
            "title": b.title,
            "royalty_per_sale": b.royalty_per_sale,
            "total_sold": sold,
            "total_royalty": sold * b.royalty_per_sale
        })

    return {
        "id": author.id,
        "name": author.name,
        "email": author.email,
        "total_books": len(author.books),
        "total_earnings": total,
        "current_balance": balance,
        "books": books
    }


@app.get("/authors/{author_id}/sales")
def author_sales(author_id: int, db: Session = Depends(get_db)):
    author = db.query(Author).get(author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    sales = []
    for book in author.books:
        for s in book.sales:
            sales.append({
                "book_title": book.title,
                "quantity": s.quantity,
                "royalty_earned": s.quantity * book.royalty_per_sale,
                "sale_date": s.sale_date
            })

    sales.sort(key=lambda x: x["sale_date"], reverse=True)
    return sales


from datetime import date


@app.post("/withdrawals")
def create_withdrawal(data: dict, db: Session = Depends(get_db)):
    author = db.query(Author).get(data["author_id"])

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    amount = data["amount"]

    if amount < 500:
        raise HTTPException(status_code=400, detail="Minimum withdrawal ₹500")

    total, balance = calculate(author)

    if amount > balance:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    w = Withdrawal(
        amount=amount,
        status="pending",
        created_at=date.today(),
        author_id=author.id
    )

    db.add(w)
    db.commit()

    return {
        "id": w.id,
        "amount": amount,
        "status": "pending",
        "new_balance": balance - amount
    }

@app.get("/authors/{author_id}/withdrawals")
def get_withdrawals(author_id: int, db: Session = Depends(get_db)):
    author = db.query(Author).get(author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    ws = db.query(Withdrawal) \
        .filter(Withdrawal.author_id == author_id) \
        .order_by(Withdrawal.created_at.desc()) \
        .all()

    return ws



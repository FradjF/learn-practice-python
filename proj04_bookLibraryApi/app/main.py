from fastapi import FastAPI

app = FastAPI(
    title="Book Library API",
    description="API for managing a book collection",
    version="1.0.0"
)

BOOKS = [
    {
        "id": 1,
        "title": "Clean Code",
        "author": "Robert C. Martin"
    },
    {
        "id": 2,
        "title": "The Pragmatic Programmer",
        "author": "David Thomas"
    }
]

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}

@app.get("/books")
def get_books() -> list[dict[str, int | str]]:
    return BOOKS

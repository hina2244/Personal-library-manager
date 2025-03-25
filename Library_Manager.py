import streamlit as st
import sqlite3
import pandas as pd

# Database setup
conn = sqlite3.connect("library.db", check_same_thread=False)
cursor = conn.cursor()

# Create books table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        genre TEXT,
        year INTEGER
    )
""")
conn.commit()

# Function to add a book
def add_book(title, author, genre, year):
    cursor.execute("INSERT INTO books (title, author, genre, year) VALUES (?, ?, ?, ?)", (title, author, genre, year))
    conn.commit()

# Function to get all books
def get_books():
    cursor.execute("SELECT * FROM books")
    return cursor.fetchall()

# Function to search books
def search_books(query):
    cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR genre LIKE ?", ('%'+query+'%', '%'+query+'%', '%'+query+'%'))
    return cursor.fetchall()

# Function to delete a book
def delete_book(book_id):
    cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()

# Streamlit UI
st.title("📚 Personal Library Manager")

# Sidebar Menu
menu = st.sidebar.selectbox("Menu", ["Add Book", "View Library", "Search Books", "Delete Book"])

if menu == "Add Book":
    st.subheader("📖 Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    genre = st.text_input("Genre")
    year = st.number_input("Year", min_value=0, step=1)

    if st.button("Add Book"):
        if title and author:
            add_book(title, author, genre, year)
            st.success(f"'{title}' by {author} added successfully!")
        else:
            st.warning("Please enter both title and author.")

elif menu == "View Library":
    st.subheader("📚 Your Library")
    books = get_books()
    df = pd.DataFrame(books, columns=["ID", "Title", "Author", "Genre", "Year"])
    st.dataframe(df)

elif menu == "Search Books":
    st.subheader("🔍 Search for Books")
    query = st.text_input("Enter title, author, or genre")
    
    if query:
        results = search_books(query)
        if results:
            df = pd.DataFrame(results, columns=["ID", "Title", "Author", "Genre", "Year"])
            st.dataframe(df)
        else:
            st.warning("No matching books found.")

elif menu == "Delete Book":
    st.subheader("❌ Delete a Book")
    books = get_books()
    
    if books:
        book_id = st.selectbox("Select Book to Delete", [f"{b[0]} - {b[1]} ({b[2]})" for b in books])
        selected_id = int(book_id.split(" - ")[0])
        
        if st.button("Delete"):
            delete_book(selected_id)
            st.success("Book deleted successfully!")
    else:
        st.warning("No books available to delete.")

st.write("📖 *Manage your personal library with ease!*")

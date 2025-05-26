# streamlit_app.py
# Streamlit UI for Personal Library Manager
import streamlit as st
import json
import os

LIBRARY_FILE = 'library.txt'

# Load and save functions

def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_library(library):
    with open(LIBRARY_FILE, 'w', encoding='utf-8') as f:
        json.dump(library, f, indent=2)

# Streamlit UI
st.set_page_config(page_title="Personal Library Manager", page_icon="📚", layout="centered")

# Custom CSS for colors and style
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .stButton>button {
        background-color: #4f8cff;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        padding: 0.5em 2em;
    }
    .stTextInput>div>div>input {
        background-color: #eaf0fb;
        border-radius: 6px;
    }
    .stSelectbox>div>div>div>div {
        background-color: #eaf0fb;
        border-radius: 6px;
    }
    .stDataFrame {
        background-color: #fff;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📚 Personal Library Manager")

library = load_library()

menu = st.sidebar.radio(
    "Menu",
    ("Add a book", "Remove a book", "Search for a book", "Display all books", "Display statistics")
)

if menu == "Add a book":
    st.header("Add a Book")
    with st.form("add_book_form"):
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", min_value=0, max_value=2100, step=1)
        genre = st.text_input("Genre")
        read = st.selectbox("Have you read this book?", ("No", "Yes"))
        submitted = st.form_submit_button("Add Book")
        if submitted:
            if not title or not author or not genre:
                st.error("Please fill in all fields.")
            else:
                book = {
                    'title': title,
                    'author': author,
                    'year': int(year),
                    'genre': genre,
                    'read': read == "Yes"
                }
                library.append(book)
                save_library(library)
                st.success("Book added successfully!")

elif menu == "Remove a book":
    st.header("Remove a Book")
    titles = [b['title'] for b in library]
    if titles:
        book_to_remove = st.selectbox("Select a book to remove", titles)
        if st.button("Remove Book"):
            library = [b for b in library if b['title'] != book_to_remove]
            save_library(library)
            st.success("Book removed successfully!")
    else:
        st.info("No books to remove.")

elif menu == "Search for a book":
    st.header("Search for a Book")
    search_by = st.radio("Search by", ("Title", "Author"))
    query = st.text_input(f"Enter the {search_by.lower()}")
    if query:
        if search_by == "Title":
            matches = [b for b in library if query.lower() in b['title'].lower()]
        else:
            matches = [b for b in library if query.lower() in b['author'].lower()]
        if matches:
            st.write("### Matching Books:")
            for i, b in enumerate(matches, 1):
                status = 'Read' if b['read'] else 'Unread'
                st.write(f"{i}. {b['title']} by {b['author']} ({b['year']}) - {b['genre']} - {status}")
        else:
            st.warning("No matching books found.")

elif menu == "Display all books":
    st.header("Your Library")
    if library:
        for i, b in enumerate(library, 1):
            status = 'Read' if b['read'] else 'Unread'
            st.write(f"{i}. {b['title']} by {b['author']} ({b['year']}) - {b['genre']} - {status}")
    else:
        st.info("Your library is empty.")

elif menu == "Display statistics":
    st.header("Library Statistics")
    total = len(library)
    if total == 0:
        st.info("No books in library.")
    else:
        read_count = sum(1 for b in library if b['read'])
        percent = (read_count / total) * 100
        st.metric("Total books", total)
        st.metric("Percentage read", f"{percent:.1f}%")

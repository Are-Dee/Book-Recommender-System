import streamlit as st
import pickle
import numpy as np
import zipfile

# Function to extract and load the pickle file from a zip
def load_pickle_from_zip(zip_path, pickle_filename):
    with zipfile.ZipFile(zip_path, 'r') as z:
        with z.open(pickle_filename) as f:
            return pickle.load(f)

# Load the pre-trained models and data
with open('popular.pkl', 'rb') as f:
    popular_df = pickle.load(f)
with open('pt.pkl', 'rb') as f:
    pt = pickle.load(f)

# Use the function to load books.pkl from the zip file
books = load_pickle_from_zip('books_pkl.zip', 'books.pkl')

with open('similarity_scores.pkl', 'rb') as f:
    similarity_scores = pickle.load(f)

# Initialize session state to store the "To Read" list
if 'to_read_list' not in st.session_state:
    st.session_state.to_read_list = []

# Function to add book to "To Read" list
def add_to_read_list(book_title):
    if book_title not in [book['title'] for book in st.session_state.to_read_list]:
        st.session_state.to_read_list.append({"title": book_title, "read": False})
        st.success(f"Added '{book_title}' to your To Read list!")

st.title("Book Recommender System 📚")
st.set_page_config(
    page_icon="📚")

st.sidebar.info("""
### 🚀 Welcome to The Book Recommender System! 
Use the navigation below to explore popular books, get recommendations, and manage your To Read list.""")

st.sidebar.header("Navigation")

# Add sections to the sidebar
section = st.sidebar.radio("Go to", ["Home", "Recommend", "To Read List"])

st.markdown(
    """
    <style>
    .css-145kmo2 {
        width: 250px;
    }
    .css-145kmo2 div[role="button"] {
        pointer-events: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Custom CSS for cards
st.markdown(
    """
    <style>
    .card {
        background-color: #CCCCCC;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 18px 18px rgba(0, 0, 0, 0.2);
        margin-bottom: 20px;
        height: 520px; /* Fixed height */
        overflow: hidden
        justify-content: space-between;
        transition: transform 0.3s ease-in-out;
    }
    .card-1 {
        background-color: #CCCCCC;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 18px 18px rgba(0, 0, 0, 0.2);
        margin-bottom: 20px;
        height: 320px; /* Fixed height */
        overflow: hidden
        justify-content: space-between;
        transition: transform 0.3s ease-in-out;
    }
    .card:hover {
        transform: scale(1.05);
    }
    .card img {
        max-height: 150px;
        object-fit: cover;
    }
    .card-content {
        flex-grow: 1;
    }
    .card button {
        align-self: center;
    }
    .modal-container {
        display: none;
        position: fixed;
        z-index: 1;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        overflow: auto;
        background-color: rgba(0,0,0,0.4);
    }
    .modal-content {
        background-color: #fefefe;
        margin: 15% auto;
        padding: 20px;
        border: 1px solid #888;
        width: 80%;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        position: relative;
    }
    .close {
        color: #aaa;
        float: right;
        font-size: 28px;
        font-weight: bold;
        cursor: pointer;
    }
    .close:hover,
    .close:focus {
        color: black;
        text-decoration: none;
        cursor: pointer;
    </style>
    """,
    unsafe_allow_html=True
)

# JavaScript for modal functionality
modal_js = """
<script>
function openModal(id) {
    var modal = document.getElementById(id);
    modal.style.display = "block";
}

function closeModal(id) {
    var modal = document.getElementById(id);
    modal.style.display = "none";
}
</script>
"""
# Add the JavaScript to the app
st.markdown(modal_js, unsafe_allow_html=True)

# Popular books section
if section == "Home":
    st.header("Popular Books")
    num_columns = 3  # Number of columns in the grid
    num_books = st.sidebar.slider("Number of books to display", min_value=5, max_value=100, value=15)

    columns = st.columns(num_columns)
    for i in range(min(num_books, len(popular_df))):
        col = columns[i % num_columns]
        with col:
            # Display book details in a card
            st.markdown(
                f"""
                <div class="card">
                    <img src="{popular_df['Image-URL-M'].values[i]}" alt="Book cover">
                    <div class="card-content">
                        <h4>{popular_df['Book-Title'].values[i]}</h4>
                        <p><strong>Author:</strong> {popular_df['Book-Author'].values[i]}</p>
                        <p><strong>Rating:</strong> {popular_df['avg_rating'].values[i]} ({popular_df['num_ratings'].values[i]} votes)</p>
                    </div>
                </div>
                
                <!-- Modal content -->
                <div id="modal_{i}" class="modal-container" onclick="closeModal('modal_{i}')">
                    <div class="modal-content">
                        <span class="close" onclick="closeModal('modal_{i}')">&times;</span>
                        <h2>{popular_df['Book-Title'].values[i]}</h2>
                        <p><strong>Author:</strong> {popular_df['Book-Author'].values[i]}</p>
                        <p><strong>Rating:</strong> {popular_df['avg_rating'].values[i]} ({popular_df['num_ratings'].values[i]} votes)</p>
                        <!-- Additional details or actions can be added here -->
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Add button to add to "To Read" list
            book_title = popular_df['Book-Title'].values[i]
            if st.button(f"Add to To Read", key=f"add_home_{book_title.replace(' ', '_')}"):
                add_to_read_list(book_title)

# Recommendation section
elif section == "Recommend":
    st.header("Recommend Books")
    selected_book = st.selectbox("Select a book", popular_df['Book-Title'].values)

    if st.button("Search"):
        if selected_book:
            try:
                index = np.where(pt.index == selected_book)[0][0]
                similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

                for i, item in enumerate(similar_items):
                    temp_df = books[books['Book-Title'] == pt.index[item[0]]]

                    # Display book details in a card-like layout
                    st.markdown(
                        f"""
                        <div class="card-1">
                            <img src="{temp_df['Image-URL-M'].values[0]}" alt="Book cover">
                            <div class="card-content">
                                <h4>{temp_df['Book-Title'].values[0]}</h4>
                                <p><strong>Author:</strong> {temp_df['Book-Author'].values[0]}</p>
                            </div>
                        </div>
                        
                        <!-- Modal content -->
                        <div id="modal_{i}" class="modal-container" onclick="closeModal('modal_{i}')">
                            <div class="modal-content">
                                <span class="close" onclick="closeModal('modal_{i}')">&times;</span>
                                <h2>{temp_df['Book-Title'].values[0]}</h2>
                                <p><strong>Author:</strong> {temp_df['Book-Author'].values[0]}</p>
                                <!-- Additional details or actions can be added here -->
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            except IndexError:
                st.error("Book not found. Please check the spelling or try another book.")

# To Read List section
elif section == "To Read List":
    st.header("To Read List")

    if st.session_state.to_read_list:
        for book in st.session_state.to_read_list:
            book_title = book['title']
            read_checkbox = st.checkbox(f"{book_title}", key=f"read_{book_title.replace(' ', '_')}", value=book['read'])
            
            # Update the book's read status
            book['read'] = read_checkbox
            
            # Highlight read books with a strikethrough
            if book['read']:
                st.markdown(f"~~**{book_title}**~~", unsafe_allow_html=True)
            else:
                st.markdown(f"**{book_title}**", unsafe_allow_html=True)
    else:
        st.write("Your To Read list is empty.")

# Footer section
st.sidebar.markdown("---")
st.sidebar.write("")
st.sidebar.info("""
###  Developed By Raghav Dhawan""")
st.sidebar.write("Contact: [raghavdhawan524@gmail.com](mailto:raghavdhawan524@gmail.com)")

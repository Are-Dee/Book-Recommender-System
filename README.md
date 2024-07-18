# Book Recommender System 📚

## Description
This project implements a Book Recommender System using [Streamlit](https://ultimate-brs.streamlit.app/), where users can explore popular books, get recommendations based on book similarity scores using collaborative filtering, and manage their "To Read" list.

## Features
- **Home Page:**
  - Displays popular books based on average ratings from users who rated more than 250 books.
  - Allows users to add books to their "To Read" list.

- **Recommendation Page:**
  - Users can select a book and get recommendations based on similarity scores with other books in the dataset using collaborative filtering.
  - Top 4 most similar books are recommended.

- **To Read List:**
  - Displays the list of books added by the user to read.
  - Allows users to mark books as read/unread.

## Popularity-Based System
- The Home Page showcases popular books based on average ratings from users who have rated more than 250 books. The top 100 most popular books are displayed.

## Collaborative Filtering
- The Recommendation Page utilizes collaborative filtering to recommend books based on similarity scores between books. It calculates the similarity between selected books and suggests the top 4 most similar books.

## Setup Instructions
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your_username/book-recommender-system.git
   cd book-recommender-system
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
3. **Run the Application:**
   ```bash
   streamlit run app.py

## Here's how it turned out:
 ![Screenshot from 2024-07-18 14-07-51](https://github.com/user-attachments/assets/67adf06a-dece-413f-866d-3c30adef12d3)



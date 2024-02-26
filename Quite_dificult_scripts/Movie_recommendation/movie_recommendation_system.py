# Python
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Load Movies Metadata
movies = pd.read_csv(r'C:\Users\Usuario\Desktop\Útiles\Proyectos\Python_Scripts\Quite_dificult_scripts\Movie_recommendation\movies.csv', low_memory=False)

# Print the first three movies
print(movies.head(3))

# Check if 'overview' column exists
if 'overview' not in movies.columns:
    print("'overview' column does not exist in the DataFrame.")
else:
    # Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
    tfidf = TfidfVectorizer(stop_words='english')

    # Replace NaN with an empty string
    movies['overview'] = movies['overview'].fillna('')

    # Construct the required TF-IDF matrix by fitting and transforming the data
    tfidf_matrix = tfidf.fit_transform(movies['overview'])

    # Output the shape of tfidf_matrix
    print(tfidf_matrix.shape)

    # Compute the cosine similarity matrix
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # Construct a reverse map of indices and movie titles
    indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()

    def get_recommendations(title, cosine_sim=cosine_sim):
        # Get the index of the movie that matches the title
        idx = indices[title]

        # Get the pairwise similarity scores of all movies with that movie
        sim_scores = list(enumerate(cosine_sim[idx]))

        # Sort the movies based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the scores of the 10 most similar movies
        sim_scores = sim_scores[1:11]

        # Get the movie indices
        movie_indices = [i[0] for i in sim_scores]

        # Get the movie titles
        movie_titles = movies['title'].iloc[movie_indices]

        # Get the similarity scores
        movie_scores = [i[1] for i in sim_scores]

        # Return the top 10 most similar movies with their scores
        return pd.DataFrame({'Title': movie_titles, 'Score': movie_scores})

    # Get recommendations for a movie
    recommendations = get_recommendations('The Dark Knight Rises')

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.barh(recommendations['Title'][::-1], recommendations['Score'][::-1])
    plt.xlabel('Similarity Score')
    plt.title('Top Movie Recommendations')
    plt.show()

    # Test the function with a movie title
    print(get_recommendations('The Dark Knight Rises'))
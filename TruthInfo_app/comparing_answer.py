from sentence_transformers import SentenceTransformer
import scipy.spatial
import streamlit as st
# from similer_search import *
import pandas as pd

# Load the sentence transformer model
models = SentenceTransformer('all-MiniLM-L6-v2')


def encode_answers_safe(models, answers):
    # Ensure 'answers' is a list of strings
    
    string_list = []
    for item in answers:
        if isinstance(item, str):
            string_list.append(item)
        else:
            try:
                # Attempt to convert to string
                string_list.append(str(item))
            except Exception as e:
                # If conversion fails, skip the item or handle it as needed
                print(f"Skipping item due to error in conversion to string: {e}")
    
    # Encode the answers using the provided model
    # embeddings = model.encode(answers).tolist()
    embeddings=models.encode(string_list).tolist()
    return embeddings



def compute_similarities(database_answers, openai_answers):
    # Generate embeddings for all answers
    # print(openai_answers)
    # print(database_answers)
    try:
        # Safely encode 'database_answers'
        db_embeddings = encode_answers_safe(models, database_answers)
        # Safely encode 'openai_answers'
        openai_embeddings = encode_answers_safe(models, openai_answers)

    except ValueError as e:
        print(f"Error: {e}")

    
    # Initialize a matrix to hold similarity scores
    similarity_matrix = []

    # Calculate the cosine similarity between each pair of answers
    for db_embedding in db_embeddings:
        similarities = []
        for openai_embedding in openai_embeddings:
            cosine_similarity = 1 - scipy.spatial.distance.cosine(db_embedding, openai_embedding)
            similarities.append(cosine_similarity)
        similarity_matrix.append(similarities)
        # print(similarity_matrix)
    # Display answers with their similarity scores
    data_rows = []

    for db_index, db_answer in enumerate(database_answers):
        for openai_index, openai_answer in enumerate(openai_answers):
            similarity_score = similarity_matrix[db_index][openai_index]
        # Add a row for each comparison
            if similarity_score > 0.60:
                # Add a row for each comparison with similarity score greater than 0.50
                data_rows.append({
                    "Database Answer": f"Answer {db_index + 1}: {db_answer}",
                    "OpenAI Answer": f"Answer {openai_index + 1}: {openai_answer}",
                    "Similarity Score": similarity_score
                })
                print("answers are similer")
                return similarity_score
            else:
                print("No matches were found.")
                return

# Display the DataFrame using st.table or st.dataframe
    # st.table(df)




#     # Display answers with their similarity scores
#     for db_index, db_answer in enumerate(database_answers):
#         print(f"Database Answer {db_index+1}: {db_answer}")
#         for openai_index, openai_answer in enumerate(openai_answers):
#             similarity_score = similarity_matrix[db_index][openai_index]
#             print(f"  vs. OpenAI Answer {openai_index+1}: {openai_answer}")
#             print(f"  SIMILARITY SCORE: {similarity_score:.4f}")
#             print("-" * 50)
#         print("-" * 150)
#     # return similarity_score

# # Example usage with multiple answers






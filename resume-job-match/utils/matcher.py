import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_jobs(resume_text, jobs_df):
    # Combine description + skills for better matching
    jobs_df['combined'] = jobs_df['description'] + " " + jobs_df['skills']

    corpus = jobs_df['combined'].tolist() + [resume_text]

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(corpus)

    similarity = cosine_similarity(vectors[-1], vectors[:-1])

    jobs_df['match_score'] = similarity.flatten() * 100

    return jobs_df.sort_values(by='match_score', ascending=False)
import pandas as pd
import numpy as np
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier
import joblib

# Read the data from the CSV file
df = pd.read_csv('output.csv')

# Convert the 'tags' column from string to list
df['tags'] = df['tags'].apply(lambda x: ast.literal_eval(x))

# Initialize MultiLabelBinarizer and transform the 'tags' column to classes
multilabel = MultiLabelBinarizer()
y = multilabel.fit_transform(df['tags'])

# Initialize TF-IDF Vectorizer
tfidf = TfidfVectorizer(analyzer='word', max_features=10000, ngram_range=(1, 3), stop_words='english')
X = tfidf.fit_transform(df['title'])

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Define the classifiers
classifiers = [SGDClassifier(), LogisticRegression(solver='lbfgs'), LinearSVC()]

# Define the Jaccard score calculation function
def j_score(y_true, y_pred):
    jaccard = np.minimum(y_true, y_pred).sum(axis=1) / np.maximum(y_true, y_pred).sum(axis=1)
    return jaccard.mean() * 100

# Define the function to print Jaccard scores for classifiers
def print_score(y_pred, clf):
    print("Classifier: ", clf.__class__.__name__)
    print("Jaccard score: {}".format(j_score(y_test, y_pred)))
    print("-----")

# Train classifiers and print scores
for classifier in classifiers:
    clf = OneVsRestClassifier(classifier)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print_score(y_pred, classifier)

# Save the trained classifier to a file
joblib_file = "tagPredictor.pkl"
joblib.dump(clf, joblib_file)

# Load the trained classifier from the file
tagPredictorModel = joblib.load(joblib_file)

# Define a function to get tags for a question
def getTags(question):
    question_tfidf = tfidf.transform([question])
    predicted_tags_bin = tagPredictorModel.predict(question_tfidf)
    predicted_tags = multilabel.inverse_transform(predicted_tags_bin)
    print(predicted_tags)



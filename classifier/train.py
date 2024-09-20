import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.utils.class_weight import compute_class_weight
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report
import joblib

df = pd.read_csv('data.csv')

# load dataset
print(df['Category'].value_counts())

# text Preprocessing with N-grams
vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))  # adjust n-grams as needed
X = vectorizer.fit_transform(df['Title'])
y = df['Category']

# compute class weights
classes = df['Category'].unique()
class_weights = compute_class_weight(class_weight='balanced', classes=classes, y=y)
class_weight_dict = dict(zip(classes, class_weights))

# data splitting
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# tune hyperparameters
param_grid = {
    'C': [0.1, 1, 10],
    'kernel': ['linear', 'rbf'],
    'gamma': ['scale', 'auto']
}

svm_model = SVC(class_weight=class_weight_dict)

grid_search = GridSearchCV(svm_model, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
grid_search.fit(X_train, y_train)

# save the best model
best_model = grid_search.best_estimator_
joblib.dump(best_model, 'svm_model_weights.joblib') # Save the model to a file
joblib.dump(vectorizer, 'tfidf_vectorizer.joblib')  # Save the vectorizer


# model evaluation
y_pred = best_model.predict(X_test)

print(f"Best Parameters: {grid_search.best_params_}")
print(classification_report(y_test, y_pred))

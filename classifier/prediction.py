import pandas as pd
import joblib

# load trained model
best_model = joblib.load('weights/svm_model_weights.joblib')

# new data for prediction
def pred(new_data):

    # load the saved vectorizer and transform the new data
    vectorizer = joblib.load('weights/tfidf_vectorizer.joblib')
    new_X = vectorizer.transform(new_data['Title'])

    # make predictions on the new data
    predictions = best_model.predict(new_X)
    new_data['Predicted Category'] = predictions

    # total amount for each individual category
    total_per_category = new_data.groupby('Predicted Category')['Price'].sum().reset_index()

    print("Updated Data with Predicted Categories and Prices:")
    print(new_data)

    # print("\nTotal Price per Category:")
    return total_per_category

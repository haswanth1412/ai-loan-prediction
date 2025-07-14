import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from data_preprocessing import load_data, preprocess_data

def train_model(data_path):
    df = load_data(data_path)
    X, y, preprocessor = preprocess_data(df)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    rf = RandomForestClassifier(random_state=42)

    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [10, 20, None],
        'min_samples_split': [2, 5]
    }

    grid_search = GridSearchCV(rf, param_grid, cv=5, scoring='roc_auc', n_jobs=-1)
    grid_search.fit(X_train, y_train)

    print(f"Best params: {grid_search.best_params_}")
    y_pred = grid_search.predict(X_test)
    y_proba = grid_search.predict_proba(X_test)[:,1]

    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    print(f"ROC-AUC Score: {roc_auc_score(y_test, y_proba):.4f}")

    joblib.dump(grid_search.best_estimator_, 'model.pkl')
    joblib.dump(preprocessor, 'preprocessor.pkl')

if __name__ == "__main__":
    train_model('data/loans.csv')

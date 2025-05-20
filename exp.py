import sys
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import pandas as pd

# Parse input argument (seed)
if len(sys.argv) != 2:
    print("Usage: exp.py <seed>")
    sys.exit(1)

seed = int(sys.argv[1])

# Fixed parameters
NUM_REPETITIONS = 5  # Set the number of repetitions here

# Define classifiers
classifiers = {
    'SVM': SVC(),
    'LogisticRegression': LogisticRegression(),
    'KNN': KNeighborsClassifier()
}

all_results = []

for rep in range(NUM_REPETITIONS):
    current_seed = rep* (seed-1) + rep
    np.random.seed(current_seed)

    # Generate synthetic data
    X, y = make_blobs(n_samples=300, centers=3, n_features=2, random_state=current_seed)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=current_seed)

    # Train and evaluate classifiers
    for name, clf in classifiers.items():
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        all_results.append({'Classifier': name, 'Accuracy': accuracy, 'Seed': current_seed, 'Repetition': rep + 1})

# Store results
df = pd.DataFrame(all_results)
output_file = f"results/seed{seed}.txt"
df.to_csv(output_file, index=False, sep='\t')
print(f"Results saved to {output_file}")
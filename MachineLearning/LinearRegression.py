'''
Docstring for MachineLearning.LinearRegression
Linear Regression is one of the simplest and most powerful algorithms in supervised machine learning.
 It helps us understand the relationship between input variables (features) and an output variable (target) 
 by fitting a straight line through the data.
'''
import numpy as np
class LinearRegression:
    def __init__(self):
        self.slope=None
        self.intercept=None
    def fit(self,X,Y):
        '''
        Docstring for fit
        
        :param self: Description
        :param X: column
        :param Y:cloumn
        Slope and intercept
        slope=sum(x-x_mean)(y-y_mean)/sum(x-x_mean)2
        '''
        X_mean=np.mean(X)
        Y_mean=np.mean(Y)

        numerator=np.mean((X-X_mean)*(Y-Y_mean))
        denominator=np.mean((X-X_mean)**2)

        self.slope=numerator/denominator

        self.intercept=Y_mean-(self.slope*X_mean)

        print(f"Training Complete!")
        print(f"Slope (m): {self.slope:.4f}")
        print(f"Intercept (c): {self.intercept:.4f}")
        print(f"Equation: Y = {self.slope:.4f}X + {self.intercept:.4f}")
    def predict(self,X):
        if self.slope is None or self.intercept is None:
            raise Exception("Model not trained yet! Call fit() first.")
        return self.slope * X + self.intercept
    def calculate_mse(self, y_actual, y_pred):
        """
        Calculate Mean Squared Error
        
        Why we use MSE:
        - Measures how far predictions are from actual values (model accuracy)
        - Squares errors to: (1) make all values positive, (2) penalize large errors more
        - Lower MSE = better model performance
        - Takes the mean to get average error across all predictions
        """
        # Formula: MSE = (1/n) × Σ(actual - predicted)²
        # Why np.mean: Automatically sums squared differences and divides by count
        return np.mean((y_actual - y_pred) ** 2)
if __name__ == "__main__":
    # Why this check: Ensures code runs only when script is executed directly
    # (not when imported as a module)
    
    # Our dataset: Study Hours vs Exam Scores
    # Why np.array: NumPy arrays enable vectorized operations (faster than Python lists)
    # Why this data: Simple example to demonstrate linear relationship
    X = np.array([1, 2, 3, 4, 5])
    y = np.array([2, 4, 5, 4, 5])
    
    # Print header for better output formatting
    # Why "=" * 50: Creates a visual separator for readability
    print("=" * 50)
    print("LINEAR REGRESSION FROM SCRATCH")
    print("=" * 50)
    
    # Display the dataset we're working with
    # Why: Allows user to see the raw data before training
    print("\nDataset:")
    print("Study Hours (X):", X)
    print("Exam Scores (Y):", y)
    print()
    
    # Create an instance of our custom Linear Regression class
    # Why: Object-oriented approach keeps code organized and reusable
    model = LinearRegression()
    
    # Train the model with our data
    # Why fit: Calculates slope and intercept from training data
    model.fit(X, y)
    
    # Section header for predictions
    print("\n" + "=" * 50)
    print("PREDICTIONS")
    print("=" * 50)
    
    # Generate predictions for our training data
    # Why predict on training data: To see how well model learned the relationship
    predictions = model.predict(X)
    
    # Display each prediction alongside actual value
    # Why loop: Shows detailed comparison for each data point
    # Why .2f: Formats numbers to 2 decimal places for readability
    for i in range(len(X)):
        print(f"Study Hours: {X[i]} → Predicted Score: {predictions[i]:.2f} (Actual: {y[i]})")
    
    # Calculate and display Mean Squared Error
    # Why: Quantifies model accuracy with a single metric
    mse = model.calculate_mse(y, predictions)
    print(f"\nMean Squared Error (MSE): {mse:.4f}")
    
    # Section header for testing with new data
    print("\n" + "=" * 50)
    print("TESTING WITH NEW DATA")
    print("=" * 50)
    new_hours = np.array([2.5, 6, 7])
    
    # Make predictions on new data
    # Why: Demonstrates the practical use of our trained model
    new_predictions = model.predict(new_hours)
    
    # Display predictions for new data
    # Why: Shows model can handle unseen values
    for i in range(len(new_hours)):
        print(f"Study Hours: {new_hours[i]} → Predicted Score: {new_predictions[i]:.2f}")
    
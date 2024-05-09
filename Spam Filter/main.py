import numpy as np #sourcecode by assemblyAi

def sigmoid(x): #definition of sigmoid function
    return 1/(1+np.exp(-x))

class LogisticRegression():

    def __init__(self, lr=0.001, n_iters=1000): #we apply the learning rate and number of iterations
        self.lr = lr
        self.n_iters = n_iters
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        for _ in range(self.n_iters): #prediction function
            linear_pred = np.dot(X, self.weights) + self.bias
            predictions = sigmoid(linear_pred)

            dw = (1/n_samples) * np.dot(X.T, (predictions - y)) #gradient
            db = (1/n_samples) * np.sum(predictions-y)

            self.weights = self.weights - self.lr*dw #weight
            self.bias = self.bias - self.lr*db #bias


    def predict(self, X):
        linear_pred = np.dot(X, self.weights) + self.bias #function which assigns the value of a prediction to 0 or 1
        y_pred = sigmoid(linear_pred) #if a prediction is above 0.5, it is labeled as 1, if it is below 0.5, it is
        class_pred = [0 if y<=0.5 else 1 for y in y_pred] #labeled as 0
        return class_pred
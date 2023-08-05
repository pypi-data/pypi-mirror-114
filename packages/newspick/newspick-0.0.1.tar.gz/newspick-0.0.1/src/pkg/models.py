class Model:
  
  def __init__(self):
    self.model = ""
    
  def get_training_data(self):
      from sklearn.datasets import load_iris
      X, y = load_iris(return_X_y = True)
      return X, y

  def format_input(self, X):
      return X
  
  def fit_model(self, X, y):
      from sklearn.neighbors import KNeighborsClassifier
      X = self.format_input(X)
      model = KNeighborsClassifier()
      model.fit(X, y)
      return model
 
  def build_model(self):
      X, y = self.get_training_data()
      model = self.fit_model(X, y)
      setattr(self, "model", model)
      return "Model was successfully build"
      
  def predict(self, X):
      X = self.format_input(X)
      model = self.model
      preds = model.predict(X)
      return preds

  def parse_input(self, json):
      import numpy as np
      samples = [np.array(list(obs.values()), ndmin = 2) for obs in json]
      samples = np.concatenate(samples, axis = 0)
      return(samples)
    
  def parse_output(self, preds):
      preds_out = preds.tolist()
      preds_json = {'predictions': preds_out}
      return preds_json



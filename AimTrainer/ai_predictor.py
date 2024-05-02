import numpy as np
from sklearn.cluster import KMeans

class AIPredictor:
    def __init__(self, history_size=100, n_clusters=3):
        self.history_size = history_size
        self.n_clusters = n_clusters
        self.click_history = []

    def update_history(self, click_position):
        self.click_history.append(click_position)
        if len(self.click_history) > self.history_size:
            self.click_history.pop(0)

    def predict_next_click(self):
        if len(self.click_history) < self.n_clusters:
            return None  
        model = KMeans(n_clusters=self.n_clusters)
        model.fit(np.array(self.click_history))
        predictions = model.cluster_centers_
        return predictions.tolist()

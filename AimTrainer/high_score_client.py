import requests

class HighScoreClient:
    SERVER_URL = "http://localhost:5000"

    @staticmethod
    def submit_score(player_name, score):
        response = requests.post(f"{HighScoreClient.SERVER_URL}/submit", json={"player": player_name, "score": score})
        return response.json()

    @staticmethod
    def get_high_scores():
        response = requests.get(f"{HighScoreClient.SERVER_URL}/scores")
        return response.json()['high_scores']

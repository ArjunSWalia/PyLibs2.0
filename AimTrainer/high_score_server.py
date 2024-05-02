from flask import Flask, request, jsonify

app = Flask(__name__)
high_scores = []

@app.route('/submit', methods=['POST'])
def submit_score():
    score_data = request.json
    high_scores.append(score_data)
    high_scores.sort(key=lambda x: x['score'], reverse=True)
    return jsonify(success=True)

@app.route('/scores', methods=['GET'])
def get_scores():
    return jsonify(high_scores=high_scores[:10])

if __name__ == "__main__":
    app.run(port=5000)

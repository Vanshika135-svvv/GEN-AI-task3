import os
import markovify
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    user_corpus = data.get('corpus', '')
    size = data.get('size', 'medium')

    # Markov chains need at least a bit of data to find patterns
    if not user_corpus or len(user_corpus.split()) < 5:
        return jsonify({'text': "I need a few more words to start cooking, bestie!", 'stats': 'Too Short'}), 400

    try:
        # Build the statistical model locally
        # state_size=2 is standard for word-based probability
        text_model = markovify.Text(user_corpus, state_size=2)
        
        # Determine how many sentences to generate based on UI selection
        count = 1
        if size == "medium": count = 3
        if size == "long": count = 6

        results = []
        for _ in range(count):
            # test_output=False prevents errors on small datasets by allowing repeats
            sentence = text_model.make_sentence(tries=100, test_output=False) or \
                       text_model.make_short_sentence(140, tries=100, test_output=False)
            if sentence:
                results.append(sentence)

        output_text = " ".join(results)

        return jsonify({
            'text': output_text if output_text else "The vibes are too unique. Add more text!",
            'word_count': len(output_text.split())
        })
    except Exception as e:
        return jsonify({'text': f"System Error: {str(e)}", 'stats': 'Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
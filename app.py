from flask import Flask, render_template, request

from models import SoilFertilityTester

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('front_page.html')

@app.route('/products')
def products():
    return render_template('products_page.html')

@app.route('/api/fertility', methods=['POST'])
def fertilityapi():
    context = request.get_json()
    sft = SoilFertilityTester(context['input'])

    score = sft.predictFertility()
    analy = sft.analyseSample()

    return {
        'score1': (float)(score),
        'dev': analy['dev'],
        'verdict': analy['verdict'],
        'score': analy['devscore'],
        'colorarr': analy['colorarr'],
        'crops': analy['crops']
    }


if __name__ == '__main__':
    app.run('0.0.0.0', 8000, debug=True)
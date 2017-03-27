from flask import Flask, render_template, request, redirect, url_for
import os, requests, pprint

app = Flask(__name__)


@app.route('/')
@app.route('/index.html')
def hello_world():
    return render_template('index.html')

@app.route('/application.html')
def second():
    return render_template('application.html')

@app.route('/application.html',methods=['POST'])
def performSearch():
    term = request.form['searchTerm']
    zipCode = request.form['zipCode']
    rad = 1609 * request.form['radius']
    lim = request.form['limit']
    deal = request.form['deals']

    userInfo = {
        'term': term,
        'location': zipCode,
        'radius_filter': rad,
        'limit': lim,
        'deals_filter': deal
    }

    app_id = 'H-HZgNDkCrVwWodMt-n8KA'
    app_secret = '5BXCx3WWi0uIhjPy6s1DehHasBxYnTgbFSnoDv210B656x7uMmUiy8JSGrmNp9mX'
    data = {'grant_type': 'client_credentials',
            'client_id': app_id,
            'client_secret': app_secret}
    token = requests.post('https://api.yelp.com/oauth2/token', data=data)
    access_token = token.json()['access_token']
    url = 'https://api.yelp.com/v3/businesses/search'
    headers = {'Authorization': 'bearer %s' % access_token}
    resp = requests.get(url=url, params=userInfo, headers=headers)
    pprint.pprint(resp.json()['businesses'])
    return ('', 204)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
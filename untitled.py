from flask import Flask, render_template, request, redirect, url_for, Response
import os, requests, json, pprint, jsonify
from flask_googlemaps import GoogleMaps, Map, icons

app = Flask(__name__)
GoogleMaps(app)



@app.route('/')
@app.route('/index.html')
def hello_world():
    return render_template('index.html')

@app.route('/application.html')
def secondPage():
    mymap = Map(
        identifier="view-side",
        lat=30.2672,
        lng=-97.7431,
        markers={icons.dots.green: [(30.2672, -97.7431)]},
        style="height: 100%; width: 100%"
    )
    return render_template('application.html', mymap=mymap)

@app.route('/application.html', methods=['GET','POST'])
def performSearch():
    if(request.method == 'POST'):
        term = request.form.get('searchTerm')
        loc = request.form.get('location')
        rad = request.form.get('radius')
        lim = request.form.get('limit')
        userInfo = {
            'term': term,
            'location': loc,
            'radius_filter': rad,
            'limit': lim,
        }
        json_data = getResponse(userInfo)
        print(json_data)
        latCenter = json_data['region']['center']['latitude']
        lngCenter = json_data['region']['center']['longitude']
        newMarkers = []
        for bus in json_data['businesses']:
            long = bus['coordinates']['longitude']
            lat = bus['coordinates']['latitude']
            newMarkers.append((lat, long))
            print(long)
            print(lat)
        print(newMarkers)
        mymap = Map(
            identifier="view-side",
            lat=30.2672,
            lng=-97.7431,
            markers={'http://maps.google.com/mapfiles/ms/icons/blue-dot.png': newMarkers},
            style="height: 100%; width: 100%"
        )
        return render_template('application.html', mymap=mymap)

def getResponse(userInfo):
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
    json_data = json.loads(resp.text)
    return json_data

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
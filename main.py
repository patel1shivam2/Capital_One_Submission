from flask import Flask, render_template, request, redirect, url_for, Response
import os, requests, json, pprint, jsonify
from flask_googlemaps import GoogleMaps, Map, icons

app = Flask(__name__)
GoogleMaps(app, key="AIzaSyDHvkt3LljCyZ_WhFeys7NiGF9H6SCBzss")


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
        style="height: 100%; width: 100%"
    )
    return render_template('application.html', mymap=mymap)

@app.route('/application.html', methods=['POST'])
def performSearch():
    if (request.method == 'POST'):
        term = request.form.get('searchTerm')
        loc = request.form.get('location')
        rad = request.form.get('radius')
        lim = request.form.get('limit')

        if rad > 25:
            rad = 25

        if rad == '':
            rad = 40000

        if lim == '':
            lim = 50


        userInfo = {
            'term': term,
            'location': loc,
            'radius_filter': rad,
            'limit': lim,
        }
        json_data = getResponse(userInfo)
        newMarkers = []
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(json_data)
        for bus in json_data['businesses']:
            temp = makeBox(bus)
            newMarkers.append(temp)
        mymap = Map(
            identifier="view-side",
            zoom=11,
            lat=json_data['region']['center']['latitude'],
            lng=json_data['region']['center']['longitude'],
            markers=newMarkers,
            style="height: 100%; width: 100%"
        )
        return render_template('application.html', mymap=mymap, results=json_data['businesses'])

def getReview(id):
    app_id = 'H-HZgNDkCrVwWodMt-n8KA'
    app_secret = '5BXCx3WWi0uIhjPy6s1DehHasBxYnTgbFSnoDv210B656x7uMmUiy8JSGrmNp9mX'
    data = {'grant_type': 'client_credentials',
            'client_id': app_id,
            'client_secret': app_secret}
    token = requests.post('https://api.yelp.com/oauth2/token', data=data)
    access_token = token.json()['access_token']
    url = "https://api.yelp.com/v3/businesses/" + id + "/reviews"
    headers = {'Authorization': 'bearer %s' % access_token}
    resp = requests.get(url=url, headers=headers)
    json_data = json.loads(resp.text)
    return json_data

def makeBox(bus):
    temp = {
        'lat': bus['coordinates']['latitude'],
        'lng': bus['coordinates']['longitude'],
        'infobox': ("<h3><a href=" + bus['url'] + " target=_blank>" + bus['name'] + "</a></h3>"
                    "<h5><img src=static/images/home.png style='max-width: 20px; max-height: 20px;'> " + bus['location']['display_address'][0]+ ", " + bus['location']['display_address'][1] + "</h5>"
                    "<h5><img src=static/images/phone.png style='max-width: 20px; max-height: 20px;'> " + bus['display_phone'] + "</h5>"
                    "<h5><img src=static/images/rating.png style='max-width: 20px; max-height: 20px;'> " + str(bus['rating']) + "</h5>")
    }
    if 'price' in bus:
        temp = {
            'lat': bus['coordinates']['latitude'],
            'lng': bus['coordinates']['longitude'],
            'infobox': ("<h3><a href=" + bus['url'] + " target=_blank>" + bus['name'] + "</a></h3>"
                        "<h5><img src=static/images/home.png style='max-width: 20px; max-height: 20px;'>  " + bus['location']['display_address'][0] + ", " + bus['location']['display_address'][1] + "</h5>"
                        "<h5><img src=static/images/phone.png style='max-width: 20px; max-height: 20px;'> " + bus['display_phone'] + "</h5>"
                        "<h5><img src=static/images/cash-other.png style='max-width: 20px; max-height: 20px;'> " + str(bus['price']) + "</h5>"
                        "<h5><img src=static/images/rating.png style='max-width: 20px; max-height: 20px;'> " + str(bus['rating']) + "</h5>")
        }
    return temp

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
    port = int(os.environ.get("PORT", 4000))
    app.run(host='0.0.0.0', port=port)
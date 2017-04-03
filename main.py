from flask import Flask, render_template, request
import os, requests, json, pprint
from flask_googlemaps import GoogleMaps, Map

key = "AIzaSyDHvkt3LljCyZ_WhFeys7NiGF9H6SCBzss"

app = Flask(__name__)
GoogleMaps(app, key=key)

latitude = 41.8781
longitude = -87.6298

@app.route('/')
@app.route('/index.html', methods=['GET','POST'])
def hello_world():
    return render_template('index.html')

@app.route('/application.html')
def secondPage():
    #request location of user on the call for the application page
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    url = 'http://freegeoip.net/json/' + ip
    r = requests.get(url)
    #convert response to JSON variable
    j = json.loads(r.text)
    #reset the global variables to the values retrieved by the API Request
    global latitude
    latitude = j['latitude']
    global longitude
    longitude = j['longitude']
    #Initialization of the Map Object
    mymap = Map(
        identifier="view-side",
        #set of lat and long centers to the new global variables
        lat=latitude,
        lng=longitude,
        style="height: 100%; width: 100%"
    )
    #return application page with the map parameter for rendering using Jinja2
    return render_template('application.html', mymap=mymap)

@app.route('/application.html', methods=['POST'])
def performSearch():
    #ensures method was called through POST request
    if (request.method == 'POST'):
        #retainment of the different form variables
        term = request.form.get('searchTerm')
        loc = request.form.get('location')
        rad = request.form.get('radius')
        lim = request.form.get('limit')
        open = request.form.get('open')
        sort = request.form.get('sortBy')
        single = request.form.get('price1')
        double = request.form.get('price2')
        triple = request.form.get('price3')
        four = request.form.get('price4')
        #variable holder for the price constraints
        price = ""
        #series of conditional statements to create the proper string to represent the users
        #price level restriction
        if single != None:
            price += str(str(1) + ",")
        if double != None:
            price += str(str(2) + ",")
        if triple != None:
            price += str(str(3) + ",")
        if four != None:
            price += str(4)
        if four == None and len(price) % 2 == 0:
            price = price[:-1]
        if len(price) == 0:
            price = "1,2,3,4"
        #checks radius element from form
        #ensures no error can be made through YELP API request
        if rad == '':
            rad = str(40000)
        else:
            rad = str(rad * 1609)
        #max case
        if int(rad) > 40000:
            rad = str(40000)
        if lim == '':
            lim = str(50)
        #establishment of API Request Parameters from formatted form elements
        userInfo = {
            'term': term,
            'location': loc,
            'radius_filter': rad,
            'limit': lim,
            'open_now': open,
            'price': price,
            'sort_by': sort
        }
        #helper method called to ease code statements
        json_data = getResponse(userInfo)
        #new array
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
    if bus['is_closed'] == True:
        temp = {
            'lat': bus['coordinates']['latitude'],
            'lng': bus['coordinates']['longitude'],
            'infobox': ("<h3><a href=" + bus['url'] + " target=_blank>" + bus['name'] + "</a></h3>"
                        "<h5 style='color: red'>Closed Now</h5>"
                        "<h5><img src=static/images/home.png style='max-width: 20px; max-height: 20px;'>  " +
                        bus['location']['display_address'][0] + ", " + bus['location']['display_address'][1] + "</h5>"
                        "<h5><img src=static/images/phone.png style='max-width: 20px; max-height: 20px;'> " +bus['display_phone'] + "</h5>"
                        "<h5><img src=static/images/cash-other.png style='max-width: 20px; max-height: 20px;'> " + str(bus['price']) + "</h5>"
                        "<h5><img src=static/images/rating.png style='max-width: 20px; max-height: 20px;'> " + str(bus['rating']) + "</h5>")
        }
    if bus['is_closed'] == False:
        temp = {
            'lat': bus['coordinates']['latitude'],
            'lng': bus['coordinates']['longitude'],
            'infobox': ("<h3><a href=" + bus['url'] + " target=_blank>" + bus['name'] + "</a></h3>"
                        "<h5 style='color: green'>Open Now</h5>"
                        "<h5><img src=static/images/home.png style='max-width: 20px; max-height: 20px;'>  " +
                        bus['location']['display_address'][0] + ", " + bus['location']['display_address'][1] + "</h5>"
                        "<h5><img src=static/images/phone.png style='max-width: 20px; max-height: 20px;'> " +bus['display_phone'] + "</h5>"
                        "<h5><img src=static/images/cash-other.png style='max-width: 20px; max-height: 20px;'> " + str(bus['price']) + "</h5>"
                        "<h5><img src=static/images/rating.png style='max-width: 20px; max-height: 20px;'> " + str(bus['rating']) + "</h5>")
        }
    if 'price' in bus:
        if bus['is_closed'] == False:
            temp = {
                'lat': bus['coordinates']['latitude'],
                'lng': bus['coordinates']['longitude'],
                'infobox': ("<h3><a href=" + bus['url'] + " target=_blank>" + bus['name'] + "</a></h3>"
                            "<h5 style='color: green'>Open Now</h5>"
                            "<h5><img src=static/images/home.png style='max-width: 20px; max-height: 20px;'>  " +
                            bus['location']['display_address'][0] + ", " + bus['location']['display_address'][1] + "</h5>"
                            "<h5><img src=static/images/phone.png style='max-width: 20px; max-height: 20px;'> " + bus['display_phone'] + "</h5>"
                            "<h5><img src=static/images/cash-other.png style='max-width: 20px; max-height: 20px;'> " + str(bus['price']) + "</h5>"
                            "<h5><img src=static/images/rating.png style='max-width: 20px; max-height: 20px;'> " + str(bus['rating']) + "</h5>")
            }
        if bus['is_closed'] == True:
            temp = {
                'lat': bus['coordinates']['latitude'],
                'lng': bus['coordinates']['longitude'],
                'infobox': ("<h3><a href=" + bus['url'] + " target=_blank>" + bus['name'] + "</a></h3>"
                            "<h5 style='color: red'>Closed Now</h5>"
                            "<h5><img src=static/images/home.png style='max-width: 20px; max-height: 20px;'>  " +
                            bus['location']['display_address'][0] + ", " + bus['location']['display_address'][1] + "</h5>"
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
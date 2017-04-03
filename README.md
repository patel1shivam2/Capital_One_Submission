# Capital One Submission - Shivam Patel - University of Texas at Austin

[Link to Web Application](http://shivamcapitalone.herokuapp.com/)

This web application serves to enhance user experience in searching and finding a restaurant or specific experience using the YELP API.
The web application has an intuitive user interface that allows users to enter their search criteria 
and perform a simple yet powerful search. In the response, the web application displays a Google Map display of the users request along with
a scrolling assortment of the different restuarants or experiences they searched for. 

Most of the leg work is thoroughly done through the Flask microframework. The form data collection, API request, and Google Map initialization
are performed through this framework. I decided to perform most of these executions through Flask because the amount of data
involved in this API request was not monumental. On the front-end, Jinja2 Templating through the Flask framework simplified  data transfer. I was able to loop through the data provided through the API on the front end and render the scrolling display of
locations on the right side of the display.

## Deployment

I deployed this web application through Heroku through their CLI

## Built With

* [Flask](http://flask.pocoo.org/) - The backend web framework
* [YELP API 3.0](https://maven.apache.org/) - Data Acquisition
* [Bootstrap](http://getbootstrap.com/) - Front-end Simplification
* [Heroku](https://dashboard.heroku.com/) - Web Application Hosting


## Author

* **Shivam Patel** - *Computer Science Major at the University of Texas at Austin*

## Acknowledgments

* If there are any issues with the code or you want to contact me about this project, I can be reached at shivampatel@utexas.edu

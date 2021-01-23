# Netflix Data analytics <a href="https://emoji.gg/emoji/3266_Netflix"><img src="https://emoji.gg/assets/emoji/3266_Netflix.png" width="35px" height="35px" alt="Netflix"></a>

### Live Web-App available [here.](https://netflix-webapp.herokuapp.com/)

## Data source:
You can get the dataset [here.](https://www.kaggle.com/shivamb/netflix-shows)

## Installation:
Simply run ***pip install -r requirements.txt*** to install the necessary dependencies.

## Usage:
1. Navigate to the directory where you have cloned this entire branch contents.
2. Run the command: ***python app.py*** and your webapp will load in your default browser.

## Final Plotly Webapp would look like this in your favourite web-browser :wink: : 
<kbd>
<img src="https://user-images.githubusercontent.com/29462447/105572675-a460c580-5d7e-11eb-927d-7416ef820171.gif" data-canonical-src="https://user-images.githubusercontent.com/29462447/105572675-a460c580-5d7e-11eb-927d-7416ef820171.gif"/> 
</kbd>

## Running the Dockerized App
1. Ensure you have Docker Installed and Setup in your OS (Windows/Mac/Linux). For detailed Instructions, please refer [this.](https://docs.docker.com/engine/install/)
2. Navigate to the folder where you have cloned this repository ( where the ***Dockerfile*** is present ).
4. Edit ***app.py*** by changing line 304 from **app.run_server(debug=True)** to **app.run_server(host='0.0.0.0',debug=True)**.
5. Build the Docker Image (don't forget the dot!! :smile: ): 
```
docker build --tag netflix_app .
```
4. Run the docker:
```
docker run --publish 8000:8080 --detach --name app netflix_app
```

This will launch the dockerized app. Navigate to ***localhost:8000*** in your browser to have a look at your web application. You can check the status of your all available running dockers by:
```
docker ps
```


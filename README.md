# How to run the script

Do the following steps to get the project running:

* Clone the repo
* Create a virtual environment (`python3 -m venv /path/to/new/virtual/environment`)
* Install the dependencies with `pip` (`pip install -r requirements.txt`)
* Edit the following variables in `run.py`
    * `TEXT_FILE_PATH` - Path to the text file containing image URLs.
    * `DOWNLOAD_DIRECTORY` - Path to download the images
* Add image URLs to the text file ( Or edit the `sample.txt` in the project root)
* Add the project root to the `PYTHONPATH` env
* Run `python3 run.py`
* Run test cases with `pytest test/ -vvv`


# Future Improvements

* Update the code to read the text_file_path, download_path as command line args, that way we can pass them in the jenkins job

* `TEXT_FILE_PATH` could be URL and we can download the text file instead of reading from server. Making it easier to update the text file.

* Extend the `BaseDownloader` class to download other file formats like PDF ...

* The Images are verified by their formats. More formats can be added to `ImageDownloader` class.
  Currently supported formats are `'bmp', 'gif', 'jpeg', 'jpg', 'svg', 'tiff', 'ico', 'rgb', 'png', 'webp'`
 
* If the code can't figure out the file name from 'content-disposition' header. A random string is used as the file name

# Deployment options

## Running downloader script periodically

There are various ways to run the script periodically in servers.

1. Cron job
2. Jenkins / Airflow

#### Cron Job
Use the OS cron to run the script periodically.

`*/5 * * * * python3 /usr/home/run.py`

Make an entry in the crontab to get this working.


#### Jenkins / Airflow

We can use jenkins/Airflow to achieve the same result as cron job.
Jenkins machine would need access to server(Or - Run jenkins on the same server).
Jenkins / Airflow can be configured to report the status of the jobs via email | chat apps, making it easier to keep track of the jobs. 
I would prefer this over basic cron job.



We can modify the script to download the text file from a URL rather than reading from the server itself. Making it easier to update the text file.


# Serving Images from server

#### Using python a server

We can create a flask app to serve the images out of server.

```
# Sample code

from flask import Flask  

app = Flask(__name__, static_url_path='/data/images')

@app.route("/images/<image_file>")
def serve_images(image_file):
    return app.send_static_file(image_file)

if __name__ == "__main__":  
    app.run()
```

* In a production environment, We have to use an App server like `Gunicorn / uwsgi` to run the flask app.
This will involve additional settings.
* To make sure that the server is always up and running we need to use a process management system like `supervisor`


#### Using a web server to host the images
We can use a web server like `Nginx` to host our images(static content) directly from server.
This would require less set up than the python server.

By editing the server conf file we can direct Nginx to server images from a image folder

```
# sample configuration

location /images/ {
            root /data/images;
        }
```

This would allow us to visit the URL : `https://******/images/test.png`
to get the image.
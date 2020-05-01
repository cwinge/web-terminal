# web-terminal
Small demo project that can be deployed on most linux machines.
Deploys any docker container to be accessible via the web, easily done via any cloud provider (such as AWS, Azure, GCS). 
Made with Python, Flask, GoTTY and Docker.

The install.sh can be used as the start script for the deployed VM, or be ran manually when SSH'ed into it. 

To run the web app, use the following commands
``tmux``

``python3 main.py <insert external ip>``

The web app can now be accessed via external_ip:8080 in the browser.

Starting a Docker Python container in the web app would look like this:

![main](https://raw.githubusercontent.com/cwinge/web-terminal/master/preview_1.PNG)

![python](https://raw.githubusercontent.com/cwinge/web-terminal/master/preview_python.PNG)

![pythonterminal](https://github.com/cwinge/web-terminal/blob/master/preview_python2.PNG?raw=true)

As this is just a simple demo, it is not well tested and not secure. Flask should not be used for production. 
With some trivial changes and additions, this could be improved substantionally.
Using another languange than Python and other deployment service than Flask would be benifital, as some things got quite ugly and less dynamic due to it not being well suited for external access. 

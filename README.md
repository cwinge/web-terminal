# web-terminal
Small demo project that can be deployed on most linux machines.
Deploys any docker container to be accessible via the web, easily done via any cloud provider (such as AWS, Azure, GCS). 
Made with Python, Flask, GoTTY and Docker.

The install.sh can be used as the start script for the deployed VM, or be ran manually when SSH'ed into it. 

To run the web app, use the following commands

``tmux``

``python3 main.py <insert external ip>``

The web app can now be accessed via external_ip:8080 in the browser.

Name of the containers should follow one of the following formats (same as used in a regular ``docker pull`` command):

``cname`` or ``cname:version`` or ``cname/cname2`` or ``cname/cname:version``


Starting the custom container in the web app would look like this:

![gif](https://raw.githubusercontent.com/cwinge/web-terminal/master/preview.gif)

As this is just a simple demo, it is not well tested and not secure. Flask should not be used for production. 
With some trivial changes and additions, this could be improved substantionally.
Using some other languange than Python and other deployment service than Flask would be benifitial, as some things got quite ugly and less dynamic due to it not being well suited for external access. 

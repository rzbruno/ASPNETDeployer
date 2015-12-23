# ASPNET Deployer
Raw Deployment Tool for ASP.Net Web Applications

# Disclaimer
Firstly, the tool is obviously under development. 
Second, keep in mind that this is a tool for learning purposes and that it may not be generic enough for you.
But feel free to customize it and use if you want.

# Summary
This is an agent-based deployer for asp.net web applications. 
The major goal is to send application data, create the pool and register the application in the IIS server. 

# Architecture
-client: CLI to manage the deploy.
-master: to hold and centralize the information of the nodes and some configs.
-node: the windows server node with IIS.

# Installing and Running
For the master and nodes are python web application powered by bottlepy.org.
So, you need python (I've tested with python 3.4) and bottle:

pip install -r requirements.txt or pip install bottle

For deploy you can follow: http://bottlepy.org/docs/dev/tutorial.html#deployment

The client just need python and the requests installed: pip install requests

# Internal-Communication
-json structured request and responses
# Python Budget Manager

The Python Budget Manager is a Pythom implementation of the [PHP Budget Manager](https://github.com/hopesimon/Budget-Manager) project. It utilizes Python, Flask, and Bootstrap as core components. It was deployed to IBM Cloud and also includes necessary files for the task, such as the `manifest.yml` file.

## Running the application

To run the application, find the directory your application is downloaded in. Once inside of the project directory, run the command:

```bash
python3 app.py
```

## Uploading the application to IBM Cloud

* Create an account on the [IBM Cloud (Bluemix)](https://console.bluemix.net/) website.
* If you use Bluemix, you will be prompted to also create an IBM Cloud account. Proceed with the registration.
* Once logged in, select `Create Resource` > `Python`
* Enter an application name and host name. Select the domain and region. Leave the rest as default.
* Select the 256mb pricing plan (don't worry, it's free).
* Download the git repository. Modify the `manifest.yml` file to be the following:
```yaml
---
applications:
- name: <your application name>
  memory: 128MB
  disk_quota: 256MB
  buildpack: python_buildpack
  command: python app.py
  domain: <your domain>
  host: <your host name>
```
* Download [the CLI](https://console.bluemix.net/docs/cli/index.html#overview).
* Change the directory to the location where the git repository was downloaded.
* Run:
```bash
bluemix api https://api.ng.bluemix.net
```
* Run:
```bash
bluemix login
```
* Enter your username and password.
* Run:
```bash
bluemix app push python-budget
```

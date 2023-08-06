# GitVars
Use the Gitlab API to extract CI/CD variables and output them in a format useable for running projects locally.

### Installation
`pip install mf-gitvars --upgrade`

### Setup
Create an API key on Gitlab [here](https://gitlab.com/-/profile/personal_access_tokens) and grant it `read_api, read_repository` permissions

Create a local configuration file and replace your token
`cat ~/.python-gitlab.cfg`

```ini
[global]
default = momentfeed
ssl_verify = true
timeout = 5
api_version = 4

[momentfeed]
url = https://gitlab.com
private_token = [YOUR API TOKEN]
```

### Usage
Find the gitlab project id on the project page here:

![Gitlab Project Id](images/projectid.png)

And then run with 
```bash
$ mf-gitvars [project-id]
```

You will get an output for each environment and one for the global environment.

![CLI Output](images/output.png)

There is a special string for `IntelliJ` and you can paste that directly into your run configuration like so:

![IntelliJ Run/Debug Config](images/intellij.png)

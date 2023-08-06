# __main__.py

from configparser import ConfigParser
from importlib import resources  # Python 3.7+
import sys

from gitvars import readvars
from gitvars import printvars

def main():
    """Import the gitlab variables"""
    # Import Gitlab CI/CD variables from your project
    cfg = ConfigParser()
    cfg.read_string(resources.read_text("gitvars", "config.txt"))
    gitlab_project = cfg.get("project", "gitlab_project")
    var_prefix = cfg.get("project", "var_prefix")
    exclude_keys_str = cfg.get("project", "exclude_keys")
    exclude_keys = []
    if(exclude_keys_str):
        exclude_keys = exclude_keys_str.split(",")

    # If an article ID is given, show the article
    if len(sys.argv) > 1:
        cicd_vars = readvars._read(sys.argv[1], gitlab_project, var_prefix, exclude_keys)
        printvars._prettyprint(cicd_vars)

    # If no ID is given, show a list of all articles
    else:
        print("Project ID is required")

if __name__ == "__main__":
    main()

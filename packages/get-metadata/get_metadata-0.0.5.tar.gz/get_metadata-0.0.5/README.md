# get_metadata
Get metadata string. Works on GAE(Google App Engine), GCF(Google Cloud Functions), and the others.
For the detail, see https://cloud.google.com/appengine/docs/standard/java/accessing-instance-metadata


## Installation;
~~~console
pip install get_metadata
~~~

## OR Write `get_metadata` in requirements.txt.

~~~
# requirements.txt sample
Flask  # sample
get_metadata
google-cloud-storage  # sample
~~~


## How to use
~~~python
from get_metadata import get_metadata

key = "project_id"
project_id = get_metadata(key)

key2 = "/computeMetadata/v1/instance/service-accounts/default/"
service_accounts = get_metadata(key2)
~~~

key accepts a key of key_list(see below) or metadata endpoint.

~~~python
key_list: dict[str, str] = {
    # The project number assigned to your project.
    "numeric_project_id": "/computeMetadata/v1/project/numeric-project-id",
    # The project ID assigned to your project.
    "project_id": "/computeMetadata/v1/project/project-id",
    # The zone the instance is running in.
    "zone": "/computeMetadata/v1/instance/zone",
    # no description
    "aliases": "/computeMetadata/v1/instance/service-accounts/default/aliases",
    # The default service account email assigned to your project.
    "email": "/computeMetadata/v1/instance/service-accounts/default/email",
    # Lists all the default service accounts for your project.
    "service-accounts": "/computeMetadata/v1/instance/service-accounts/default/",
    # Lists all the supported scopes for the default service accounts.
    "scopes": "/computeMetadata/v1/instance/service-accounts/default/scopes",
    # Returns the auth token that can be used to authenticate your application to other Google Cloud APIs.
    "token": "/computeMetadata/v1/instance/service-accounts/default/token",
}
~~~
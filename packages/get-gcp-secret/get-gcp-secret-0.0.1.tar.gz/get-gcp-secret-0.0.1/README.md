# get-gcp-secret
Get value from google Cloud Secret Manager.


## Installation;
~~~console
pip install get-gcp-secret google-cloud-secret-manager
pip install get_metadata  # optional
~~~

## OR Write `get-gcp-secret` on requirements.txt

~~~
# requirements.txt sample
get-gcp-secret
google-cloud-secret-manager  # required
get_metadata  # optional
~~~


## How to use
~~~python
import get-gcp-secret

# GCP Project ID will be automatically detected("get_metadata" required).
# OR set GCP project ID manually.
get-gcp-secret.set_project_id("Project ID string")

# get secret text
secret_name = "secret name string"
secret_ver = 2 # or "2"
secret_text = get-gcp-secret.get_secret_text(secret_name, secret_ver)
# when secret_ver is omitted, 'latest' will be used.
# secret_text = get-gcp-secret.get_secret_text(secret_name)

# get secret text(secret name/version from env)
env_secret_name = "secret name env name"
env_secret_ver = "secret ver env name"
secret_text = get-gcp-secret.get_secret_text_from_env(env_secret_name, env_secret_ver)

# when secret_ver is omitted, 'latest' will be used.
# secret_text = get-gcp-secret.get_secret_text_from_env(env_secret_name)
~~~

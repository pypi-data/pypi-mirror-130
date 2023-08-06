This is a helper module to allow you to capture all the request/response which comes to your Flask app.

### How to use
```python
from flask_cdc import cdc

# We expect you already have the flask app 
app = "Existing flask" 

# Recorder is called everytim you get request response. You can do anything you want
# In this example we have logged data with a helper function provided by cdc. You can change
# this method to do anything else
def recorder(state):
    cdc.log_results(state)

# Wrap app to your session record MW    
app.wsgi_app = cdc.SessionRecorderMiddleware(app.wsgi_app, recorder)

```
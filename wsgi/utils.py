from functools import update_wrapper
from flask import make_response
import json

def nocache(func):
    """Stop caching for pages wrapped in nocache decorator."""
    def new_func(*args, **kwargs):
        ''' No cache Wrapper '''
        resp = make_response(func(*args, **kwargs))
        resp.cache_control.no_cache = True
        return resp
    return update_wrapper(new_func, func)

def check_qs(qs, required):
	valid = True
	for arg in required:
	    if arg not in qs:
	        valid = False

	return valid


def check_browser_platform(user_agent):
    browser = "Unknown" if not user_agent.browser else user_agent.browser
    platform = "Unknown" if not user_agent.platform else user_agent.platform

    return browser, platform

def check_valid_json(json_input):
    # Check JSON valid
    try:
        json.loads(json.dumps(json_input))
        valid = True
    except ValueError:
        valid = False

    return valid

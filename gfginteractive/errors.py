#----------------------------------------------
# ExperimentError Exception, for db errors, etc.
#----------------------------------------------
# Possible ExperimentError values.

from flask import render_template

class ExperimentError(Exception):
    """
    Error class for experimental errors, such as subject not being found in
    the database.
    """
    def __init__(self, value, **kwargs):
        experiment_errors = dict(
            already_started_exp = 1001,
            already_did_exp = 1002, 
            tried_to_quit=1003,
            improper_inputs = 1004,
            browser_type_not_allowed = 1005,
            error_setting_worker_complete = 1006,
            hit_not_registered_with_ad_server = 1018,
            unknown_error = 9999,
        )
        self.value = value
        self.errornum = experiment_errors[self.value]
        self.kwargs = kwargs

    def __str__(self):
        return repr(self.value)
        
    def error_page(self, request, contact_on_error):
        return render_template("error.html",
                               errornum = self.errornum,
                               contact_address = contact_on_error, 
                               **self.kwargs)
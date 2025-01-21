from flask import Flask, render_template
import traceback
import sys

def configure_error_handlers(app):
    @app.errorhandler(500)
    def internal_error(error):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error_details = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        
        with open('error.log', 'a') as f:
            f.write(f"500 Error:\n{error_details}\n\n")
        
        return render_template('500.html'), 500

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

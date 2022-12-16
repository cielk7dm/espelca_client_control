from flask import (render_template)
import socket

def page_not_found(e):
    hostname = socket.gethostname()
    return render_template('404.html', hostname=hostname), 404
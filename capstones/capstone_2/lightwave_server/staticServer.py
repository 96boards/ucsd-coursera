#staticServer.py
import os.path

def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__)) + "/client"
    
def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)

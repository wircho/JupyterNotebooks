from IPython.display import display, HTML
import ipywidgets as widgets
from traitlets import Unicode, validate

class KeyWidget(widgets.DOMWidget):
    _view_name = Unicode('KeyView').tag(sync=True)
    _view_module = Unicode('keyview').tag(sync=True)
    current_key = Unicode('nothing').tag(sync=True)

display(HTML("<script src=\"tag_images_social_widget.js\"></script>"))
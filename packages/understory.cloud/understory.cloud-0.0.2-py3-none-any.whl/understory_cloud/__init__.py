"""
Use the understory.

"""

from understory import web
from understory.web import tx

app = web.application("understory.cloud", static=__name__)
templates = web.templates(__name__)


@app.route(r"")
class Main:
    def get(self):
        return templates.index()

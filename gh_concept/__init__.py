import os
from flask import Flask
import ghhops_server as hs
app = Flask(__name__)
hops: hs.HopsFlask = hs.Hops(app)
os.environ["no_proxy"] = "127.0.0.1, localhost"

# import general view routing
import gh_concept.views
# import gh components
import gh_concept.components.add_slab_area
import gh_concept.components.add_column
import gh_concept.components.add_wall



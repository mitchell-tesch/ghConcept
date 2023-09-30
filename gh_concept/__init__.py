import os
from flask import Flask
import ghhops_server as hs
app = Flask(__name__)
hops: hs.HopsFlask = hs.Hops(app)
os.environ["no_proxy"] = "127.0.0.1, localhost"

# import general view routing
import gh_concept.views

# import ghConcept add structure components
import gh_concept.components.add_beam
import gh_concept.components.add_slab
import gh_concept.components.add_column
import gh_concept.components.add_wall
import gh_concept.components.add_opening

# import ghConcept add support components
import gh_concept.components.add_point_support
import gh_concept.components.add_line_support

# import ghConcept add spring components
import gh_concept.components.add_point_spring
import gh_concept.components.add_line_spring
import gh_concept.components.add_area_spring

# import ghConcept add loading components
import gh_concept.components.add_loading_layer
import gh_concept.components.add_point_load
import gh_concept.components.add_line_load
import gh_concept.components.add_area_load

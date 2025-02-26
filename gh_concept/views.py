from gh_concept import app


@app.route("/about")
def about():
    return "ghConcept - because every RAM needs a Grasshopper"

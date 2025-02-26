from gh_concept import hs, hops
from gh_concept.concept import model as concept_model, add_loading as concept_add_load


@hops.component(
    "/add_loading_layer",
    name="Concept Add Loading Layer",
    nickname="add loading layer",
    description="Adds a loading layer of specified type to the specified RAM Concept model.",
    icon="images/add_slab_area.png",
    inputs=[
        hs.HopsBoolean(
            "Enable push?",
            "Push?",
            "Push to RAM Concept model",
            hs.HopsParamAccess.ITEM,
            default=False,
        ),
        hs.HopsString(
            "Concept model",
            "Model",
            "File path of RAM Concept model",
            hs.HopsParamAccess.ITEM,
        ),
        hs.HopsString(
            "Layer name",
            "Name",
            "Name of loading layer as list",
            hs.HopsParamAccess.LIST,
        ),
        hs.HopsString(
            "Layer type",
            "Type",
            "Layer type as list\n\
                      (force, shrink, temp, combo)",
            hs.HopsParamAccess.LIST,
        ),
    ],
    outputs=[
        hs.HopsString("Push log", "Log", "Log of Concept push"),
    ],
)
def add_loading_layer(
    push: bool, model_file: str, layer_name: list[str], layer_type: list[str]
):
    if push:
        logger = []
        # verify valid areas and translate to Concept Polygons
        valid_loading_layers = []
        for i, name in enumerate(layer_name):
            if layer_type[i].lower not in ["force", "shrink", "temp", "combo"]:
                logger.append(f"Polyline/Line at index {i} is invalid.")
                continue
            # store valid
            valid_loading_layers.append(
                {
                    "layer_name": name,
                    "layer_type": layer_type[i],
                }
            )
        if valid_loading_layers:
            # open Concept model and extract set api units and signs
            concept, model = concept_model.open_concept_model(model_file)
            file_units, file_signs = concept_model.set_api_units_signs(model)
            # add loading layers
            for layer in valid_loading_layers:
                concept_add_load.add_loading_layer(model, **layer)
            # restore user units and save and close Concept
            concept_model.restore_file_units_signs(model, file_units, file_signs)
            concept_model.save_close_concept(concept, model, model_file)
            logger.append(f"{len(valid_loading_layers)} loading layers pushed.")
        else:
            logger.append("No valid loading layers provided.")
        return logger

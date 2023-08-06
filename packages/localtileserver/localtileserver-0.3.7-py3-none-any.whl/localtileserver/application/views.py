import logging

from flask import render_template, request
from flask.views import View

from localtileserver import utilities
from localtileserver.application import app
from localtileserver.examples import get_data_path

logger = logging.getLogger(__name__)


class GeoJSViewer(View):
    def dispatch_request(self):
        return render_template("geojsViewer.html")


class CesiumViewer(View):
    def dispatch_request(self):
        return render_template("cesiumViewer.html")


@app.context_processor
def inject_context():
    try:
        # First look for filename in URL params
        f = request.args.get("filename")
        if not f:
            raise KeyError
        filename = utilities.get_clean_filename(f)
    except KeyError:
        # Backup to app.config
        try:
            filename = utilities.get_clean_filename(app.config["filename"])
        except KeyError:
            # Fallback to sample data
            logger.error("No filename set in app config or URL params. Using sample data.")
            filename = get_data_path("landsat.tif")
    tile_source = utilities.get_tile_source(filename)
    context = utilities.get_meta_data(tile_source)
    context["bounds"] = utilities.get_tile_bounds(tile_source, projection="EPSG:4326")
    context["filename"] = filename
    return context

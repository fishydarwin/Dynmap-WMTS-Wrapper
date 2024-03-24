import json
from math import floor
from xml.dom.minidom import parseString
from dict2xml import dict2xml
from requests import get
from dwmtsw.util.config_parser import DWMTSWConfigParser

class DynmapConfiguration:

    @staticmethod
    def get_capabilities(url: str) -> str:
        config = DWMTSWConfigParser.get_config()

        request = get(f"{url}/up/configuration")
        result = json.loads(request.content)

        xml_result = {}

        available = config["worlds"]["available"].split(',')
        for world in result["worlds"]:
            if world["name"] not in available:
                continue

            world_width = str(floor(float(config["worlds"][world["name"] + "_width"])))
            world_height = str(floor(float(config["worlds"][world["name"] + "_height"])))

            matrix_set = {}
            matrix_set["ows:Title"] = world["name"] + " view"
            matrix_set["ows:Identifier"] = world["name"]
            matrix_set["ows:BoundingBox"] = {
                "ows:LowerCorner" : "0.0 0.0",
                "ows:UpperCorner" : world_width + " " + world_height
            }

            zoom_levels = int(world["maps"][0]["scale"])
            print(zoom_levels)

            tile_matrices = []
            for i in range(zoom_levels + 1):
                tile_matrix = {}
                tile_matrix["ows:Identifier"] = zoom_levels - i
                tile_matrix["TopLeftCorner"] = "0.0 0.0"
                tile_matrix["TileWidth"] = 128
                tile_matrix["TileHeight"] = 128

                matrix_width = floor(int(config["worlds"][world["name"] + "_width"]) // 16 / (i + 1))
                matrix_height = floor(int(config["worlds"][world["name"] + "_width"]) // 16 / (i + 1))
                tile_matrix["MatrixWidth"] = matrix_width
                tile_matrix["MatrixHeight"] = matrix_height

                tile_matrices.append(tile_matrix)

            matrix_set["TileMatrix"] = tile_matrices

            xml_result["TileMatrixSet"] = matrix_set

        xml = dict2xml(xml_result)
        return xml

import json
from dict2xml import dict2xml
from requests import get
from dwmtsw.util.config_parser import DWMTSWConfigParser

class DynmapConfiguration:

    # Experimentally-found Voodoo Magic Constant. Enjoy.
    EXACT_BLOCK_SCALING_FACTOR = 892.958114397

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

            layers = {}
            layer_content = {}
            
            layer_content["ows:Title"] = world["name"]
            layer_content["ows:Abstract"] = world["name"] + " View"
            layer_content["ows:WGS84BoundingBox"] = {
                "ows:LowerCorner" : "-180 -90",
                "ows:UpperCorner" : "180 90"
            }
            layer_content["ows:Identifier"] = world["name"]
            layer_content["Style"] = {
                "ows:Identifier" : "default"
            }
            layer_content["Format"] = "image/jpg"
            layer_content["TileMatrixSetLink"] = {
                "TileMatrixSet" : world["name"]
            }

            matrix_set = {}
            matrix_set["ows:Title"] = world["name"] + " view"
            matrix_set["ows:Identifier"] = world["name"]
            matrix_set["ows:SupportedCRS"] = "EPSG:3857"

            zoom_levels = int(world["maps"][0]["scale"])
            DWMTSWConfigParser.log(zoom_levels)

            center_x = - int(config['worlds'][world["name"] + "_width"]) // 2
            center_z = - int(config['worlds'][world["name"] + "_height"]) // 2 - 32
            center_z = -center_z

            tile_matrices = []
            for i in range(zoom_levels + 1):
                tile_matrix = {}
                tile_matrix["ows:Identifier"] = zoom_levels - i
                tile_matrix["ScaleDenominator"] = DynmapConfiguration.EXACT_BLOCK_SCALING_FACTOR * 2 ** (zoom_levels - i)
                tile_matrix["TopLeftCorner"] = str(center_x) + " " + str(center_z)
                tile_matrix["TileWidth"] = 128
                tile_matrix["TileHeight"] = 128

                matrix_width = int(config['worlds'][world["name"] + "_tiles_width"]) // (2 ** (zoom_levels - i))
                matrix_height = int(config['worlds'][world["name"] + "_tiles_height"]) // (2 ** (zoom_levels - i))
                tile_matrix["MatrixWidth"] = matrix_width
                tile_matrix["MatrixHeight"] = matrix_height

                tile_matrices.append(tile_matrix)

            matrix_set["TileMatrix"] = tile_matrices
            xml_result["TileMatrixSet__"] = matrix_set

            xml_result["Layer"] = layer_content

        xml = dict2xml(xml_result)
        xml = xml.replace("<TileMatrixSet__>", "<TileMatrixSet xml:id=\"world\">")
        xml = xml.replace("</TileMatrixSet__>", "</TileMatrixSet>")

        template_file = open("dwmtsw/entity/data/capabilities_format.xml").read()
        template_file = template_file.replace("__$generated__", xml)
        return template_file

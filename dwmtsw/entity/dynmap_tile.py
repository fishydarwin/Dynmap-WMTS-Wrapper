import requests
from dwmtsw.util.config_parser import DWMTSWConfigParser

class DynmapTile:

    def __init__(self, url: str, world: str, zoom: int = 0, x: int = 0, y: int = 0) -> None:
        self.__url = url;
        self.__world = world;
        self.__zoom = zoom;
        self.__x = x;
        self.__y = y;
    
    def get_tile(self) -> str:

        config = DWMTSWConfigParser.get_config()

        matrix_width = int(config['worlds'][self.__world + "_tiles_width"]) // (2 ** self.__zoom)
        matrix_height = int(config['worlds'][self.__world + "_tiles_height"]) // (2 ** self.__zoom)

        zoom_ratio = 2 ** self.__zoom

        x = int(self.__x - matrix_width // 2) * zoom_ratio
        y = int(self.__y - matrix_height // 2) * zoom_ratio

        zoom_string = ("z" * self.__zoom) + "_"
        if self.__zoom == 0:
            zoom_string = ""
        
        query = f"{ self.__url }/tiles/{self.__world}/flat/0_0/{ zoom_string }{x}_{-y}.jpg"
        DWMTSWConfigParser.log(f"Fetching {query}")
        return requests.get(query).content

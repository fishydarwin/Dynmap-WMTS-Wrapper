import requests
from dwmtsw.entity.dynmap_configuration import DynmapConfiguration
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

        world_width = int(config["worlds"][self.__world + "_width"])
        world_height = int(config["worlds"][self.__world + "_height"])

        x = int(self.__x * 16 - world_width // 2)
        y = - int(self.__y * 16 -  world_height // 2)

        zoom_string = ("z" * self.__zoom) + "_"
        if self.__zoom == 0:
            zoom_string = ""
        
        query = f"{ self.__url }/tiles/{self.__world}/flat/0_0/{ zoom_string }{x}_{y}.jpg"
        print(query)
        return requests.get(query).content

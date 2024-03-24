from configparser import ConfigParser

class DWMTSWConfigParser:

    config: ConfigParser
    
    @staticmethod
    def init(cfg_file: str) -> None:
        DWMTSWConfigParser.config = ConfigParser()
        DWMTSWConfigParser.config.read(cfg_file)

    @staticmethod
    def get_config() -> ConfigParser:
        return DWMTSWConfigParser.config


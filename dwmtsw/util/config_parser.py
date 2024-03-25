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
    
    @staticmethod
    def should_log() -> bool:
        return DWMTSWConfigParser.config['settings']['verbose_logs'] == 'True'

    @staticmethod
    def log(message: str) -> None:
        if DWMTSWConfigParser.should_log():
            print(message)

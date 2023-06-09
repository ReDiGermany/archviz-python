from dotenv import load_dotenv
load_dotenv()
import os

class Config:
    _IMAGE_WIDTH:int = 0
    _IMAGE_HEIGHT:int = 0
    _SERVER_PORT:int = 0
    _SAVE_TEMP:bool = True
    _SAVE_STATIC:bool = True
    _VERTICAL_ROOMZ_COUNT:int = 0
    _HORIZOHNTAHL_ROOMZ_COUNT:int = 0
    _WALL_WIDTH:int = 0
    def __init__(self) -> None:
        self._IMAGE_WIDTH = int(os.environ.get("IMAGE_WIDTH")),
        self._IMAGE_HEIGHT = int(os.environ.get("IMAGE_HEIGHT")),
        self._SERVER_PORT = int(os.environ.get("SERVER_PORT")),
        self._SAVE_TEMP = os.environ.get("SAVE_TEMP").lower()=="true",
        self._SAVE_STATIC = os.environ.get("SAVE_STATIC").lower()=="true",
        self._VERTICAL_ROOMZ_COUNT = int(os.environ.get("VERTICAL_ROOMZ_COUNT")),
        self._HORIZOHNTAHL_ROOMZ_COUNT = int(os.environ.get("HORIZOHNTAHL_ROOMZ_COUNT")),
        self._WALL_WIDTH = int(os.environ.get("WALL_WIDTH")),

        self._DB_HOST = os.environ.get("DB_HOST") # =api.lisha-app.com
        self._DB_PORT = int(os.environ.get("DB_PORT")) # =27017
        self._DB_DATABASE = os.environ.get("DB_DATABASE") # =archviz
    

        self._WEB_HOST = os.environ.get("WEB_HOST")
        self._WEB_PORT = int(os.environ.get("WEB_PORT"))
        self._WEB_PROTOCOL = os.environ.get("WEB_PROTOCOL")


    def __str__(self) -> str:
        return f"IMAGE_WIDTH={self._IMAGE_WIDTH[0]} - IMAGE_HEIGHT={self._IMAGE_HEIGHT[0]} - SERVER_PORT={self._SERVER_PORT[0]} - SAVE_TEMP={self._SAVE_TEMP[0]} - SAVE_STATIC={self._SAVE_STATIC[0]} - VERTICAL_ROOMZ_COUNT={self._VERTICAL_ROOMZ_COUNT[0]} - HORIZOHNTAHL_ROOMZ_COUNT={self._HORIZOHNTAHL_ROOMZ_COUNT[0]} DB_HOST={self.DB_HOST} - DB_PORT={self.DB_PORT} - DB_DATABASE={self.DB_DATABASE}"
 
    def getIMAGE_WIDTH(self)->int:
        return self._IMAGE_WIDTH[0]

    def getIMAGE_HEIGHT(self)->int:
        return self._IMAGE_HEIGHT[0]

    def getSERVER_PORT(self)->int:
        return self._SERVER_PORT[0]

    def getSAVE_TEMP(self)->bool:
        return self._SAVE_TEMP[0]

    def getSAVE_STATIC(self)->bool:
        return self._SAVE_STATIC[0]

    def getVERTICAL_ROOMZ_COUNT(self)->int:
        return self._VERTICAL_ROOMZ_COUNT[0]

    def getHORIZOHNTAHL_ROOMZ_COUNT(self)->int:
        return self._HORIZOHNTAHL_ROOMZ_COUNT[0]

    def getWALL_WIDTH(self)->int:
        return self._WALL_WIDTH[0]

    def getDB_HOST(self)->str:
        return self._DB_HOST
    
    def getDB_PORT(self)->int:
        return self._DB_PORT
    
    def getDB_DATABASE(self)->str:
        return self._DB_DATABASE
    
    def getWEB_HOST(self) ->str:
        return self._WEB_HOST
    
    def getWEB_PORT(self) ->int:
        return self._WEB_PORT
    
    def getWEB_PROTOCOL(self) ->str:
        return self._WEB_PROTOCOL


CONFIG = Config()

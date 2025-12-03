
from abc import ABC, abstractmethod
import config.const as const

class Wrapper(ABC):

    @abstractmethod
    def wrap(self, const: str) -> str:
        pass

class AddOn(Wrapper):

    def wrap(self, const: str) -> str:
        return '\"' + const + '\"'
    
    def __init__(self):
        self.gem: bool = False

    def process(self, part: str, dict: dict) -> dict:
        if part == "exam":
            pass
        elif part == "proto":
            pass
        elif part == "series":
            pass
        elif part == "group":
            dict = self._is_manual_kv(dict)
            dict = self._is_gem_kv(dict, part)
            dict = self._is_cardiac_scan(dict)
            dict = self._cal_detector_coverage(dict)
        elif part == "recon":
            dict = self._is_gem_kv(dict, part)
        elif part == "subrecon":
            pass
        else :
            pass
        
        return dict
    
    # If the Kv Mode is 'Manual', then kV range is None 
    def _is_manual_kv(self, dict: dict) -> dict:
        Manual: str = self.wrap(const.MANUAL)
        if dict["kV Mode"] == Manual:
            dict["Min kV"] = self.wrap(const.EMPTY)
            dict["Max kV"] = self.wrap(const.EMPTY)

        return dict
    
    # If the Kv Mode is not 'GEM', then, GEM parameters are None 
    def _is_gem_kv(self, dict: dict, part: str) -> dict:
        if part == "group":
            GEM: str = self.wrap(const.GEM)
            if dict["kV Mode"] == GEM:
                dict["mA Mode"] = self.wrap(const.GEM)
                self.gem = True
            else:
                dict["GEM mA Mode"] = self.wrap(const.EMPTY)
                dict["GEM Profile"] = self.wrap(const.EMPTY)
                self.gem = False
        elif part == "recon":
            if self.gem:
                pass
            else: 
                dict["CID Link"] = self.wrap(const.EMPTY)
                dict["GEM Profile"] = self.wrap(const.EMPTY)
        
        return dict

    # If the Scan type is not 'Cardiac', then the Scan mode is 'N/A'
    def _is_cardiac_scan(self, dict: dict) -> dict:
        
        if "Cardiac" not in dict["Scan Type"]:
             dict["Scan Mode"] = self.wrap(const.NA)
             
        return dict
    
    # Dector Coverage = 5 (If Scan type = Scout)
    # Dector Coverage = MacroRowNumber × 0.625 (Otherwise)
    def _cal_detector_coverage(self, dict: dict) -> dict:
        
        macro_row_num: str = dict["Detector Coverage"].replace('"', '')
        Scout: str = self.wrap(const.SCOUT)
        if len(macro_row_num) > 0:
            if dict["Scan Type"] == Scout:
                dict["Detector Coverage"] = self.wrap(str(5))
            else:
                detector_coverage = int(macro_row_num) * 0.625
                dict["Detector Coverage"] = self.wrap(str(detector_coverage))

        return dict


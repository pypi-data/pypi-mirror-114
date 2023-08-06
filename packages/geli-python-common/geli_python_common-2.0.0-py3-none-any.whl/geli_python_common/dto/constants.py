from enum import Enum, unique, auto

from geli_python_common.util.constants import CaseInsensitiveEnum

SECONDS_PER_HOUR = 3600
SECONDS_PER_QUARTER_HR = 900

class BaseEnum(Enum):

    @classmethod
    def from_value(cls, value) -> Enum:
        for _value, _enum in cls.__members__.items():
            if _value == value.upper() or _value == value.lower():
                return _enum
        raise ValueError(f'{value} is not a valid {cls} name')


@unique
class GHGDataType(BaseEnum):
    ACTUAL = "ACTUAL"
    CURRENT = "CURRENT"
    FORECAST = "FORECAST"
    ALL = "ALL"


@unique
class GridRegion(BaseEnum):
    SGIP_CAISO_SDGE = "sgip_caiso_sdge"
    SGIP_CAISO_PGE = "sgip_caiso_pge"
    SGIP_CAISO_SCE = "sgip_caiso_sce"
    SGIP_LADWP = "sgip_ladwp"
    SGIP_BANC_SMUD = "sgip_banc_smud"
    SGIP_BANC_P2 = "sgip_banc_p2"
    SGIP_IID = "sgip_iid"
    SGIP_PACW = "sgip_pacw"
    SGIP_NVENERGY = "sgip_nvenergy"
    SGIP_TID = "sgip_tid"
    SGIP_WALC = "sgip_walc"


@unique
class PriceUnit(BaseEnum):
    dollars_per_MWh = "$/MWh"
    dollars_per_kWh = "$/kWh"


class MarketExchanges(CaseInsensitiveEnum):
    JEPX = "JEPX"
    NYISO = "NYISO"

    @classmethod
    def get_exchange_timestep(cls, exchange):
        return {MarketExchanges.NYISO: SECONDS_PER_HOUR,
                MarketExchanges.JEPX: SECONDS_PER_QUARTER_HR * 2}.get(exchange)

    @classmethod
    def get_exchange_regions(cls, exchange):
        return {MarketExchanges.NYISO: MarketRegions.NYISO_regions(),
                MarketExchanges.JEPX: MarketRegions.JEPX_regions()}.get(exchange)


class MarketRegions(CaseInsensitiveEnum):

    # JEPX Regions
    NATIONWIDE = "NATIONWIDE"
    HOKKAIDO = "HOKKAIDO"
    TOHOKU = "TOHOKU"
    TOKYO = "TOKYO"
    CHUBU = "CHUBU"
    HOKURIKU = "HOKURIKU"
    KANSAI = "KANSAI"
    CHIBA = "CHIBA"
    SHIKOKU = "SHIKOKU"
    KYUSHU = "KYUSHU"

    # NYISO Regions
    CAPITL = "CAPITL"
    CENTRL = "CENTRL"
    DUNWOD = "DUNWOD"
    GENESE = "GENESE"
    HQ = "HQ"
    HUDVL = "HUDVL"
    LONGIL = "LONGIL"
    MHKVL = "MHKVL"
    MILLWD = "MILLWD"
    NYC = "NYC"
    NORTH = "NORTH"
    NPX = "NPX"
    OH = "OH"
    PJM = "PJM"
    WEST = "WEST"

    @classmethod
    def NYISO_regions(cls):
        return {cls.CAPITL,
                cls.CENTRL,
                cls.DUNWOD,
                cls.GENESE,
                cls.HQ,
                cls.HUDVL,
                cls.LONGIL,
                cls.MHKVL,
                cls.MILLWD,
                cls.NYC,
                cls.NORTH,
                cls.NPX,
                cls.OH,
                cls.PJM,
                cls.WEST}

    @classmethod
    def JEPX_regions(cls):
        return {cls.NATIONWIDE,
                cls.HOKKAIDO,
                cls.TOHOKU,
                cls.TOKYO,
                cls.CHUBU,
                cls.HOKURIKU,
                cls.KANSAI,
                cls.CHIBA,
                cls.SHIKOKU,
                cls.KYUSHU}


class ConnectedSolutionsSeason(CaseInsensitiveEnum):
    SUMMER = auto()
    WINTER = auto()

    @classmethod
    def get_season(cls, month: int):
        """
        Seasons are hard coded based on definitions found in:
        https://www.nationalgridus.com/media/pdfs/bus-ways-to-save/connectedsolutions-ciprogrammaterials.pdf
        """
        if month in [6, 7, 8, 9]:
            return ConnectedSolutionsSeason.SUMMER
        elif month in [12, 1, 2, 3]:
            return ConnectedSolutionsSeason.WINTER
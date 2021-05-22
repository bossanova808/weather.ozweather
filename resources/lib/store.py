class Store:
    """
    Helper class to to provide a centralised store for CONSTANTS and globals
    """

    # Static class variables, referred to by Store.whatever
    # https://docs.python.org/3/faq/programming.html#how-do-i-create-static-class-data-and-static-class-methods

    # CONSTANTS
    WEATHERZONE_URL = 'https://www.weatherzone.com.au'
    WEATHERZONE_SEARCH_URL = WEATHERZONE_URL + "/search/"
    BOM_API_URL = 'https://api.weather.bom.gov.au/v1'
    BOM_API_LOCATIONS_URL = BOM_API_URL + '/locations'

    # 'Globals'

    def __init__(self):
        pass


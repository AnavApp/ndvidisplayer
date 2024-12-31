import ee
import geemap
#import solara
import solara.lab
import datetime as dt

# Declare reactive variables at the top level. Components using these variables
# will be re-executed when their values change.
clicks = solara.reactive([0])
zoom = solara.reactive([5])
center = solara.reactive([40, -100])
word_limit = solara.reactive(10)
valleys = ["Sacramento Valley", "San Joaquin Valley"]
valley = solara.reactive(valleys[0])

class Map(geemap.Map):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_basemap("Esri.WorldImagery")
        self.add_ee_data()
        self.add_layer_manager()
        self.add_inspector()

    def add_ee_data(self):
        # Add Earth Engine dataset
        dem = ee.Image('USGS/SRTMGL1_003')
        landsat7 = ee.Image('LANDSAT/LE7_TOA_5YEAR/1999_2003').select(
            ['B1', 'B2', 'B3', 'B4', 'B5', 'B7']
        )
        states = ee.FeatureCollection("TIGER/2018/States")

        # Set visualization parameters.
        vis_params = {
            'min': 0,
            'max': 4000,
            'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5'],
        }

        # Add Earth Engine layers to Map
        self.addLayer(dem, vis_params, 'SRTM DEM', True, 0.5)
        self.addLayer(
            landsat7,
            {'bands': ['B4', 'B3', 'B2'], 'min': 20, 'max': 200, 'gamma': 2.0},
            'Landsat 7',
            False,
        )
        self.addLayer(states, {}, "US States")

@solara.component
def Page():
    # Calculate word_count within the component to ensure re-execution when reactive variables change.
    solara.SliderInt("Slider", value=word_limit, min=2, max=20)
    
    
    solara.Select(label="Valleys", value=valley, values=valleys)
    solara.Markdown(f"**Selected**: {valley.value}")
    #solara.Text(str(dates.value))
    with solara.Column(style={"min-width": "500"}):
        # solara components support reactive variables
        # solara.SliderInt(label="Zoom level", value=zoom, min=1, max=20)
        # using 3rd party widget library require wiring up the events manually
        # using zoom.value and zoom.set
        Map.element(  # type: ignore
            zoom=zoom.value,
            on_zoom=zoom.set,
            center=center.value,
            on_center=center.set,
            scroll_wheel_zoom=True,
            add_google_map=True,
            height="500px",
        )
        solara.Text(f"Zoom: {zoom.value}")
        solara.Text(f"Center: {center.value}")
    dates = solara.use_reactive(tuple([dt.date.today(), dt.date.today() + dt.timedelta(days=1)]))

    solara.lab.InputDateRange(dates)


# The following line is required only when running the code in a Jupyter notebook:
Page()

import ee
import geemap
import solara


class Map(geemap.Map):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_ee_data()

    def add_ee_data(self):
        years = ["2001", "2004", "2006", "2008", "2011", "2013", "2016", "2019"]

        def getNLCD(year):
            dataset = ee.ImageCollection("USGS/NLCD_RELEASES/2019_REL/NLCD")
            nlcd = dataset.filter(ee.Filter.eq("system:index", year)).first()
            landcover = nlcd.select("landcover")
            return landcover

        collection = ee.ImageCollection(ee.List(years).map(lambda year: getNLCD(year)))
        labels = [f"NLCD {year}" for year in years]
        self.ts_inspector(
            left_ts=collection,
            right_ts=collection,
            left_names=labels,
            right_names=labels,
        )
        self.add_legend(
            title="NLCD Land Cover Type",
            builtin_legend="NLCD",
            height="460px",
            add_header=False,
        )


@solara.component
def Page():
    with solara.Column(style={"min-width": "500px"}):
        Map.element(
            center=[40, -100],
            zoom=4,
            height="800px",
        )


Page()
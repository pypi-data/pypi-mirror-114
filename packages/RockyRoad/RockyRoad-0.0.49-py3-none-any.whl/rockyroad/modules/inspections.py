from .module_imports import *


@headers({"Ocp-Apim-Subscription-Key": key})
class Inspections(Consumer):
    """Inteface to Inspection resource for the RockyRoad API."""

    def __init__(self, Resource, *args, **kw):
        self._base_url = Resource._base_url
        super().__init__(base_url=Resource._base_url, *args, **kw)

    def reports(self):
        return self.__Reports(self)

    @headers({"Ocp-Apim-Subscription-Key": key})
    class __Reports(Consumer):
        """Inteface to Warranty Credit Request resource for the RockyRoad API."""

        def __init__(self, Resource, *args, **kw):
            super().__init__(base_url=Resource._base_url, *args, **kw)

        @returns.json
        @json
        @post("inspections/reports")
        def insert(self, reports: Body):
            """This call will create an inspection report with the specified parameters."""

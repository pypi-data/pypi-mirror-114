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

        @returns.json
        @get("inspections/reports")
        def list(
            self,
            machine_id: Query(type=str) = None,
            account: Query(type=str) = None,
            dealer_account: Query(type=str) = None,
        ):
            """This call will return detailed inspection report information for the specified criteria."""

        @returns.json
        @delete("inspections/reports")
        def delete(self, uid: Query(type=str)):
            """This call will delete the inspection report for the specified uid."""

        @returns.json
        @json
        @patch("inspections/reports")
        def update(self, inspectionReport: Body):
            """This call will update the warranty credit request with the specified parameters."""

        @returns.json
        @multipart
        @post("inspections/uploadfiles")
        def addFile(self, uid: Query(type=str), file: Part):
            """This call will create a warranty credit request with the specified parameters."""

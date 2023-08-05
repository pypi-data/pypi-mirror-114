from .module_imports import *


@headers({"Ocp-Apim-Subscription-Key": key})
class Warranty(Consumer):
    """Inteface to Warranty resource for the RockyRoad API."""

    def __init__(self, Resource, *args, **kw):
        self._base_url = Resource._base_url
        super().__init__(base_url=Resource._base_url, *args, **kw)

    def creditRequest(self):
        return self.__Credit_Request(self)

    @headers({"Ocp-Apim-Subscription-Key": key})
    class __Credit_Request(Consumer):
        """Inteface to Warranty Credit Request resource for the RockyRoad API."""

        def __init__(self, Resource, *args, **kw):
            super().__init__(base_url=Resource._base_url, *args, **kw)

        @returns.json
        @get("warranty/credit-requests")
        def list(
            self,
            uid: Query(type=str) = None,
            claimReference: Query(type=str) = None,
        ):
            """This call will return detailed warranty credit request information for the specified criteria."""

        @returns.json
        @delete("warranty/credit-requests")
        def delete(self, uid: Query(type=str)):
            """This call will delete the maintenance interval for the specified uid."""

        @returns.json
        @json
        @post("warranty/credit-requests")
        def insert(self, creditRequest: Body):
            """This call will create a warranty credit request with the specified parameters."""

        @returns.json
        @json
        @patch("warranty/credit-requests")
        def update(self, creditRequest: Body):
            """This call will update the warranty credit request with the specified parameters."""

        @returns.json
        @multipart
        @post("warranty/credit-requests/add-files")
        def addFile(self, uid: Query(type=str), file: Part):
            """This call will a upload file for a warranty credit request with the specified uid."""
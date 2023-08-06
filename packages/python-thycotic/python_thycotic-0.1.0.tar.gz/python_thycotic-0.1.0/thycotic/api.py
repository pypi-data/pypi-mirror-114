import requests
from urllib.parse import urljoin


from thycotic import Folder


class Api:
    REQUEST_TOKEN_URI = "/SecretServer/oauth2/token"
    API_URI = "/SecretServer/api/v1"

    def __init__(self, username, password, url, verify=True):
        self.username = username
        self.password = password
        self.url = url
        self._session = requests.Session()
        self._session.headers.update({"Content-Type": "application/json"})
        self._session.verify = verify
        self._token = None

    def auth(self):
        TOKEN_URL = urljoin(self.url, self.REQUEST_TOKEN_URI)
        payload = {
            "username": self.username,
            "password": self.password,
            "grant_type": "password",
        }
        self._token = self._internal_call("POST", TOKEN_URL, payload=payload)
        self._session.headers.update(
            {"Authorization": "Bearer {}".format(self._token["access_token"])}
        )

    def search_folders(
        self,
        foldertypeid=None,
        parentfolder=None,
        permissionrequired="View",
        searchtext=None,
        limit=10,
    ):
        """Search, filter, sort, and page secret folders

        The caller is responsible for handling pages and looping to gather all
        of the data

        :param foldertypeid: (optional) Folder type ID
        :param parantfolder: (optional) Parent folder ID
        :param permissionrequired: (optional) Specify whether to filter by Owner, Edit,
            AddSecret, View folder permission. Default is View
        :param searchtext: (optional) Search text
        :param limit: (optional) Maximum number of records to include in results.
            Default is 10
        :returns: PagingOfFolderSummary

        """

        endpoint = "/folders"
        params = {
            "filter.folderTypeId": foldertypeid,
            "filter.parentFolderId": parentfolder,
            "filter.permissionRequired": permissionrequired,
            "filter.searchText": searchtext,
            "take": limit,
        }
        return self._internal_call("GET", self._geturl(endpoint), params=params)

    def _internal_call(self, method, url, params=None, payload=None):
        args = dict(params=params)
        if payload:
            args["data"] = payload
        response = self._session.request(method, url, **args)
        response.raise_for_status()
        return response.json()

    def _geturl(self, endpoint):
        return urljoin(self.url, self.API_URI) + endpoint

    def lookup_folders(
        self,
        foldertypeid=None,
        parentfolder=None,
        permissionrequired="View",
        searchtext=None,
        limit=10,
    ):
        """Search, filter, sort, and page secret folders, returning only folder ID and name

        :param foldertypeid: (optional) Folder type ID
        :param parantfolder: (optional) Parent folder ID
        :param permissionrequired: (optional) Specify whether to filter by Owner, Edit,
            AddSecret, View folder permission. Default is View
        :param searchtext: (optional) Search text
        :param limit: (optional) Maximum number of records to include in results.
            Default is 10
        :returns: PagingOfFolderLookup

        """

        endpoint = "/folders/lookup"
        params = {
            "filter.folderTypeId": foldertypeid,
            "filter.parentFolderId": parentfolder,
            "filter.permissionRequired": permissionrequired,
            "filter.searchText": searchtext,
            "take": limit,
        }
        return self._internal_call("GET", self._geturl(endpoint), params=params)

    def get_folder_stub(self):
        """Return the default values for a new secret folder

        :returns: FolderModel
        """

        endpoint = "/folders/stub"
        return self._internal_call("GET", self._geturl(endpoint))

    def get_folder(self, id, getchildren=False):
        """Get a single folder by ID

        :params id: Folder ID
        :params getchildren: Whether to retrieve all child folders of the requested folder
        :returns: FolderModel
        """

        endpoint = "/folders/{}".format(id)
        params = {"getAllChildren": getchildren}
        return self._internal_call("GET", self._geturl(endpoint), params=params)

    def folder_audit(self, id, limit=10):
        """Retrieve a list of audits for folder by ID

        :params id: Folder ID
        :returns: PagingOfFolderAuditSummary
        """

        endpoint = "/folders/{}/audit".format(id)
        params = {"take": limit}
        return self._internal_call("GET", self._geturl(endpoint), params=params)

    def search_secrets(
        self, folderid=None, includesubfolders=None, heartbeatstatus=None, limit=10
    ):
        """Search, filter, sort, and page secrets

        :params folderid: (optional) Return only secrets within a certain folder
        :params includesubfolders: (optional) Whether to include secrets in subfolders of the
            specified folder
        :param heartbeatstatus: Return only secrets with a certain heartbeat status
        :params limit: (optional) Maximum number of records to include in results
            Default is 10
        :returns: PagingOfSecretSummary
        """

        endpoint = "/secrets"
        params = {
            "filter.folderId": folderid,
            "filter.includeSubFolders": includesubfolders,
            "filter.heartbeatStatus": heartbeatstatus,
            "take": limit,
        }
        return self._internal_call("GET", self._geturl(endpoint), params=params)

    def get_favorite_secrets(self):
        """Returns a list of secrets which the user has favorited

        :returns: WidgetSecretModel
        """

        endpoint = "/secrets/favorite"
        return self._internal_call("GET", self._geturl(endpoint))

    def lookup_secrets(
        self,
        folderid=None,
        heartbeatstatus=None,
        includerestricted=None,
        includesubfolders=None,
        onlysharedwithme=None,
        permissionrequired=None,
        searchtext=None,
        limit=None,
    ):
        """Search, filter, sort, and page secrets, returning only secret ID and name

        :params folderid: (optional) Return only secrets within a certain folder
        :params heartbeatstatus: (optional) Return only secrets with a certain heartbeat status
        :params includerestricted: (optional) Whether to include restricted secrets in results
        :params includesubfolders: (optional) Whether to include secrets in subfolders
            of the specified folder
        :params onlysharedwithme: (optional) When true only Secrets where you are not
            the owner and the Secret was shared explicitly with your user id will be returned
        :params permissionrequired: (optional) Specify whether to filter by List, View,
            Edit, or Owner permission. Default is List. (List = 1, View = 2, Edit = 3, Owner = 4
        :params searchtext: (optional) Search text
        :params limit: (optional) Maximum number of records to include in results
        :returns: PagingOfSecretLookup
        """

        endpoint = "/secrets/lookup"
        params = {
            "filter.folderId": folderid,
            "filter.heartbeatStatus": heartbeatstatus,
            "filter.includeRestricted": includerestricted,
            "filter.includeSubFolders": includesubfolders,
            "filter.onlySharedWithMe": onlysharedwithme,
            "filter.permissionRequired": permissionrequired,
            "filter.searchText": searchtext,
            "take": limit,
        }
        return self._internal_call("GET", self._geturl(endpoint), params=params)

    def lookup_secret_by_id(self, id):
        """Look up secret by ID and return secret name and ID

        :params id: Secret ID
        :returns: SecretLookup
        """

        endpoint = "/secrets/lookup/{}".format(id)
        return self._internal_call("GET", self._geturl(endpoint))

    def get_secret_stub(self, folderid, templateid):
        """Return the default values for a new secret

        :params folderid: Containing folder ID
        :params templateid: Secret template ID
        :returns: SecretModel
        """

        endpoint = "/secrets/stub"
        params = {"secretTemplateId": templateid, "folderId": folderid}
        return self._internal_call("GET", self._geturl(endpoint), params=params)

    def get_secret(self, id):
        """Get a single secret by ID

        :params id: Secret ID
        :returns: SecretModel
        """

        endpoint = "/secrets/{}".format(id)
        return self._internal_call("GET", self._geturl(endpoint))

    def create_folder(self, name, parentfolderid, type=1):
        """Create a new folder

        :params name: Folder name
        :params parentfolderid: Parent folder ID
        :params type: (optional) Folder type ID. Default is 1
        :returns: FolderModel
        """

        endpoint = "/folders"
        data = {
            "folderName": name,
            "folderTypeId": type,
            "parentFolderId": parentfolderid,
        }
        return self._internal_call("POST", self._geturl(endpoint), payload=data)

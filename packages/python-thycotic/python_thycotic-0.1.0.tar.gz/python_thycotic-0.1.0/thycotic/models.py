class Folder:
    """A class representing a thycotic secret folder."""

    def __init__(self, **kwargs):
        self.param_defaults = {
            "folderName": None,
            "folderPath": None,
            "folderTypeId": None,
            "id": None,
            "inheritPermissions": None,
            "inheritSecretPolicy": None,
            "parentFolderId": None,
            "secretPolicyId": None,
        }

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

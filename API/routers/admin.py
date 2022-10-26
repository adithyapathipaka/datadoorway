from typing import Optional, List

from fastapi import APIRouter

from API.metadata.paths import Paths
from API.metadata.tags import Tags
from API.metadata.doc_strings import DocStrings

from core.models.setting_model import SettingModel
from core.settings.settings import Settings
from core.validations.admin_validations import AdminValidations


class Admin:
    def __init__(self, settings: Settings, dependencies: Optional[List]):
        """
        Constructor for publish endpoint
        :param settings: environment settings
        :param dependencies:
        """
        self.settings = settings

        self.router = APIRouter(
            tags=[str(Tags.ADMIN.value)],
            dependencies=dependencies,
        ) if dependencies else APIRouter(tags=[str(Tags.ADMIN.value)])

        self.router.add_api_route(
            path=str(Paths.ADMIN.value),
            endpoint=self.get_settings,
            dependencies=None,
            methods=["GET"],
            responses=DocStrings.ADMIN_GET_ENDPOINT_DOCS
        )

        self.router.add_api_route(
            path=str(Paths.ADMIN.value),
            endpoint=self.update_setting,
            dependencies=None,
            methods=["PUT"],
            responses=DocStrings.ADMIN_PUT_ENDPOINT_DOCS
        )

    async def get_settings(self) -> dict:
        """
        get the settings
        """
        return {"settings": self.settings}

    async def update_setting(self, setting: SettingModel) -> dict:
        """
        update the settings with given key, value. Automatically updates the env file
        """
        admin_validations = AdminValidations(settings=self.settings)
        await admin_validations.validate_setting(key=setting.key)
        self.settings.update_setting(key=setting.key, value=setting.value)
        return {"updated_settings": self.settings}
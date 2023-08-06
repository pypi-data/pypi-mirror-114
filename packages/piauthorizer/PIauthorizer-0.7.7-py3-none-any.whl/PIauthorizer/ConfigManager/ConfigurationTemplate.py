import json
import logging

import requests
from fastapi.exceptions import HTTPException

logger = logging.getLogger("ConfigurationTemplate")


class ConfigurationTemplate:
    """An Application template for a specific Application Conigguration from the STS API"""

    def __init__(self, config_dict: dict, sts_application_url: str) -> None:
        """[summary]

        Args:
            config_dict (dict): [description]
            sts_application_url (str): [description]
        """
        self.sts_application_url = sts_application_url
        self.application = config_dict
        self.config_name = config_dict['name']
        self.tenants = []
        for field in self.application['configurations']:
            if field['tenants']:
                self.tenants = field['tenants']
                break

    def add_tenant(self, tenant_name: str, token: str) -> None:
        """Add a tenant to the Application template.

        Args:
            tenant_name (str): tenant name
        """
        logger.debug(
            f"Adding tenant {tenant_name} to the template {self.config_name}.")
        if tenant_name not in self.tenants:
            self.tenants.append(tenant_name)
            for field in self.application['configurations']:
                if tenant_name not in field['tenants']:
                    field['tenants'].append(tenant_name)

        self.update_template(token)

    def remove_tenant(self, tenant_name: str, token: str) -> None:
        """Remove a tenant from the Application template.

        Args:
            tenant_name (str): tenant name
        """
        if tenant_name in self.tenants:
            self.tenants.remove(tenant_name)
            for field in self.application['configurations']:
                if tenant_name in field['tenants']:
                    field['tenants'].remove(tenant_name)

        self.update_template(token)

    def get_template(self) -> str:
        """Obtain the Application template in a string representation

        Returns:
            str: the application template
        """
        return json.dumps(self.application)

    def set_template(self, template: str) -> None:
        """Set the Application template from a string representation

        Args:
            template (str): string representation of the Application template
        """
        self.application = json.loads(template)

    def update_template(self, token: str) -> None:
        """[summary]

        Args:
            token (str): [description]

        Raises:
            HTTPException: [description]
        """
        logger.debug(
            f"Updating template for the template {self.config_name}.")
        headers = {'Authorization': f'Bearer {token}',
                   'content-type': 'application/json'}
        response = requests.put(self.sts_application_url,
                                headers=headers,
                                data=self.get_template())

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code,
                                detail=f"There was an error editing the translation configuration template: {response.text}")

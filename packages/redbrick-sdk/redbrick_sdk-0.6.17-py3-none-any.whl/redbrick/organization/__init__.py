"""Organization class."""

from typing import List, Optional, Dict
from tqdm import tqdm  # type: ignore

from redbrick.common.enums import LabelType
from redbrick.common.context import RBContext
from redbrick.project import RBProject
from redbrick.utils.logging import print_warning
from .basic_project import get_active_learning_project, get_basic_project


class RBOrganization:
    """
    Representation of RedBrick organization.

    The RBOrganization object allows you to programmatically interact with
    your RedBrick organization. This class provides methods for querying your
    organization and doing other high level actions.
    """

    def __init__(self, context: RBContext, org_id: str) -> None:
        """Construct RBOrganization."""
        self.context = context

        self._org_id = org_id
        self._name: str

        self._get_org()

    def _get_org(self) -> None:
        org = self.context.project.get_org(self._org_id)
        self._name = org["name"]

    def taxonomies(self) -> List[str]:
        """Get a list of taxonomy names in the organization."""
        return self.context.project.get_taxonomies(self._org_id)

    def projects(self) -> List[RBProject]:
        """Get a list of active projects in the organization."""
        projects = self.context.project.get_projects(self._org_id)
        projects = list(filter(lambda x: x["status"] == "CREATION_SUCCESS", projects))
        return [
            RBProject(self.context, self._org_id, proj["projectId"])
            for proj in tqdm(projects)
        ]

    @property
    def org_id(self) -> str:
        """Retrieve the unique org_id of this organization."""
        return self._org_id

    @property
    def name(self) -> str:
        """Retrieve unique name of this organization."""
        return self._name

    def __str__(self) -> str:
        """Get string representation of RBOrganization object."""
        return f"RedBrick AI Organization - {self._name} - ( {self._org_id} )"

    def __repr__(self) -> str:
        """Representation of object."""
        return str(self)

    def create_project(
        self,
        name: str,
        label_type: LabelType,
        taxonomy_name: str,
        reviews: int = 0,
        active_learning: Optional[Dict] = None,
    ) -> RBProject:
        """
        Create a project within the organization.

        This method creates an organization in a similar fashion to the
        quickstart on the RedBrick Ai create project page.

        Parameters
        --------------
        name: str
            A unique name for your project

        label_type: redbrick.LabelType
            Configures the label and data type of your project.

        taxonomy_name: str
            The name of the taxonomy you want to use for this project.
            Taxonomies can be found on the left side bar of the platform.

        reviews: int = 0
            The number of review stages that you want to add after the label
            stage.

        Returns
        --------------
        redbrick.project.RBProject
            A RedBrick Project object.
        """
        if active_learning is not None:
            print_warning("active_learning arg is deprecated and will be ignored")
        stages = get_basic_project(reviews)

        project_data = self.context.project.create_project(
            self.org_id, name, stages, label_type.value, taxonomy_name
        )

        return RBProject(self.context, self.org_id, project_data["projectId"])

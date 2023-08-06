import logging
from typing import Dict

from rezide.utils import interfaces


class ConfigParser(interfaces.ConfigParserInterface):
    """Parses a config file and creates a Tree out of it."""

    def __init__(
        self,
        config_dict: Dict,
        tree_factory: interfaces.TreeFactoryInterface,
    ) -> None:
        self._tree_factory = tree_factory
        self._layout_definitions = config_dict

    def validate(self) -> None:
        for definition_name, definition_body in self._layout_definitions.items():
            if "command" in definition_body:
                self._validate_window(definition_name, definition_body)
            elif "children" in definition_body:
                self._validate_section(definition_name, definition_body)
            else:
                logging.error(definition_body)
                raise RuntimeError(
                    f"This definition is not a Window or Section: {definition_name}"
                )

    def _validate_window(self, definition_name: str, definition_body: Dict) -> None:
        if len(definition_body) != 1:
            raise RuntimeError(f"Window must only define command: {definition_name}")

    def _validate_section(self, definition_name: str, definition_body: Dict) -> None:
        keys = set(definition_body.keys())
        if not {"split", "children", "sizes"}.issubset(keys):
            raise RuntimeError(
                f"Section must define split, children, and sizes. keys defined: {keys}"
            )
        allowed_keys = {"split", "children", "sizes", "is_layout"}
        extra_keys = keys - allowed_keys
        if len(extra_keys) > 0:
            raise RuntimeError(
                f"Section must only define these keys: {allowed_keys}. extra keys"
                + f" defined: {extra_keys}"
            )
        if sum(definition_body["sizes"]) != 100:
            raise RuntimeError(f"Sum of sizes is not 100: {definition_name}")
        for child in definition_body["children"]:
            if child not in self._layout_definitions:
                raise RuntimeError(
                    f"{child} is a child of {definition_name} but is not defined"
                )
        if len(definition_body["children"]) < 2:
            raise RuntimeError(f"{definition_name} has less than 2 children")
        if len(definition_body["children"]) != len(definition_body["sizes"]):
            raise RuntimeError(
                "The number of children to not match the number of sizes in"
                + f" {definition_name}"
            )

    def get_tree(self) -> interfaces.TreeNodeInterface:
        """Parse and validate the layout, stitch together the node definitions, and
        create a tree out of them.
        """
        layout_top_definition = self._layout_definitions["root"]
        root_node = self._construct_subtree(layout_top_definition)
        return self._tree_factory.create_tree(root_node)

    def _construct_subtree(self, subtree_dict: Dict) -> Dict:
        if "command" in subtree_dict:
            return subtree_dict.copy()
        else:
            subtree = subtree_dict.copy()
            child_subtrees = []
            for child in subtree["children"]:
                child_definition = self._layout_definitions[child]
                if "mark" not in child_definition:
                    child_definition["mark"] = child
                child_subtrees.append(self._construct_subtree(child_definition))
            subtree["children"] = child_subtrees
            return subtree

from sovereign.modifiers.lib import Modifier
from sovereign.utils import templates


class Test(Modifier):
    def match(self) -> bool:
        return True

    def apply(self) -> None:
        assert templates
        self.instance["modifier_test_executed"] = True

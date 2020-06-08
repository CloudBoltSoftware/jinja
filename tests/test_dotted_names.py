import itertools
from importlib import reload
from jinja2 import Template


class Attributes:
    a = "aaa"
    b = {"next": "next level", "next.thing": "thing"}

    def myfunc(self):
        return "myfunc is called"


class TestDottedNames:

    def test_full_dot_key_match(self):
        dict = {"level0": "000", "level0.level1": "abc", "level0.level1.level2": "def"}
        t = Template("{{ level0.level1 }}")
        out = t.render(dict)
        assert out == "abc"
        t = Template("{{ level0.level1.level2 }}")
        out = t.render(dict)
        assert out == "def"
        t = Template("{{ level0 }}")
        out = t.render(dict)
        assert out == "000"

    def test_dotted_nested(self):
        dict2 = {"a": {"b": {"c.d": "e"}}}
        t2 = Template("{{ a.b.c.d }}")
        out2 = t2.render(dict2)
        assert out2 == "e"

    def test_dot_with_list(self):
        dict = {"a.b": ["1a", "2a"], "a": "nothere"}
        t = Template("{{a.b[0]}}")
        out = t.render(dict)
        assert out == "1a"
        t = Template("{{a.b[0][1]}}")
        out = t.render(dict)
        assert out == "a"

    def test_dot_with_attributes(self):
        t = Template("{{ level0.level1.b.next }}")
        ta = Attributes()
        dict = {"level0": "000", "level0.level1": ta, "level0.level1.level2": "def"}
        out = t.render(dict)
        assert out == "next level"

    def test_dot_with_attributes_return_dictStr(self):
        t = Template("{{ level0.level1.b }}")
        ta = Attributes()
        dict = {"level0": "000", "level0.level1": ta, "level0.level1.level2": "def"}
        out = t.render(dict)
        assert out == str({"next": "next level", "next.thing": "thing"})

    def test_names(self):
        t = Template(
            "{{ environment[0]|lower }}{{ platform[0:2]|lower}}{{ team[0]|lower "
            "}}{{ app|lower }}{% if os|lower == 'windows' %}11{% elif os|lower == "
            "'linux' %}15{% else %}17{% endif %}{{ sequence.MySequence }}")
        dict = {"environment": "PROD", "platform": "Azure", "team": "DevOps",
                "os": "Windows", "app": "Web", "sequence.MySequence": "001"}
        out = t.render(dict)
        assert out == "pazdweb11001"

    def test_for(self):
        template_test1 = "FOR:{% for key,val in level1.level2.level3.level4.level5.items() %} KEY: {{ key }} VAL: {{ val }} {% endfor %}"

        result_test1 = "FOR: KEY: message VAL: Hello, World 2! "

        dict = {
            "level1.level2": {
                "level3.level4.level5": {
                    "message": "Hello, World!"
                }
            },
            "level1.level2.level3": {
                "level4.level5": {
                    "message": "Hello, World 2!"
                }
            }
        }

        t = Template(template_test1)
        out = t.render(dict)
        assert out == result_test1

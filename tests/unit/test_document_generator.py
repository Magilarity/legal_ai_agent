# tests/unit/test_document_generator.py
import jinja2
import pytest

from app.document_generator import DocumentGenerator


@pytest.fixture(
    params=[
        # Simple greeting template
        ("Hello, {{ name }}!", {"name": "Alex"}, "Hello, Alex!"),
        # Arithmetic template
        (
            "Sum: {{ a }}+{{ b }}={{ result }}",
            {"a": 1, "b": 2, "result": 3},
            "Sum: 1+2=3",
        ),
    ]
)
def basic_template(request):
    return request.param


def test_render_simple_templates(basic_template):
    template, context, expected = basic_template
    gen = DocumentGenerator(template)
    output = gen.render(context)
    assert output == expected


def test_missing_variable_raises_undefined_error():
    gen = DocumentGenerator("Value: {{ missing }}")
    with pytest.raises(jinja2.exceptions.UndefinedError):
        gen.render({})


def test_security_violation_access_attr_raises():
    # Attempt to break sandbox
    gen = DocumentGenerator("{{ ''.__class__.__mro__ }}")
    with pytest.raises(jinja2.exceptions.SecurityError):
        gen.render({})


def test_control_structures_safe():
    # Simple loop and condition
    tmpl = "{% for x in items %}{{ x }}{% endfor %}"
    gen = DocumentGenerator(tmpl)
    output = gen.render({"items": ["a", "b", "c"]})
    assert output == "abc"

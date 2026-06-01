from app.preprocessing.text_cleaner import clean_text, normalize_whitespace


def test_clean_removes_non_ascii():
    assert clean_text("hello\x00world") == "helloworld"


def test_clean_collapses_whitespace():
    assert clean_text("foo   bar") == "foo bar"


def test_normalize_strips_blank_lines():
    text = "line1\n\n\nline2"
    result = normalize_whitespace(text)
    assert "\n\n" not in result
    assert "line1" in result
    assert "line2" in result

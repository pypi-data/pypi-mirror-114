"""Settings for reformater."""
# pylint: disable=C0301
# flake8: noqa
settings: dict = {
    # default indentation
    "indent": "    ",
    # indicates tags whose contents should not be formatted
    "ignored_tag_opening": r"<script|<style|<!--|{\*|<\?php|<pre",
    # indicates when to stop ignoring
    "ignored_tag_closing": r"</script|</style|-->|\*}|\?>|</pre",
    # the contents of these tag blocks will be start on a new line
    "tag_newline_before": r"([^\n])((?:\{% +?(?:if|end|for|block|endblock|else|spaceless|compress|load|include)|(?:<script)|(?:</?(html|head|body|div|a|nav|ul|ol|dl|li|table|thead|tbody|tr|th|td|blockquote|select|form|option|optgroup|fieldset|legend|label|header|main|section|aside|footer|figure|video|span|p|g|svg|button|h\d))))",
    # these tags should be followed by a newline
    "tag_newline_after": r"((?:\{% +?(?:if|end|for|block|else|spaceless|compress|load|include)(?:.*?%}))|(?:<html|<head|</head|<body|</body|</script|<div|</div|<nav|</nav|<ul|</ul|<ol|</ol|<dl|</dl|<li|</li|<table|</table|<thead|</thead|<tbody|</tbody|<tr|</tr|<th|</th|<td|</td|<blockquote|</blockquote|<select|</select|<form|</form|<option|</option|<optgroup|</optgroup|<fieldset|</fieldset|<legend|</legend|<label|</label|<header|</header|<main|</main|<section|</section|<aside|</aside|<footer|</footer|<figure|</figure|<video|</video|</span|<p|</p|<g|</g|<svg|</svg|</h\d).*?\>)([^\n])",
    # the contents of these tag blocks will be indented
    "tag_indent": r"\{% +?(if|for|block|else|spaceless|compress)|(?:<(?:html|head|body|div|a|nav|ul|ol|dl|li|table|thead|tbody|tr|th|td|blockquote|select|form|option|optgroup|fieldset|legend|label|header|main|section|aside|footer|figure|video|span|p|g|svg|h\d|button))",
    # this signals when tags should be unindented (see tags above)
    "tag_unindent": r"\{% end|(?:</(?:html|head|body|div|a|nav|ul|ol|dl|li|table|thead|tbody|tr|th|td|blockquote|select|form|option|optgroup|fieldset|legend|label|header|main|section|aside|footer|figure|video|span|p|g|svg|h\d|button))",
    # these tags should be unindented and next line will be indented
    "tag_unindent_line": r"\{% el",
    # these tags can sometimes be on one line
    "tag_pos_inline": r"\{% if.*endif %\}|\{% block.*endblock %\}|<link.*/>|<link.*\">|<link.*>|<meta.*/>|<script.*</script>|<div.*</div>|<a.*</a>|<li.*</li>|<dt.*</dt>|<dd.*</dd>|<th.*</th>|<td.*</td>|<legend.*</legend>|<label.*</label>|<option.*</option>|<input.*/>|<input.*\">|<span.*</span>|<p.*</p>|<path.*/>|<!--.*-->|<button.*</button>",
    # these tags use raw code and should flatten to column 1
    # tabs will be removed inside these tags! use spaces for spacing if needed!
    # flatten starting with this tag...
    "tag_raw_flat_opening": r"",
    # ...stop flattening when you encounter this tag
    "tag_raw_flat_closing": r"",
    # reduce empty lines greater than  x to 1 line
    "reduce_extralines_gt": 2,
    # if lines are longer than x
    "max_line_length": 99,
    "format_long_attributes": True,
    # pattern used to find attributes in a tag
    "attribute_pattern": r"([a-zA-Z-_]+=(?:\".*?\"|\'.*?\')|required|checked)\s*",
    "tag_pattern": r"(<\w+?)((?:\n\s*?[^>]+?)+?)(/?\>)",
}

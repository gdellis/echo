# Custom style for markdownlint (mdl)
# This file configures the rules for the mdl linter

# Configure rule MD007 (unordered list indentation)
# Allow 2-space indentation for unordered lists
rule 'MD007', indent: 2

# Configure rule MD033 (inline HTML)
# Allow specific inline HTML elements (comma-separated string)
rule 'MD033', allowed_elements: 'br, sub, sup, span, div, img, p'

# Configure rule MD013 (line length)
# Allow longer lines (200 chars), but not in code blocks
rule 'MD013', line_length: 200, ignore_code_blocks: true

# Disable specific rules using exclude_rule (rule names must be strings)
# These rules are excluded after enabling all to override default behavior
exclude_rule 'MD006'  # Inline HTML
exclude_rule 'MD012'  # Multiple blank lines
exclude_rule 'MD021'  # Headers not properly closed
exclude_rule 'MD022'  # Headers should be surrounded by blank lines
exclude_rule 'MD024'  # Multiple headers with same content
exclude_rule 'MD029'  # Ordered list item prefix
exclude_rule 'MD030'  # Spaces after list markers
exclude_rule 'MD047'  # Trailing newline
exclude_rule 'MD040'  # Code block style


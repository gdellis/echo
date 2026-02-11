# Custom style for markdownlint (mdl)
# This file configures the rules for the mdl linter

# Configure rule MD007 (unordered list indentation) - use 2-space indentation
# Configure rule MD033 (inline HTML) - allow specific inline HTML elements
# Configure rule MD013 (line length) - allow longer lines (200 chars) in code blocks

# Set indentation for MD007 (unordered list indentation)
rule 'MD007', indent: 0

# Allow inline HTML elements for MD033
rule 'MD033', allowed_elements: 'br, sub, sup, span, div, img, p'

# Set line length for MD013
rule 'MD013', line_length: 200, ignore_code_blocks: true
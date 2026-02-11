# Custom style for markdownlint (mdl)
# This file configures the rules for the mdl linter

# Enable all rules by default
all

# Disable specific rules using exclude_rule (rule names must be strings)
exclude_rule 'MD006'
exclude_rule 'MD012'
exclude_rule 'MD021'
exclude_rule 'MD047'
exclude_rule 'MD040'

# Configure rule MD007 (unordered list indentation)
# Allow 2-space indentation for unordered lists
rule 'MD007', params: { indent: 2 }

# Configure rule MD029 (ordered list prefixes)
# Allow "1." prefix for all ordered list items
rule 'MD029', params: { style: :one }

# Configure rule MD033 (inline HTML)
# Allow specific inline HTML elements (comma-separated string)
rule 'MD033', allowed_elements: 'br, sub, sup, span, div, img, p'

# Configure rule MD013 (line length)
# Allow longer lines (120 chars), but not in code blocks or tables
rule 'MD013', params: { line_length: 120, ignore_code_blocks: true, tables: false }


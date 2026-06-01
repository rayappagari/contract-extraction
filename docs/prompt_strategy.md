# Prompt Strategy

## Versioning

Prompts are stored in `prompts/` and versioned as plain Markdown files. The active version is controlled by the `prompt_version` parameter passed to `ContractExtractor.extract()`.

| File | Purpose |
|------|---------|
| `contract_extraction_v1.md` | Baseline — simple field list |
| `contract_extraction_v2.md` | Current — richer instructions, typed JSON schema |
| `amendment_prompt.md` | Amendment-specific extraction |

## Design Principles

- **Zero temperature**: All extraction calls use `temperature=0.0` for deterministic output.
- **JSON-only output**: Prompts instruct Claude to return raw JSON with no surrounding text.
- **Null over empty**: Missing fields must be `null`, not `""`, so confidence scoring is reliable.
- **Structured XML wrapping**: Contract text is wrapped in `<contract>` tags to clearly delineate input from instructions.

## Iteration Process

1. Identify failing fields in `evaluation_report.json`.
2. Modify the prompt in a new version file.
3. Run `evaluation/benchmark.py` against the full dataset.
4. Promote the new version if overall accuracy improves by ≥2%.

## Known Limitations

- Very long contracts (>100 pages) may require multi-chunk extraction with merging logic.
- Scanned PDFs with poor OCR quality degrade extraction accuracy significantly.
- Amendment extraction depends on having the original contract text for comparison.

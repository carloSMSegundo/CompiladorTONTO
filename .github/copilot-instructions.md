## Quick context — what this repo is

- This project implements a lexical analyzer for the TONTO language using PLY (Lex). The main entry point is `src/main.py` which calls `analisar_arquivo()` from `src/lexico_tonto.py` and writes outputs into the `outputs/` folder.

## How to run locally (Windows PowerShell)

```powershell
python -m venv venv
.\
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src\main.py tests\exemplo1.tonto --saida outputs
```

Notes: tests/ contains several example `.tonto` files you can use as inputs. The script writes `tabela_de_simbolos.{txt,csv,html}` and `erros_lexicos.txt` to the `outputs/` folder.

## Big-picture architecture and dataflow

- `src/lexico_tonto.py` builds a PLY lexer and exports `analisar_arquivo(caminho)` which:
  - reads the whole source file, feeds it to the lexer,
  - collects tokens into a `tabela_de_simbolos` list of dicts: { tipo, valor, linha, posicao },
  - collects lexical errors into the global list `erros_lexicos` and returns it alongside the table.
- `src/main.py` receives those results and is responsible for formatting and persisting them to disk.

## Important, project-specific lexer conventions (read before editing)

- Token families are declared in `reserved` and the `tokens` list in `src/lexico_tonto.py`.
  - Many reserved words include hyphens (e.g. `functional-complexes`) — those are treated as reserved tokens.
  - Class stereotypes, relation stereotypes, meta-attributes and native data types are explicitly enumerated in `reserved`.
- Naming rules enforced by the lexer:
  - CLASS_NAME: starts with an uppercase letter (including accented characters). Example: `Person` → CLASS_NAME.
  - RELATION_NAME: starts with a lowercase letter. Example: `owns` → RELATION_NAME.
  - INSTANCE_NAME: identifiers that include trailing digits (regex enforced). Example: `item123` → INSTANCE_NAME.
  - NEW_TYPE: identifiers that end with `DataType` and must not contain underscores or digits. See `t_NEW_TYPE`.
  - Identifiers with hyphens are invalid unless they exactly match an entry in `reserved` (hyphenated reserved words are allowed).

## Error handling patterns

- Lexical errors are appended to the module-level `erros_lexicos` list. `t_error` records an informative message and calls `lexer.skip(1)`.
- Several token rules return `None` to drop tokens while appending an error message to `erros_lexicos` (e.g. invalid identifiers or invalid NEW_TYPE names).

## How to extend or modify tokens safely

- When adding a new reserved word or stereotype, update the `reserved` dict in `src/lexico_tonto.py` and ensure its mapped token name is included in `tokens` if it is a new value.
- When adding new regex-based token functions, follow PLY conventions: named functions `t_<NAME>` with a docstring regex. Keep more specific rules above more general ones when order matters.
- If you change identifier validation (e.g. allow underscores), update both the regex and the error messages where `erros_lexicos` is appended.

## Useful examples (concrete) taken from code

- Reserved with hyphen: `functional-complexes` → token from `reserved` dict (treated as RESERVED_WORD).
- New type rule: `MyCustomDataType` → matches `t_NEW_TYPE` unless it contains `_` or digits (which will append an error).
- Identifier rule with hyphen error: `bad-name` (not in `reserved`) → lexer appends an error and drops token.

## Where to look next

- `src/lexico_tonto.py` — core lexer logic (token definitions, validation rules, error collection).
- `src/main.py` — persistence/formatting of outputs and the CLI surface.
- `tests/` — sample .tonto files used for manual verification.

If anything in these notes is unclear or you want more examples (e.g., suggested unit-test patterns or a quick tokenization script), tell me which part to expand.

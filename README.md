# Rhizi Importer

Client to import data into Rhizi nodes

## Using Python
```python
from client import RhiziAPIClient
client = RhiziAPIClient("http://localhost:8080", "test@test.com", "password")
client.create_node("ID-89388", data={"type"="Typed", "title"="The Most Awesome Title"})
client.create_node("ID-89389", data={"type"="Typed", "title"="The Second Most Awesome Title"})
client.create_edge("ID-89389", "ID-89388")
```

## Using Command-line

```bash
$ PYTHONPATH=. ./bin/rhizi-import --help
usage: rhizi-import [-h] [--base-url BASE_URL] [--user USER]
                    [--password PASSWORD] [--rz-doc-name RZ_DOC_NAME]
                    [--verbose VERBOSE] [--rules RULES] [--header HEADER]
                    filename

Rhizi Importer with simples options

positional arguments:
  filename              CSV file path

optional arguments:
  -h, --help            show this help message and exit
  --base-url BASE_URL   Base URL for the API
  --user USER           Username
  --password PASSWORD   Password
  --rz-doc-name RZ_DOC_NAME
                        Name of the document to update
  --verbose VERBOSE     Show / hide logs
  --rules RULES         yaml file with rules to create graph from csv
  --header HEADER       list of columns to use for header rows
```

Example invocation:

```
PYTHONPATH=. ./bin/rhizi-import --user test@example.com --password test --rules convertion.crz --base-url http://localhost:7000/ "phd/Rhizi Data - 2015.csv" --rz-doc-name "Welcome Rhizi"
```

Try first with a small example. This is experimental - probably off by one
errors and even more major stuff exists.

Example rules file: (extension is not important)

```
- node:
  - type: person
  - name: B + A
  - work address: X + Y + Z + AA + AB
  - subtype-tags: Phd student 2015


- node:
  - type: project
  - name: C
  - subtype-tags: Phd project


- node:
  - var: discipline-{name}
  - type: keyword
  - name: N-U
  - subtype-tags: Discipline


- node:
  - type: skill
  -  name: W
  - subtype-tags: Methodology


- node:
  - type: person
  - name: AJ + AI
  - email: AL
  - subtype-tags: Phd Supervisor


- node:
  - type: organisation
  - name: AN
  - description: AO
  - URL: AQ
  - subtype-tags: Research-Group


- node:
  - type: keyword
  - name: AX-BB
  - subtype-tags: Discipline


- node:
  - type: skill
  - name: BD
  - subtype-tags: Methodology


- node:
  - type: person
  - name: BG + BF
  - email: BI
  - subtype-tags: Group leader


- node:
  - type: organisation
  - name: BK
  - description: BL
  - URL: BN
  - subtype-tags: Lab


- node:
  - type: person
  - name: BQ + BP
  - subtype-tags: Lab director
  - email: BS


- node:
  - type: organisation
  - name: BT
  - subtype-tags: University/Institute
  - URL: BU


- node:
  - type: person
  - name: BX + BW
  - subtype-tags: Phd Supervisor
  - email: BZ


- node:
  - type: organisation
  - name: CB
  - description: CC
  - URL: CE
  - subtype-tags: Research-Group


- node:
  - type: keyword
  - name: CL-CP
  - subtype-tags: Discipline


- node:
  - name: CS
  - type: skill
  - subtype-tags: Methodology


- node:
  - type: person
  - name: CU + CV
  - subtype-tags: Group Leader
  - email: CX


- node:
  - type: organisation
  - name: CZ
  - subtype-tags: Lab
  - description: BK
  - URL: DB


- node:
  - type: person
  - name: DF + DE
  - subtype-tags: Lab director
  - email: DH


- node:
  - type: organisation
  - name: DI
  - subtype-tags: University/Institute
  - URL: DJ

- edges:
  - '[A+B] worked on [C]'

  - '[C] discipline [N-U]'

  - '[A+B] discipline [N-U]'

  - '[C] methodologies [W]'

  - '[A+B] supervised by [AI-AJ]'

  - '[A+B] supervised by [BX+BW]'

  - '[AI-AJ] worked at [AN]'

  - '[A+B] Worked at [AN]'

  - '[AX-BB] disciplines [AN]'

  - '[AN] discipline [AX-BB]'

  - '[AN] methodology [BD]'

  - '[BG+BF] group leader [AN]'

  - '[BK] lab of [AN]'

  - '[BQ-BP] director of [BK]'

  - '[BK] part of [BT]'

  - '[BX+BW] worked at [CB]'

  - '[A+B] Worked at [CB]'

  - '[AX-BB] disciplines [CB]'

  - '[CB] discipline [CL-CP]'

  - '[CB] methodology [BD]'

  - '[CV+CU] group leader [CB]'

  - '[CZ] lab of [CB]'

  - '[DE+DF] director of [CZ]'

  - '[CZ] part of [DI]'
```

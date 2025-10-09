# slideLabelGenerator
Create labels for light microscopy slides with QR code and description.

## local run
```shell
poetry env use python3.13
poetry install
apt-get install -y fonts-dejavu # to have fonts available


poetry run python test.py # expects /test/template.xlsx file..
```

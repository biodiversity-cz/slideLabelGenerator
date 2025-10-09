# slideLabelGenerator
Create labels for light microscopy slides with QR code and description.

## local run
```shell
poetry env use python3.13
poetry install

poetry run python test.py # expects /test/template.xlsx file..
```

Uses DejaVu font, available from https://www.fontsquirrel.com/fonts/download/dejavu-sans (extract and copy .ttf files to the /fonts directory).
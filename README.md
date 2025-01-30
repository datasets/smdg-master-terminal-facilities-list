<a className="gh-badge" href="https://datahub.io/core/smdg-master-terminal-facilities-list"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

List mantained by the [SMDG Secretariat](http://smdg.org/) to specify the port terminal facilities in UN/EDIFACT messages. The list is directly linked with the UN/LOCODE codelist (see [data package](http://data.okfn.org/data/core/un-locode))

## Data

Example segment where the main location is RULED (UN/LOCODE for Saint Petersburg, Russia) and the facility is PLP (SMDG code for Petrolesport).
```
LOC+11+RULED:139:6+PLP:72:306
```

## Preparation
Process is recorded and automated in python script:
```bash
# Install requirements
pip install -r scripts/requirementst.txt

# Run the script
python scripts/process.py
```

## Automation
Up-to-date (auto-updates every 3 months) smdg dataset could be found on the datahub.io: https://datahub.io/core/smdg-master-terminal-facilities-list

## License

All data is licensed under the [Creative Commons 4.0 Attribution License](https://creativecommons.org/licenses/by/4.0/). You may need to attribute the specific code to the SMDG Secretariat.
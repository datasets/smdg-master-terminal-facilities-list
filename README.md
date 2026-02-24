<a className="gh-badge" href="https://datahub.io/core/smdg-master-terminal-facilities-list"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

# SMDG Terminal Code List

List maintained by the [SMDG Secretariat](http://smdg.org/) to specify the port terminal facilities in UN/EDIFACT messages. The list is directly linked with the UN/LOCODE codelist (see [data package](http://data.okfn.org/data/core/un-locode))

## Data Source

This dataset is automatically synced from the official SMDG GitHub repository:
- **Source**: https://github.com/smdg-org/Terminal-Code-List
- **File**: SMDG Terminal Code List.csv

The data is updated automatically when changes are pushed to the GitHub repository.

## Data Format

The CSV file contains the following columns:
- **UNLOCODE**: Main location UN/LOCODE
- **Alternative UNLOCODE**: Alternative UN/LOCODE codes
- **Terminal Code**: Terminal facility code
- **Terminal Facility Name**: Name of the terminal facility
- **Terminal Company Name**: Company operating the terminal
- **Latitude (DMS)**: Latitude in Degrees Minutes Seconds format
- **Longitude (DMS)**: Longitude in Degrees Minutes Seconds format
- **Latitude**: Latitude in decimal degrees
- **Longitude**: Longitude in decimal degrees
- **Last Change**: Date of last modification
- **Valid From**: Date when the entry became valid
- **Valid Until**: Date when the entry expires
- **Terminal Website**: URL of the terminal's website
- **Terminal Address**: Physical address of the terminal
- **Remarks**: Additional notes

### Example

Example segment where the main location is RULED (UN/LOCODE for Saint Petersburg, Russia) and the facility is PLP (SMDG code for Petrolesport).
```
LOC+11+RULED:139:6+PLP:72:306
```

## Preparation

The update process is automated via a Python script:
```bash
# Install requirements
pip install -r scripts/requirements.txt

# Run the update script
python scripts/process.py
```

The script will:
1. Check for updates on GitHub
2. Download the latest CSV file if available
3. Process the CSV to match the expected format
4. Update the datapackage.json with the new version

## Automation

Up-to-date (auto-updates when GitHub source is updated) smdg dataset could be found on the datahub.io: https://datahub.io/core/smdg-master-terminal-facilities-list

## License

All data is licensed under the [Creative Commons 4.0 Attribution License](https://creativecommons.org/licenses/by/4.0/). You may need to attribute the specific code to the SMDG Secretariat.

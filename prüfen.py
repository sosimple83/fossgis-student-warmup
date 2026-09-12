import zipfile
import xml.etree.ElementTree as ET

for project_name in ['berlin_fk_starter.qgz', 'mainz_starter.qgz']:
    print(f"\n--- Prüfe: {project_name} ---")
    with zipfile.ZipFile(project_name, 'r') as z:
        qgs_filename = [name for name in z.namelist() if name.endswith('.qgs')][0]
        with z.open(qgs_filename) as f:
            tree = ET.parse(f)
            root = tree.getroot()
            # Alle Datenquellen-Pfade im QGIS-XML finden
            for elem in root.iter('datasource'):
                print(f"Layer-Pfad: {elem.text}")
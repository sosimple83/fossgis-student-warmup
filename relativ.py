import zipfile
import os
import shutil

for project_name in ['berlin_fk_starter.qgz', 'mainz_starter.qgz']:
    if not os.path.exists(project_name):
        continue

    # .qgz ist ein Zip-Archiv, darin liegt die .qgs-Projektdatei
    with zipfile.ZipFile(project_name, 'r') as z:
        qgs_filename = [name for name in z.namelist() if name.endswith('.qgs')][0]
        z.extract(qgs_filename, 'temp_extracted')

    qgs_path = os.path.join('temp_extracted', qgs_filename)

    # Text einlesen
    with open(qgs_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Die langen absoluten Windows-Pfade hart durch relative Pfade ersetzen
    # QGIS ersetzt absolute Pfade im qgs, wenn man ./data/... nutzt
    content = content.replace(
        r'C:\Users\Lenovo\Desktop\Desktop\Freelancer\projekte\hackathon\fossgis-student-warmup\data', './data')
    content = content.replace(r'C:\Users\Lenovo\Desktop\Desktop\Freelancer\projekte\hackathon\Daten\data', './data')

    # Zurückschreiben
    with open(qgs_path, 'w', encoding='utf-8') as f:
        f.write(content)

    # Wieder als .qgz zippen
    with zipfile.ZipFile(project_name, 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(qgs_path, qgs_filename)

print("Fertig! Alle Pfade in den Projektdateien wurden auf relative Pfade umgebogen.")

# Aufräumen
shutil.rmtree('temp_extracted', ignore_errors=True)
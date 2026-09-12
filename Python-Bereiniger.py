import zipfile
import os
import shutil
import xml.etree.ElementTree as ET

for project_name, subfolder, gpkg_name in [('berlin_fk_starter.qgz', 'berlin_fk', 'berlin_fk_base.gpkg'), ('mainz_starter.qgz', 'mainz', 'mainz_base.gpkg')]:
    if not os.path.exists(project_name):
        continue
        
    with zipfile.ZipFile(project_name, 'r') as z:
        qgs_filename = [name for name in z.namelist() if name.endswith('.qgs')][0]
        z.extract(qgs_filename, 'temp_extracted')
        
    qgs_path = os.path.join('temp_extracted', qgs_filename)
    
    tree = ET.parse(qgs_path)
    root = tree.getroot()
    
    # Wir sammeln bereits gesehene Layer-Namen, um Duplikate im Projekt zu verhindern
    seen_layers = set()
    
    for maplayer in list(root.iter('maplayer')):
        ds_elem = maplayer.find('datasource')
        layername_elem = maplayer.find('layername')
        
        if ds_elem is not None and ds_elem.text:
            # Prüfen, ob es ein GeoPackage ist oder eine alte Leiche (wie Documents)
            if '.gpkg' in ds_elem.text or 'gpkg' in ds_elem.text:
                name = None
                if layername_elem is not None and layername_elem.text:
                    name = layername_elem.text.split(' — ')[-1].strip()
                elif 'layername=' in ds_elem.text:
                    raw_name = ds_elem.text.split('layername=')[-1].split('|')[0]
                    name = raw_name.split(' — ')[-1].strip()
                
                if name:
                    # Wenn dieser Layer-Name in diesem Projekt schon da war, entfernen wir das doppelte Element
                    if name in seen_layers:
                        # Den parent layer-tree / layer-node finden und entfernen
                        # In QGIS XML liegen die maplayer meist direkt unter projectlayers
                        for parent in root.iter():
                            if maplayer in list(parent):
                                parent.remove(maplayer)
                    else:
                        seen_layers.add(name)
                        ds_elem.text = f"./data/{subfolder}/{gpkg_name}|layername={name}"
            else:
                # Alte Leichen (wie Documents oder absolute Pfade ohne gpkg) komplett aus dem Baum werfen
                for parent in root.iter():
                    if maplayer in list(parent):
                        parent.remove(maplayer)

    tree.write(qgs_path, encoding='utf-8', xml_declaration=True)
    
    with zipfile.ZipFile(project_name, 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(qgs_path, qgs_filename)

shutil.rmtree('temp_extracted', ignore_errors=True)
print("Absoluter Feinschliff und Deduplizierung erfolgreich abgeschlossen!")
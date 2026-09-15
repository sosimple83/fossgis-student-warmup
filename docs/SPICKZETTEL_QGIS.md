### 3b. Optional: Hitzeinseln verschneiden (Erweitertes Kriterium)
Falls ihr die Klimabelastung einbeziehen wollt:
1. Menü: **Vektor ➔ Geoverarbeitungswerkzeuge ➔ Verschneidung (Intersection)**
   * **Eingabelayer:** Eure zuvor erzeugten öffentlichen Parkplätze
   * **Überlagerungslayer:** `klima_hitzeinseln`
2. Neue Priorität im Feldrechner (`Strg + I`) vergeben:
   ```sql
   CASE 
     WHEN "temp_klasse" = 'Extrem' THEN 'Sehr Hoch'
     WHEN "temp_klasse" = 'Hoch'   THEN 'Hoch'
     ELSE 'Mittel'
   END
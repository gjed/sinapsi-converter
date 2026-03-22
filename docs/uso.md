# Sinapsi Converter - Guida all'uso

Converte i file CSV dei report Sinapsi (RAW_report) in file XLSX con tabella pivot.

## Uso su Windows (drag-and-drop)

1. Trascinare il file CSV sull'icona di `sinapsi-converter.exe`
1. Il file XLSX viene creato nella stessa cartella del CSV
1. Il nome del file di output segue il formato: `MERC  LETTURE  <codice>_<data>.xlsx`

## Uso da riga di comando (Linux/Windows)

```bash
sinapsi-converter percorso/al/file.csv
```

Oppure:

```bash
python -m sinapsi_converter percorso/al/file.csv
```

## Formato di output

Il file XLSX contiene due fogli:

### Foglio PIVOT

Riepilogo per appartamento:

- Ogni appartamento ha una riga di totale e le righe dei singoli dispositivi
- Colonna A: nome appartamento / dispositivo
- Colonna B: valore HCA (somma per gli appartamenti)
- Ultima riga: totale complessivo

### Foglio dati grezzi

Contiene tutti i dati del report originale:

- Righe 1-2: intestazione del file (metadata del report)
- Righe 4-8: dispositivi concentratori
- Riga 9: sotto-intestazioni "Attuale" / "Es.Prec"
- Riga 10: intestazioni colonne HCA
- Righe 11+: dispositivi HCA ordinati per appartamento
- Ultima riga: formule SOMMA per le colonne HCA

## Risoluzione problemi

- **"File non trovato"**: verificare che il percorso del file sia corretto
- **"Il file deve essere un CSV"**: il programma accetta solo file con estensione .csv
- **File di output vuoto**: verificare che il CSV sia nel formato Sinapsi RAW_report

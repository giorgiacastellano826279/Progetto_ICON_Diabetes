# KBS Diabete
Repository per il progetto di ingegneria della conoscenza 2026-2027. Realizzato da:
 - Castellano Giorgia (mat. 826279)
 - Liguori Silvia     (mat. 838174)

# Installazione
Posizionarsi all'interno della root principale:

`cd Progetto_ICON_Diabetes`

Creare l'ambiente virtuale (consigliato):

`python -m venv venv`

Attivare l'ambiente virtuale:
* Su Windows (Git Bash): `source venv/Scripts/activate`
* Su Linux/macOS: `source venv/bin/activate`

Installare le dipendenze:

`pip install -r requirements.txt`

# Guida all'utilizzo
Per avviare il sistema intelligente, eseguire il comando:

`python src/main.py`

## Caricamento dati
Il programma, una volta avviato, esegue la pulizia del dataset clinico (*Pima Indians Diabetes*) e avvia il Reasoner ontologico per categorizzare i pazienti in base alle linee guida mediche (ADA/OMS).

## Opzioni principali
Il menu interattivo mette a disposizione le seguenti opzioni operative:

- **Visualizzazione statistiche dataset e ontologia**: mostra il numero di pazienti esaminati e le istanze classificate dal Reasoner nelle classi derivate (es. pazienti iperglicemici, obesi o con profilo ad alto rischio).

- **Esecuzione Studio di Ablazione (Machine Learning)**: valuta le prestazioni dei classificatori (Random Forest, Logistic Regression, Decision Tree) confrontando i dati grezzi con quelli arricchiti dalle inferenze ontologiche tramite Repeated Stratified K-Fold.

- **Pianificazione dieta personalizzata (CSP)**: prende in esame un paziente clinico e, tramite propagazione dei vincoli e backtracking, genera un piano pasti giornaliero compatibile con i suoi limiti glicemici e calorici.

- **Ricerca percorso terapeutico ottimale (A\*)**: calcola la sequenza a costo minimo di interventi terapeutici e modifiche dello stile di vita per riportare i parametri patologici del paziente (glucosio, BMI, pressione) entro le soglie di sicurezza fisiologica.

### Esempi concreti di utilizzo delle opzioni del menu
- Se si seleziona l'opzione **Pianificazione dieta personalizzata (CSP)**, il sistema analizza i cut-off dedotti dalla Knowledge Base per il paziente selezionato e produce la composizione ottimale di colazione, pranzo e cena senza superare la soglia massima consentita di carboidrati.
- Se si desidera pianificare il rientro dei parametri di un paziente ad alto rischio, l'opzione **Ricerca percorso terapeutico ottimale (A\*)** esplora lo spazio degli stati e restituisce il piano di azione passo-passo (es. dieta, attività fisica mirata, terapia farmacologica) minimizzando lo sforzo complessivo.

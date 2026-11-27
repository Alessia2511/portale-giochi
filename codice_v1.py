import time
import sys
import os

# ============================================================
#   Q U I   P U O I   P E R S O N A L I Z Z A R E   T U T T O
#   - Cambia il nome, i messaggi, le domande, i ricordi
#   - Aggiungi quanti capitoli vuoi!
# ============================================================

NOME = "Marco"          # <-- metti il suo nome qui
NOME_TUO = "Giulia"     # <-- metti il tuo nome qui


# ── Utilità ─────────────────────────────────────────────────

def pulisci():
    os.system('cls' if os.name == 'nt' else 'clear')

def scrivi_lento(testo, velocita=0.03, a_capo=True):
    """Stampa il testo lettera per lettera."""
    for carattere in testo:
        sys.stdout.write(carattere)
        sys.stdout.flush()
        time.sleep(velocita)
    if a_capo:
        print()

def pausa(secondi=1.5):
    time.sleep(secondi)

def premi_invio(messaggio="  [ premi INVIO per continuare ]"):
    input(messaggio)

def linea(carattere="─", lunghezza=50):
    print(carattere * lunghezza)


# ── Schermata di caricamento ─────────────────────────────────

def caricamento():
    pulisci()
    print()
    scrivi_lento(f"  Inizializzazione in corso...", velocita=0.04)
    print()

    barra_lunghezza = 40
    messaggi = [
        "  Caricamento ricordi...",
        "  Raccolta momenti speciali...",
        "  Preparazione sorprese...",
        "  Quasi pronto...",
        "  Completato!              ",
    ]

    for i in range(barra_lunghezza + 1):
        percentuale = int((i / barra_lunghezza) * 100)
        blocchi = "█" * i
        spazi   = "░" * (barra_lunghezza - i)

        # Sceglie il messaggio in base alla percentuale
        if percentuale < 25:
            msg = messaggi[0]
        elif percentuale < 50:
            msg = messaggi[1]
        elif percentuale < 75:
            msg = messaggi[2]
        elif percentuale < 99:
            msg = messaggi[3]
        else:
            msg = messaggi[4]

        sys.stdout.write(f"\r  [{blocchi}{spazi}] {percentuale}%   {msg}")
        sys.stdout.flush()
        time.sleep(0.06)

    print("\n")
    pausa(0.5)


# ── Titolo / Apertura ────────────────────────────────────────

def apertura():
    pulisci()
    print()
    linea("═")
    scrivi_lento(f"        B U O N   C O M P L E A N N O", velocita=0.06)
    scrivi_lento(f"              {NOME.upper()}", velocita=0.08)
    linea("═")
    print()
    scrivi_lento(f"  Questo programma è stato scritto solo per te.", velocita=0.03)
    scrivi_lento(f"  Con tanto amore, da {NOME_TUO}.", velocita=0.03)
    print()
    premi_invio()


# ── Capitolo 1: il vostro inizio ─────────────────────────────

def capitolo_1():
    pulisci()
    print()
    linea()
    scrivi_lento("  CAPITOLO 1 — Come tutto è iniziato", velocita=0.04)
    linea()
    print()

    # 💡 PERSONALIZZA: racconta come vi siete conosciuti
    storia = [
        "Era una giornata qualunque...",
        "O almeno, così sembrava.",
        "E poi sei arrivato tu.",
        "",
        # aggiungi quante righe vuoi qui sotto!
        "Scrivi qui il vostro inizio. Ogni dettaglio conta.",
        "Il posto, il giorno, cosa hai pensato la prima volta.",
    ]

    for riga in storia:
        scrivi_lento(f"  {riga}", velocita=0.03)
        time.sleep(0.2)

    print()
    premi_invio()


# ── Capitolo 2: quiz su di voi ───────────────────────────────

def capitolo_2():
    pulisci()
    print()
    linea()
    scrivi_lento("  CAPITOLO 2 — Quanto mi conosci?", velocita=0.04)
    linea()
    print()
    scrivi_lento("  Rispondi alle domande. Niente paura, non c'è il voto!", velocita=0.03)
    print()
    pausa()

    # 💡 PERSONALIZZA: aggiungi le tue domande e risposte
    domande = [
        {
            "domanda": "Qual è il mio cibo preferito?",
            "risposta": "pizza",          # risposta corretta (minuscolo)
            "messaggio_ok":    "Esatto!! Mi conosci bene ❤",
            "messaggio_no":    "Nooo! Era la pizza! Come non lo sai?!"
        },
        {
            "domanda": "Qual è il posto dove siamo stati meglio insieme?",
            "risposta": "mare",
            "messaggio_ok":    "Sì! Quel viaggio non lo dimentico.",
            "messaggio_no":    "Era il mare! Ti ricordi quella sera?"
        },
        # ➕ aggiungi altre domande qui con lo stesso formato
    ]

    punti = 0
    for i, q in enumerate(domande):
        scrivi_lento(f"  Domanda {i+1}: {q['domanda']}", velocita=0.04)
        risposta = input("  > ").strip().lower()

        if risposta == q["risposta"]:
            punti += 1
            scrivi_lento(f"  ✓ {q['messaggio_ok']}", velocita=0.04)
        else:
            scrivi_lento(f"  ✗ {q['messaggio_no']}", velocita=0.04)
        print()
        pausa(0.8)

    linea()
    scrivi_lento(f"  Hai totalizzato {punti}/{len(domande)} punti!", velocita=0.05)

    # Messaggio finale in base al punteggio
    if punti == len(domande):
        scrivi_lento("  Perfetto! Mi conosci meglio di chiunque altro.", velocita=0.04)
    elif punti >= len(domande) // 2:
        scrivi_lento("  Non male! Ma puoi fare di meglio ;)", velocita=0.04)
    else:
        scrivi_lento("  Ehm... forse dobbiamo passare più tempo insieme!", velocita=0.04)

    print()
    premi_invio()


# ── Capitolo 3: messaggio nascosto ───────────────────────────

def capitolo_3():
    pulisci()
    print()
    linea()
    scrivi_lento("  CAPITOLO 3 — Un messaggio per te", velocita=0.04)
    linea()
    print()
    pausa(0.5)

    # 💡 PERSONALIZZA: scrivi qui il tuo messaggio più bello
    # Viene rivelato una riga alla volta, con pausa tra una e l'altra
    messaggio = [
        "Ci sono cose che non so dire a voce.",
        "Le parole mi escono storte, o non escono affatto.",
        "Perciò ho imparato a parlare così —",
        "nel linguaggio che ci unisce.",
        "",
        "Ogni riga di codice che scrivo,",
        "ogni errore che correggo,",
        "mi ricorda che anche le cose difficili",
        "alla fine funzionano.",
        "",
        # ➕ continua il messaggio qui...
        "Scrivi quello che senti davvero.",
        "Questo è il tuo spazio.",
    ]

    for riga in messaggio:
        scrivi_lento(f"  {riga}", velocita=0.035)
        time.sleep(0.3)

    print()
    premi_invio()


# ── Finale ───────────────────────────────────────────────────

def finale():
    pulisci()
    print()
    pausa(0.5)

    # Animazione cuore in ASCII
    cuore = [
        "        ♥♥♥♥♥   ♥♥♥♥♥      ",
        "      ♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥    ",
        "      ♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥    ",
        "        ♥♥♥♥♥♥♥♥♥♥♥♥♥      ",
        "          ♥♥♥♥♥♥♥♥♥        ",
        "            ♥♥♥♥♥          ",
        "              ♥            ",
    ]

    for riga in cuore:
        scrivi_lento(riga, velocita=0.01)
        time.sleep(0.05)

    print()
    scrivi_lento(f"  Tanti auguri, {NOME}.", velocita=0.06)
    scrivi_lento(f"  Con tutto il mio amore — {NOME_TUO}", velocita=0.05)
    print()
    linea("═")
    print()

    # 🔐 MESSAGGIO SEGRETO NASCOSTO NEL CODICE
    # Se lui legge il sorgente, trova questo:
    segreto = "ti_amo"  # ← lui lo troverà solo leggendo il codice 😉
    _ = segreto         # variabile "inutile"... o forse no?

    pausa(2)


# ── Main ─────────────────────────────────────────────────────

def main():
    caricamento()
    apertura()
    capitolo_1()
    capitolo_2()
    capitolo_3()
    finale()

if __name__ == "__main__":
    main()
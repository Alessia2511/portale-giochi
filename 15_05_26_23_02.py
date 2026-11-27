import pygame
import sys
import os
import random
import json
import math
import numpy as np

# --- SISTEMA LINGUE ---
lingua_selezionata = "it" # Lingua fissa italiana

LINGUE = {
    "it": {
        # Menu e U
        "start": "INIZIA", "exit": "ESCI", "settings": "IMPOSTAZIONI", "back": "INDIETRO",
        "resume": "RIPRENDI", "restart": "RICOMINCIA", "menu": "MENU INIZIALE", "help": "AIUTO",
        "skip": "SALTA",
        "vibe": "Vibrazione Schermo: ",
        "rules_title": "REGOLE DEL GIOCO:",
        "pause_title": "GIOCO IN PAUSA",
        "certificates": "ATTESTATI", "back_game": "TORNA AL GIOCO",
        "quit": "ESCI", "volume": "Volume:", "music": "Musica:", "sound": "Effetti Sonori:",
        "on": "ACCESA", "off": "SPENTA", "yes": "SI", "no": "NO",
        "pause": "PAUSA", "click_continue": "Clicca per continuare",
        "click_menu": "Clicca per tornare al menu",
        "your_certificates": "I TUOI ATTESTATI",
        "mission_complete": "MISSIONE COMPLETATA",
        "certificates_obtained": "ATTESTATI OTTENUTI:",
        "main_menu": "MENU PRINCIPALE", "exit_game": "ESCI DAL GIOCO",
        "back_menu": "TORNA AL MENU", "time": "TEMPO:",
        "time_up": "Tempo scaduto! Non hai risposto abbastanza in fretta.",
        
        # Titolo e intro
        "game_title": "KISS ME LIKE YOU LOVE ME: SHADOWS OF EQUALITY",
        "game_subtitle": "Un'esperienza interattiva che unisce il libro 'Kiss Me Like You Love Me' con i punti 5, 8 e 10 dell'Agenda 2030",
        "intro": "Niente è mai come appare e la verità è spesso un gioco di ombre.\nIn questa stanza sei circondato da segreti che attendono di essere svelati.\nNon è solo tecnologia: è potere, è libertà, è il diritto di non essere invisibili.\nEsplora ogni angolo, sfida i tuoi pregiudizi e non aver paura della complessità.\nLa parità non è un miraggio, ma una conquista coraggiosa.\nIl gioco sta per appena iniziare. Dimostra quanto vali.",
        
        # Regole
        "rule1": "1. LO SGUARDO\n\nGli oggetti che nascondono un segreto reagiranno\nal tuo passaggio con un leggero bagliore.\nNon tutto è subito accessibile.\nAlcuni segreti si sbloccheranno solo\nquando sarai pronto a vederli.\nImpara a osservare.",
        "rule2": "2. LA SCELTA\n\nOgni parola ha un peso.\nRispondi correttamente per avanzare.\nHai 30 secondi per rispondere.\nSe il tempo scade, il gioco finisce.",
        "rule3": "3. IL TRAGUARDO\n\nColleziona gli Attestati \nper sbloccare il finale.",
        "rule_final": "Il velo sta per alzarsi.\n\nClicca per entrare nell'ombra.",
        
        # Messaggi oggetti
        "pc_msg": "Un PC non è solo hardware, è il ponte che abbatte i confini:\ncollegare ogni individuo alla rete significa dare a tutti la stessa velocità di opportunità.",
        "watch_msg": "Il tempo non aspetta nessuno,\n ma la vera sfida è fare in modo che tutti abbiano lo stesso orario di partenza.\nRidurre le disuguaglianze significa sincronizzare le opportunità.",
        "phone_msg": "Uno smartphone ha mille sensori, ma nessuno vede la violenza che non lascia lividi.\n La parità non è un'app che si installa: è il coraggio di capire che il controllo non è amore, \n e che un genere non è un telecomando per la vita di un altro. \n Guarda bene lo schermo: chi sta muovendo chi.",
        "system_update": "SISTEMA AGGIORNATO:\nLa lampada e il cellulare sulla scrivania sono ora sbloccati.\nInteragisci con essi per continuare l'analisi.",
        "bonus_unlock": "BONUS SBLOCCATO! \nHai combattuto contro le disuguaglianze e abbattuto i pregiudizi.\nMa ora che l'equilibrio è ristabilito, sei pronto a perderti nel caos?\nLa storia di 'Kiss Me Like You Love Me' ti aspetta.\nEntra nel mondo di Selene e Neil, dove l'amore brucia e le ombre non perdonano.\nAttenzione: la perfezione dell'Agenda 2030 finisce qui. Benvenuti nell'abisso.",
        
        # Domande PC
        "pc_question": "Credi che la tecnologia possa davvero ridurre le disuguaglianze?",
        "pc_ans1": "Sì, se accessibile a tutti.",
        "pc_ans2": "No, crea solo più distacco.",
        "pc_wrong": "Se usata correttamente,\nla tecnologia è in grado di ridurre di molto le disuguaglianze.",
        
        # Domande Orologio
        "watch_question": "È giusto che tutti abbiano le stesse opportunità di partenza?",
        "watch_ans1": "Assolutamente sì.",
        "watch_ans2": "No, ognuno deve fare da sé.",
        "watch_wrong": "Ridurre le disuguaglianze significa proprio questo:\nFare in modo che tutti abbiano le stesse opportunità.",
        
        # Domande Cellulare
        "phone_q1": "Perché garantire a ogni donna il possesso di uno smartphone è un passo fondamentale verso l'uguaglianza?",
        "phone_q1_a1": "Le permette di partecipare attivamente alla vita economica e politica, facendo sentire la propria voce.",
        "phone_q1_a2": " È un modo per tenerla occupata e distoglierla da problemi sociali più complessi.",
        "phone_q1_wrong": "Hai confuso un diritto con un passatempo.\nLa tecnologia è un'arma per l'indipendenza.",
        
        "phone_q2": "In che modo l'uso consapevole della tecnologia può aiutare a contrastare la denigrazione della donna?",
        "phone_q2_a1": "Limitando l'uso dei social per evitare di esporsi a critiche o giudizi estetici.",
        "phone_q2_a2": "Creando reti di solidarietà e spazi sicuri dove denunciare abusi e rivendicare i propri diritti.",
        "phone_q2_wrong": "Il silenzio non ferma l'odio.\nSenza reti di solidarietà, le donne restano isolate.",
        
        "phone_q3": "Cosa significa, nel Punto 5 dell'Agenda 2030, includere le donne nella rivoluzione digitale?",
        "phone_q3_a1": "Fornire loro dispositivi economici e semplificati rispetto a quelli degli uomini.",
        "phone_q3_a2": "Abbattere i pregiudizi che negano alle donne le stesse competenze e opportunità tecnologiche degli uomini",
        "phone_q3_wrong": "L'uguaglianza non è semplificazione, è accesso alla complessità.",
        
        # Certificati
        "cert_p10_title": "Il Diritto di Essere Uguali",
        "cert_p10_body":"Complimenti! Hai smesso di guardare e hai iniziato a vedere.\nLa disuguaglianza prospera nell'indifferenza; tu hai scelto di riconoscerla.\nQuesto è il primo passo per distruggerla.",
        "cert_p10_name": "Il Diritto di Essere Uguali",
        
        "cert_p5_title": "La Forza della Parità",
        "cert_p5_body": "Nessuna donna dovrebbe chiedere il permesso per esistere.\nHai difeso il diritto all'autodeterminazione.",
        "cert_p5_name": "La Forza della Parità",
        
        "cert_final_title": "Il Cuore oltre l'Abisso",
        "cert_final_body": "Hai attraversato l'oscurità di Neil e la forza di Selene.\nHai capito che non esiste parità senza la conoscenza del trauma.\nOra sei pronto a riscrivere le regole.",
        "cert_final_name": "Il Cuore oltre l'Abisso",

        # Messaggio Lampada (Punto 8)
        "lamp_msg": "Questa luce dorata illumina ogni notte chi lavora nell'ombra.\nMa non basta lavorare: bisogna farlo con dignità.\nOgni persona, indipendentemente dal genere o dall'origine,\nha diritto a un lavoro equo, sicuro e rispettoso.\nIl controllo economico è una delle forme più silenziose di violenza.",

        # Domande Lampada (Punto 8)
        "lamp_q1": "Qual è il rischio più grave di una generazione senza lavoro dignitoso?",
        "lamp_q1_a1": "Si perde un'intera generazione di potenziale creativo e produttivo.",
        "lamp_q1_a2": "I giovani sviluppano maggiore autonomia cercando soluzioni alternative.",
        "lamp_q1_wrong": "I giovani senza lavoro non sviluppano autonomia:\nperdono dignità, prospettiva e fiducia nel futuro.\nUna società che non investe in loro non cresce, regredisce.",

        "lamp_q2": "In che modo il turismo sostenibile può essere uno strumento di giustizia economica?",
        "lamp_q2_a1": "Aumenta i guadagni dei grandi operatori internazionali del settore.",
        "lamp_q2_a2": "Genera lavoro dignitoso nelle comunità locali più fragili, distribuendo ricchezza.",
        "lamp_q2_wrong": "I grandi operatori non distribuiscono ricchezza: la concentrano. \n Il turismo che arricchisce solo chi è già ricco \n non è sviluppo, è estrattivismo con vista sul mare.",

        # Certificato Lampada (Punto 8)
        "cert_p8_title": "La Dignità nell'Ombra",
        "cert_p8_body": "Un'economia giusta non lascia generazioni senza lavoro\n né territori senza voce.\nHai capito che la ricchezza non è un problema quando circola.\nDiventa un'ingiustizia quando si ferma sempre nelle stesse mani.",
        "cert_p8_name": "La Dignità nell'Ombra",
        
        # Racconto finale
        "story0": "La storia che seguirà rappresenta il riflesso oscuro dei diritti precedentemente tutelati.\nCostituisce la cronaca di un legame tossico, dominato da istinti privi di regolamentazione.\nIl mondo di 'Kiss Me Like You Love Me' si presenta come un contesto in cui il sentimento non offre salvezza, ma conduce all'erosione individuale.",
        "story1": "Il trasferimento di Selene a New York \n la trascina nel mondo oscuro dei fratelli Miller \n e nel labirinto psicologico di Neil, \n un ragazzo spezzato da gravi traumi passati.",
        "story2": "Tra i due non nasce un amore convenzionale, \n ma un'ossessione logorante fatta di provocazioni e confini violati.",
        "story3": "In un equilibrio precario tra passione viscerale e rifiuti gelidi, \n Selene si ritrova a dover scegliere se soccombere \n o resistere alle ombre di Neil per tentare di comprenderlo.",

        # Schermata finale
        "final_conclusion": "Hai dimostrato che la consapevolezza è il primo passo per il cambiamento.\nAttraverso la tua esplorazione hai raccolto gli strumenti per costruire un futuro\nbasato sull'uguaglianza, la dignità del lavoro e la parità di genere.",
        
        # Credits
        "credits": [
            "KISS ME LIKE YOU LOVE ME: SHADOWS OF EQUALITY",
            "",
            "Sviluppato da: Patrono Alessia",
            "Realizzato in stretta collaborazione con le professoresse:",
            "Gabriella Testa e Silvia Mariggio',",
            "che hanno ispirato il progetto e guidato ogni passo della sua creazione.",
            "",
            "Ispirato al romanzo 'Kiss Me Like You Love Me' di Kira Shell",
            "",
            "OBIETTIVI AGENDA 2030:",
            "Punto 5: Parità di Genere",
            "Punto 8: Lavoro Dignitoso e Crescita Economica",
            "Punto 10: Ridurre le Disuguaglianze",
            "",
            "Progetto realizzato unendo il libro 'Kiss Me Like You Love Me',",
            "con i punti 5, 8 e 10 dell'Agenda 2030",
            "",
            "GRAZIE PER AVER GIOCATO",
        ]
    }
}

# --- 1. INIZIALIZZAZIONE ---
pygame.init()
pygame.mixer.init() 

# --- GENERAZIONE SUONI SINTETICI ---
def genera_suono_click():
    """Genera un suono di click breve, morbido e consonante"""
    sample_rate = 22050
    duration = 0.15
    # Uso un accordo consonante (Do maggiore: Do-Mi-Sol)
    frequencies = [523.25, 659.25, 783.99]  # C5, E5, G5
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave = np.zeros(len(t))
    # Somma le frequenze dell'accordo con decay esponenziale
    for freq in frequencies:
        wave += np.sin(2 * np.pi * freq * t) * np.exp(-15 * t)
    wave = wave / 3  # Normalizza
    wave = (wave * 32767 * 0.4).astype(np.int16)
    stereo = np.column_stack((wave, wave))
    return pygame.sndarray.make_sound(stereo)

def genera_suono_glitch():
    """Genera un suono glitch distorto ma musicalmente interessante"""
    sample_rate = 22050
    duration = 0.3
    t = np.linspace(0, duration, int(sample_rate * duration))
    # Usa frequenze dissonanti ma definite (tritono - "diabolus in musica")
    freq1 = 220  # A3
    freq2 = 311  # D#4 (tritono)
    # Alterna tra le due frequenze con modulazione
    modulation = np.sin(2 * np.pi * 8 * t)
    freq = freq1 + (freq2 - freq1) * (modulation + 1) / 2
    wave = np.sin(2 * np.pi * freq * t)
    # Aggiungi un po' di rumore controllato
    wave += 0.15 * np.random.random(len(t)) - 0.075
    wave = np.clip(wave, -1, 1)
    envelope = np.exp(-7 * t)
    wave *= envelope
    wave = (wave * 32767 * 0.5).astype(np.int16)
    stereo = np.column_stack((wave, wave))
    return pygame.sndarray.make_sound(stereo)

def genera_suono_achievement():
    """Genera un suono di achievement positivo e armonioso"""
    sample_rate = 22050
    duration = 0.5
    t = np.linspace(0, duration, int(sample_rate * duration))
    # Progressione armonica piacevole: Do-Mi-Sol-Do (arpeggio maggiore)
    frequencies = [523.25, 659.25, 783.99, 1046.50]  # C5, E5, G5, C6
    wave = np.zeros(len(t))
    # Ogni nota si sovrappone leggermente con la successiva
    for i, freq in enumerate(frequencies):
        start_time = i * duration / 5
        note_duration = duration / 3
        mask = (t >= start_time) & (t < start_time + note_duration)
        t_note = t[mask] - start_time
        envelope = np.exp(-6 * t_note) * np.sin(np.pi * t_note / note_duration)
        wave[mask] += np.sin(2 * np.pi * freq * t_note) * envelope
    wave = wave / 2  # Normalizza
    wave = (wave * 32767 * 0.5).astype(np.int16)
    stereo = np.column_stack((wave, wave))
    return pygame.sndarray.make_sound(stereo)

def genera_suono_transition():
    """Genera un suono swoosh per transizioni"""
    sample_rate = 22050
    duration = 0.3
    t = np.linspace(0, duration, int(sample_rate * duration))
    freq = 200 * (1 - t / duration) + 100
    wave = np.sin(2 * np.pi * freq * t) * (1 - t / duration)
    wave = (wave * 32767 * 0.5).astype(np.int16)
    stereo = np.column_stack((wave, wave))
    return pygame.sndarray.make_sound(stereo)

# Genera i suoni all'avvio
try:
    suono_click = genera_suono_click()
    suono_glitch = genera_suono_glitch()
    suono_achievement = genera_suono_achievement()
    suono_transition = genera_suono_transition()
    suoni_attivi = True
except:
    suoni_attivi = False
    print("Avviso: impossibile generare suoni sintetici")

cartella_progetto = os.path.dirname(__file__)
percorso_immagine = os.path.join(cartella_progetto, "immagine_sfondo.png")

percorso_menu = os.path.join(cartella_progetto, "musica_menu.mp3")
percorso_home = os.path.join(cartella_progetto, "musica_home.mp3")

volume_audio = 0.4
musica_attiva = True
effetti_sonori_attivi = True  # Toggle per gli effetti sonori

L_VIRTUAL, A_VIRTUAL = 1600, 900
info = pygame.display.Info()
monitor_w, monitor_h = info.current_w, info.current_h
win_w = min(L_VIRTUAL, int(monitor_w * 0.9))
win_h = int(win_w * (A_VIRTUAL / L_VIRTUAL))

screen = pygame.display.set_mode((win_w, win_h), pygame.RESIZABLE)
canvas = pygame.Surface((L_VIRTUAL, A_VIRTUAL))
pygame.display.set_caption("Kiss Me Like You Love Me: Shadows of Equality")

# --- CLASSE PARTICELLE ---
class Particella:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(0, L_VIRTUAL)
        self.y = random.randint(0, A_VIRTUAL)
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.5, -0.1)
        self.size = random.randint(2, 5)
        self.alpha = random.randint(50, 180)
        self.fade_speed = random.uniform(0.2, 0.8)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.alpha -= self.fade_speed
        if self.alpha <= 0 or self.y < -10:
            self.reset()

    def draw(self, surf):
        p_surf = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
        pygame.draw.circle(p_surf, (255, 255, 220, int(self.alpha)), (self.size, self.size), self.size)
        surf.blit(p_surf, (self.x, self.y))

particelle_polvere = [Particella() for _ in range(50)]

# --- RISORSE ---
try:
    sfondo_originale = pygame.image.load(percorso_immagine).convert()
    sfondo = pygame.transform.scale(sfondo_originale, (L_VIRTUAL, A_VIRTUAL))
except pygame.error:
    sfondo = pygame.Surface((L_VIRTUAL, A_VIRTUAL))
    sfondo.fill((200, 200, 200))

def gestisci_musica(percorso):
    if not musica_attiva: return
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(percorso)
        pygame.mixer.music.set_volume(volume_audio)
        pygame.mixer.music.play(-1, fade_ms=2000)
    except pygame.error:
        print(f"Nota: File {os.path.basename(percorso)} non trovato.")

def riproduci_suono(tipo_suono):
    """Riproduce un effetto sonoro se gli effetti sono attivi"""
    if not effetti_sonori_attivi or not suoni_attivi:
        return
    try:
        volume = volume_audio * 0.5  # Gli effetti sonori sono al 50% del volume generale
        if tipo_suono == "click":
            suono_click.set_volume(volume)
            suono_click.play()
        elif tipo_suono == "glitch":
            suono_glitch.set_volume(volume)
            suono_glitch.play()
        elif tipo_suono == "achievement":
            suono_achievement.set_volume(volume)
            suono_achievement.play()
        elif tipo_suono == "transition":
            suono_transition.set_volume(volume)
            suono_transition.play()
    except:
        pass

# COLORI E FONT
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
GRAY, GOLD = (220, 220, 220), (255, 215, 0)
GREEN, RED = (34, 139, 34), (200, 0, 0)
DARK_BAR = (5, 5, 5, 255)
COBALT_BLUE = (0, 71, 171)

font = pygame.font.SysFont("Arial", 22)
font_vittoria = pygame.font.SysFont("Arial", 28, bold=True)
font_button = pygame.font.SysFont("Arial", 18, bold=True)
font_small = pygame.font.SysFont("Arial", 14, bold=True) 
font_cert = pygame.font.SysFont("Times New Roman", 35, bold=True, italic=True)
font_titolo = pygame.font.SysFont("Arial", 60, bold=True)
font_domanda = pygame.font.SysFont("Arial", 24, bold=True)
# Font corsivo elegante per i nomi degli attestati
font_corsivo_attestati = pygame.font.SysFont("Georgia", 32, italic=True)

# --- STATI ---
MENU, STUDY, THOUGHT, DIALOGUE, END, PAUSE, CERTIFICATE, PORTFOLIO, FINAL_SCREEN, SETTINGS, CREDITS, RULES = range(12)
state = MENU
previous_state = MENU
state_before_pause = MENU  # Salva lo stato prima di andare in pausa (per gestire settings)
message_text, dialogue_step = "", 0
pc_clicked = watch_clicked = phone_clicked = books_clicked = lamp_clicked = vittoria = False
attestati_raccolti = []
mostrato_certificato_p10 = False
avviso_cellulare_mostrato = False
mostrato_avviso_bonus = False 
titolo_cert, corpo_cert = "", ""
char_index = 0
last_update = 0
TEMPO_RISPOSTA = 30000 
timer_inizio = 0
tempo_pausa = 0  # Tempo accumulato in pausa
timer_pausato = False  # Flag per sapere se il timer è in pausa
tempo_inizio_pausa = 0  # Momento in cui è iniziata la pausa
y_credits = A_VIRTUAL

indice_racconto = 0
regola_corrente = 1  # Nuova variabile per tracciare la regola corrente
glitch_intensity = 0.0  # Intensità effetto glitch (0.0 = nessuno, 1.0 = massimo)

# --- SISTEMA CHECKPOINT ---
checkpoint = {
    "pc_clicked": False,
    "watch_clicked": False,
    "phone_clicked": False,
    "lamp_clicked": False,
    "books_clicked": False,
    "mostrato_certificato_p10": False,
    "avviso_cellulare_mostrato": False,
    "attestati_raccolti": []
}

ALTEZZA_FASCIA = 250
Y_FASCIA = A_VIRTUAL - ALTEZZA_FASCIA 
Y_PULSANTI = Y_FASCIA + 140

pc_rect = pygame.Rect(860, 360, 220, 200)
watch_rect = pygame.Rect(1192, 435, 95, 95)
phone_rect = pygame.Rect(735, 550, 100, 45)
books_rect = pygame.Rect(435, 500, 125, 100)
lamp_rects = [
    pygame.Rect(664, 409, 67, 44),
    pygame.Rect(592, 444, 26, 24),
    pygame.Rect(593, 471, 25, 24),
    pygame.Rect(594, 502, 25, 24),
    pygame.Rect(590, 529, 26, 24),
    pygame.Rect(569, 557, 68, 22),
    pygame.Rect(574, 432, 41, 30),
    pygame.Rect(549, 450, 30, 28),
    pygame.Rect(636, 391, 32, 28),
    pygame.Rect(606, 411, 38, 30),
    pygame.Rect(665, 379, 40, 30),
]
lamp_rect = pygame.Rect(549, 379, 182, 200)
btn_pause_toggle = pygame.Rect(1430, 20, 150, 50) 
btn_zaino = pygame.Rect(1430, 80, 150, 50) 
btn_start_game = pygame.Rect(L_VIRTUAL // 2 - 150, 620, 300, 60)
btn_exit_game = pygame.Rect(L_VIRTUAL // 2 - 150, 710, 300, 60)

btn_close_rules = pygame.Rect(L_VIRTUAL // 2 - 150, 750, 300, 60)
btn_skip_rules = pygame.Rect(L_VIRTUAL - 220, 30, 180, 50)

btn_resume = pygame.Rect(L_VIRTUAL // 2 - 150, 220, 300, 60)
btn_restart = pygame.Rect(L_VIRTUAL // 2 - 150, 300, 300, 60)
btn_help = pygame.Rect(L_VIRTUAL // 2 - 150, 380, 300, 60)
btn_settings = pygame.Rect(L_VIRTUAL // 2 - 150, 460, 300, 60)
btn_back_menu = pygame.Rect(L_VIRTUAL // 2 - 150, 540, 300, 60)
btn_quit = pygame.Rect(L_VIRTUAL // 2 - 150, 620, 300, 60)
btn_toggle_music = pygame.Rect(L_VIRTUAL // 2 - 150, 380, 300, 55)
btn_back_from_settings = pygame.Rect(L_VIRTUAL // 2 - 150, 500, 300, 60)
btn_final_menu = pygame.Rect(L_VIRTUAL // 2 - 320, 750, 300, 60)
btn_final_exit = pygame.Rect(L_VIRTUAL // 2 + 20, 750, 300, 60)

btn_w, btn_h = 420, 80
gap = 40
start_x = (L_VIRTUAL - (btn_w * 2 + gap)) // 2
btn_left = pygame.Rect(start_x, Y_PULSANTI, btn_w, btn_h)
btn_right = pygame.Rect(start_x + btn_w + gap, Y_PULSANTI, btn_w, btn_h)
btn_large_left = pygame.Rect(start_x, Y_PULSANTI - 40, btn_w, 120)
btn_large_right = pygame.Rect(start_x + btn_w + gap, Y_PULSANTI - 40, btn_w, 120)

def reset_game():
    global state, previous_state, state_before_pause, pc_clicked, watch_clicked, phone_clicked, books_clicked, lamp_clicked, vittoria, mostrato_certificato_p10, attestati_raccolti, message_text, avviso_cellulare_mostrato, mostrato_avviso_bonus, indice_racconto, y_credits, char_index, regola_corrente, glitch_intensity, tempo_pausa, timer_pausato, tempo_inizio_pausa
    state = MENU
    previous_state = MENU
    state_before_pause = MENU
    message_text = ""
    char_index = 0
    pc_clicked = watch_clicked = phone_clicked = books_clicked = lamp_clicked = vittoria = False
    mostrato_certificato_p10 = avviso_cellulare_mostrato = mostrato_avviso_bonus = False
    checkpoint["pc_clicked"] = False
    checkpoint["watch_clicked"] = False
    checkpoint["phone_clicked"] = False
    checkpoint["lamp_clicked"] = False
    checkpoint["books_clicked"] = False
    checkpoint["mostrato_certificato_p10"] = False
    checkpoint["avviso_cellulare_mostrato"] = False
    checkpoint["attestati_raccolti"] = []
    indice_racconto = 0
    regola_corrente = 1
    attestati_raccolti = []
    glitch_intensity = 0.0
    y_credits = A_VIRTUAL
    tempo_pausa = 0
    timer_pausato = False
    tempo_inizio_pausa = 0
    gestisci_musica(percorso_menu)

def draw_text_centered(surf, text, y_pos, color=BLACK, bold=False, custom_font=None):
    used_font = custom_font if custom_font else (font_vittoria if bold else font)
    lines = text.split('\n')
    for i, line in enumerate(lines):
        t_s = used_font.render(line.strip(), True, color)
        t_r = t_s.get_rect(center=(L_VIRTUAL // 2, y_pos + (i * 35)))
        surf.blit(t_s, t_r)

def draw_button(canvas, rect, text, mouse_pos, color_override=None):
    is_hover = rect.collidepoint(mouse_pos)
    if color_override:
        base_color = (*color_override, 220) if is_hover else (*color_override, 180)
    else:
        base_color = (50, 50, 50, 220) if is_hover else (30, 30, 30, 180)
    
    btn_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(btn_surf, base_color, (0, 0, rect.width, rect.height), border_radius=12)
    canvas.blit(btn_surf, rect.topleft)
    
    words = text.split(' ')
    lines, curr = [], ""
    for w in words:
        if font_button.size(curr + w)[0] < rect.width - 20: curr += w + " "
        else: lines.append(curr); curr = w + " "
    lines.append(curr)
    for i, l in enumerate(lines):
        t_s = font_button.render(l.strip(), True, WHITE)
        t_r = t_s.get_rect(center=(rect.centerx, rect.centery - (len(lines)-1)*10 + i * 20))
        canvas.blit(t_s, t_r)

def draw_interactive_object(surf, rect, mouse_pos):
    if rect.collidepoint(mouse_pos):
        margin = 120 
        glow_surf = pygame.Surface((rect.width + margin*2, rect.height + margin*2), pygame.SRCALPHA)
        for i in range(50, 0, -1):
            alpha = int(70 * (1 - i/50)**3)
            expand = i * (margin / 50)
            pygame.draw.ellipse(glow_surf, (255, 255, 200, alpha), pygame.Rect(margin-expand, margin-expand, rect.width+expand*2, rect.height+expand*2))
        surf.blit(glow_surf, (rect.x - margin, rect.y - margin))

def lamp_collidepoint(pos):
    return any(r.collidepoint(pos) for r in lamp_rects)

def draw_lamp_glow(surf, mouse_pos):
    if lamp_collidepoint(mouse_pos):
        margin = 100
        for r in lamp_rects:
            glow_surf = pygame.Surface((r.width + margin*2, r.height + margin*2), pygame.SRCALPHA)
            for i in range(40, 0, -1):
                alpha = int(60 * (1 - i/40)**3)
                expand = i * (margin / 40)
                pygame.draw.ellipse(glow_surf, (255, 255, 200, alpha),
                    pygame.Rect(margin-expand, margin-expand, r.width+expand*2, r.height+expand*2))
            surf.blit(glow_surf, (r.x - margin, r.y - margin))

ROMANI = ["I", "II", "III", "IV", "V"]

def assegna_attestato(nome_base, corpo_base):
    global titolo_cert, corpo_cert
    numero = ROMANI[len(attestati_raccolti)]
    titolo_cert = f"Atto d'Amore {numero}:\n{nome_base}"
    corpo_cert = corpo_base
    nome_att = f"Atto d'Amore {numero}: {nome_base}"
    if nome_att not in attestati_raccolti:
        attestati_raccolti.append(nome_att)
        riproduci_suono("achievement")

def draw_checkmark(surf, rect):
    punti = [(rect.right - 20, rect.top + 10), (rect.right - 12, rect.top + 20), (rect.right - 4, rect.top + 4)]
    pygame.draw.lines(surf, GREEN, False, punti, 4)

def effetto_transizione(canvas_surf, screen_surf, clock, tipo="OUT"):
    fade_surf = pygame.Surface((L_VIRTUAL, A_VIRTUAL))
    fade_surf.fill(BLACK)
    range_alpha = range(0, 256, 8) if tipo == "OUT" else range(255, -1, -8)
    for alpha in range_alpha:
        fade_surf.set_alpha(alpha)
        real_w, real_h = screen_surf.get_size()
        screen_surf.blit(pygame.transform.smoothscale(canvas_surf, (real_w, real_h)), (0, 0))
        overlay_scaled = pygame.transform.smoothscale(fade_surf, (real_w, real_h))
        screen_surf.blit(overlay_scaled, (0, 0))
        pygame.display.flip()
        clock.tick(60)

def main():
    global state, previous_state, state_before_pause, message_text, pc_clicked, watch_clicked, phone_clicked, books_clicked, lamp_clicked, dialogue_step, vittoria, attestati_raccolti, titolo_cert, corpo_cert, mostrato_certificato_p10, avviso_cellulare_mostrato, mostrato_avviso_bonus, volume_audio, musica_attiva, effetti_sonori_attivi, indice_racconto, y_credits, timer_inizio, tempo_pausa, timer_pausato, tempo_inizio_pausa, char_index, last_update, regola_corrente, glitch_intensity
    running, clock = True, pygame.time.Clock()
    last_obj, txt_main = "", ""
    trascinando_volume = False
    gestisci_musica(percorso_menu)

    while running:
        real_w, real_h = screen.get_size()
        m_x, m_y = pygame.mouse.get_pos()
        m_pos = (m_x * L_VIRTUAL / real_w, m_y * A_VIRTUAL / real_h)
        
        # Recupera le traduzioni per la lingua corrente
        lang = LINGUE[lingua_selezionata]
        
        canvas.blit(sfondo, (0, 0))
        for p in particelle_polvere:
            p.update()
            p.draw(canvas)

        if state == DIALOGUE:
            if not timer_pausato:
                tempo_trascorso = pygame.time.get_ticks() - timer_inizio - tempo_pausa
            else:
                tempo_trascorso = pygame.time.get_ticks() - timer_inizio - tempo_pausa
            if tempo_trascorso > TEMPO_RISPOSTA:
                message_text, vittoria, state = lang["time_up"], False, END
                pygame.mixer.music.stop()

        clickable = False
        if state == MENU: clickable = btn_start_game.collidepoint(m_pos) or btn_exit_game.collidepoint(m_pos)
        elif state == RULES: clickable = True 
        elif state == STUDY: clickable = pc_rect.collidepoint(m_pos) or watch_rect.collidepoint(m_pos) or (mostrato_certificato_p10 and lamp_collidepoint(m_pos)) or (mostrato_certificato_p10 and phone_rect.collidepoint(m_pos)) or btn_pause_toggle.collidepoint(m_pos) or (vittoria and lamp_clicked and books_rect.collidepoint(m_pos)) or (attestati_raccolti and btn_zaino.collidepoint(m_pos))
        elif state == PAUSE: clickable = any(b.collidepoint(m_pos) for b in [btn_resume, btn_restart, btn_settings, btn_back_menu, btn_quit])
        elif state == SETTINGS: 
            bar_rect = pygame.Rect((L_VIRTUAL - 400) // 2, 315, 400, 20)
            clickable = any(b.collidepoint(m_pos) for b in [btn_toggle_music, btn_back_from_settings]) or bar_rect.collidepoint(m_pos)
        elif state == DIALOGUE: clickable = btn_left.collidepoint(m_pos) or btn_right.collidepoint(m_pos) or btn_large_left.collidepoint(m_pos) or btn_large_right.collidepoint(m_pos) or btn_pause_toggle.collidepoint(m_pos)
        elif state == FINAL_SCREEN: clickable = btn_final_menu.collidepoint(m_pos) or btn_final_exit.collidepoint(m_pos)
        elif state in [THOUGHT, CERTIFICATE, PORTFOLIO, END, CREDITS]: clickable = True
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if clickable else pygame.SYSTEM_CURSOR_ARROW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            tasto_premuto = pygame.mouse.get_pressed()
            if event.type == pygame.MOUSEBUTTONUP:
                trascinando_volume = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                tasto_premuto = pygame.mouse.get_pressed()
            if tasto_premuto[0] and state == SETTINGS:
                bar_rect = pygame.Rect((L_VIRTUAL - 400) // 2, 315, 400, 20)
                if bar_rect.collidepoint(m_pos):
                    volume_audio = (m_pos[0] - bar_rect.x) / bar_rect.width
                    volume_audio = max(0.0, min(1.0, volume_audio))
                    if musica_attiva:
                        pygame.mixer.music.set_volume(volume_audio)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == MENU:
                    if btn_start_game.collidepoint(m_pos): 
                        if musica_attiva: pygame.mixer.music.fadeout(1500)
                        effetto_transizione(canvas, screen, clock, "OUT") 
                        state = RULES
                        regola_corrente = 1
                    elif btn_exit_game.collidepoint(m_pos): running = False
                
                elif state == RULES:
                    regola_corrente += 1
                    if regola_corrente > 4:  # Fine delle slide delle regole
                        if previous_state == PAUSE:
                            # Torniamo alla pausa, ma dobbiamo assicurarci che 
                            # il pulsante "Riprendi" sappia dove tornare dopo.
                            state = PAUSE
                            # IMPORTANTE: previous_state ora deve tornare a essere STUDY 
                            # o lo stato in cui eri prima della pausa.
                            previous_state = STUDY 
                        else:
                            state = STUDY
                            gestisci_musica(percorso_home)
                            canvas.blit(sfondo, (0, 0))
                            effetto_transizione(canvas, screen, clock, "IN")
                        regola_corrente = 1

                elif state == STUDY:
                    if btn_pause_toggle.collidepoint(m_pos): 
                        state_before_pause = state
                        previous_state = state
                        state = PAUSE
                        pygame.mixer.music.set_volume(0.0)
                    elif btn_zaino.collidepoint(m_pos) and attestati_raccolti: state = PORTFOLIO; pygame.mixer.music.pause()
                    elif pc_rect.collidepoint(m_pos): 
                        checkpoint["pc_clicked"] = pc_clicked
                        checkpoint["watch_clicked"] = watch_clicked
                        checkpoint["phone_clicked"] = phone_clicked
                        checkpoint["lamp_clicked"] = lamp_clicked
                        checkpoint["books_clicked"] = books_clicked
                        checkpoint["mostrato_certificato_p10"] = mostrato_certificato_p10
                        checkpoint["avviso_cellulare_mostrato"] = avviso_cellulare_mostrato
                        checkpoint["attestati_raccolti"] = attestati_raccolti.copy()
                        char_index = 0
                        riproduci_suono("click")
                        message_text = lang["pc_msg"]
                        pc_clicked, last_obj, state = True, "PC", THOUGHT
                    elif watch_rect.collidepoint(m_pos): 
                        checkpoint["pc_clicked"] = pc_clicked
                        checkpoint["watch_clicked"] = watch_clicked
                        checkpoint["phone_clicked"] = phone_clicked
                        checkpoint["lamp_clicked"] = lamp_clicked
                        checkpoint["books_clicked"] = books_clicked
                        checkpoint["mostrato_certificato_p10"] = mostrato_certificato_p10
                        checkpoint["avviso_cellulare_mostrato"] = avviso_cellulare_mostrato
                        checkpoint["attestati_raccolti"] = attestati_raccolti.copy()
                        char_index = 0
                        riproduci_suono("click")
                        message_text = lang["watch_msg"]
                        watch_clicked, last_obj, state = True, "WATCH", THOUGHT
                    elif lamp_collidepoint(m_pos) and mostrato_certificato_p10:
                        checkpoint["pc_clicked"] = pc_clicked
                        checkpoint["watch_clicked"] = watch_clicked
                        checkpoint["phone_clicked"] = phone_clicked
                        checkpoint["lamp_clicked"] = lamp_clicked
                        checkpoint["books_clicked"] = books_clicked
                        checkpoint["mostrato_certificato_p10"] = mostrato_certificato_p10
                        checkpoint["avviso_cellulare_mostrato"] = avviso_cellulare_mostrato
                        checkpoint["attestati_raccolti"] = attestati_raccolti.copy()
                        char_index = 0
                        riproduci_suono("click")
                        message_text = lang["lamp_msg"]
                        lamp_clicked, last_obj, state = True, "LAMP", THOUGHT
                    elif books_rect.collidepoint(m_pos) and vittoria and lamp_clicked: 
                        indice_racconto = 0; char_index = 0
                        riproduci_suono("glitch")
                        message_text = lang["story0"]
                        books_clicked, last_obj, state = True, "BOOKS", THOUGHT
                        glitch_intensity = 0.5
                        pygame.time.delay(200) 
                    elif phone_rect.collidepoint(m_pos) and mostrato_certificato_p10: 
                        checkpoint["pc_clicked"] = pc_clicked
                        checkpoint["watch_clicked"] = watch_clicked
                        checkpoint["phone_clicked"] = phone_clicked
                        checkpoint["lamp_clicked"] = lamp_clicked
                        checkpoint["books_clicked"] = books_clicked
                        checkpoint["mostrato_certificato_p10"] = mostrato_certificato_p10
                        checkpoint["avviso_cellulare_mostrato"] = avviso_cellulare_mostrato
                        checkpoint["attestati_raccolti"] = attestati_raccolti.copy()
                        char_index = 0
                        riproduci_suono("click")
                        message_text = lang["phone_msg"]
                        phone_clicked, last_obj, state = True, "PHONE", THOUGHT
                
                elif state == PAUSE:
                    if btn_resume.collidepoint(m_pos): 
                        # Calcola quanto tempo è passato in pausa e aggiungilo al totale
                        if timer_pausato:
                            tempo_pausa += pygame.time.get_ticks() - tempo_inizio_pausa
                            timer_pausato = False
                        state = previous_state
                        if musica_attiva: pygame.mixer.music.set_volume(volume_audio)
                    elif btn_restart.collidepoint(m_pos): reset_game(); state = STUDY; gestisci_musica(percorso_home)
                    elif btn_help.collidepoint(m_pos):
                        previous_state = PAUSE
                        regola_corrente = 1
                        state = RULES
                    elif btn_settings.collidepoint(m_pos):
                        # Non modificare previous_state, mantieni lo stato prima della pausa
                        state = SETTINGS
                    elif btn_back_menu.collidepoint(m_pos): reset_game()
                    elif btn_quit.collidepoint(m_pos): running = False
                
                elif state == SETTINGS:
                    bar_rect = pygame.Rect((L_VIRTUAL - 400) // 2, 315, 400, 20)
                    if bar_rect.collidepoint(m_pos):
                        trascinando_volume = True
                        volume_audio = (m_pos[0] - bar_rect.x) / bar_rect.width
                        volume_audio = max(0.0, min(1.0, volume_audio))
                        if musica_attiva: pygame.mixer.music.set_volume(volume_audio)
                    elif btn_toggle_music.collidepoint(m_pos): 
                        musica_attiva = not musica_attiva
                        if musica_attiva:
                            pygame.mixer.music.play(-1); pygame.mixer.music.set_volume(volume_audio)
                        else: pygame.mixer.music.stop()
                    elif btn_back_from_settings.collidepoint(m_pos):
                        # Se eravamo in DIALOGUE prima della pausa, riprendi il timer e torna al gioco
                        if state_before_pause == DIALOGUE:
                            # Calcola quanto tempo è passato in pausa e aggiungilo al totale
                            if timer_pausato:
                                tempo_pausa += pygame.time.get_ticks() - tempo_inizio_pausa
                                timer_pausato = False
                            state = DIALOGUE
                            if musica_attiva: pygame.mixer.music.set_volume(volume_audio)
                        else:
                            state = previous_state
                            if musica_attiva: pygame.mixer.music.set_volume(volume_audio)

                elif state == THOUGHT:
                        if last_obj == "BOOKS":
                            indice_racconto += 1
                            if indice_racconto <= 3: 
                                char_index = 0
                                message_text = lang[f"story{indice_racconto}"]
                            else: 
                                assegna_attestato(lang["cert_final_name"], lang["cert_final_body"])
                                state = CERTIFICATE; last_obj = "FINAL_DONE" 
                        elif lang["system_update"] in message_text or lang["bonus_unlock"] in message_text: 
                            state = STUDY
                        elif last_obj == "PHONE": 
                            state, dialogue_step = DIALOGUE, 1
                            timer_inizio = pygame.time.get_ticks()
                            tempo_pausa = 0
                            timer_pausato = False
                        elif last_obj == "LAMP":
                            state, dialogue_step = DIALOGUE, "LAMP_Q1"
                            timer_inizio = pygame.time.get_ticks()
                            tempo_pausa = 0
                            timer_pausato = False
                        else: 
                            state, dialogue_step = DIALOGUE, ("PC_Q" if last_obj == "PC" else "WATCH_Q")
                            timer_inizio = pygame.time.get_ticks()
                            tempo_pausa = 0
                            timer_pausato = False
                
                elif state == CERTIFICATE:
                    if last_obj == "FINAL_DONE": state = CREDITS
                    elif vittoria and lamp_clicked and not mostrato_avviso_bonus: 
                        char_index = 0
                        message_text = lang["bonus_unlock"]
                        mostrato_avviso_bonus = True; state = THOUGHT
                        glitch_intensity = 0.15
                    elif mostrato_certificato_p10 and not avviso_cellulare_mostrato: 
                        char_index = 0
                        message_text = lang["system_update"]
                        avviso_cellulare_mostrato = True; state = THOUGHT
                    else: state = STUDY

                elif state == FINAL_SCREEN:
                    if btn_final_menu.collidepoint(m_pos): reset_game()
                    elif btn_final_exit.collidepoint(m_pos): running = False 
                elif state == PORTFOLIO: state = STUDY; pygame.mixer.music.unpause()
                elif state == END: reset_game()
                elif state == CREDITS: state = FINAL_SCREEN 
                elif state == DIALOGUE:
                    if btn_pause_toggle.collidepoint(m_pos): 
                        state_before_pause = state
                        previous_state = state
                        state = PAUSE
                        pygame.mixer.music.set_volume(0.0)
                        timer_pausato = True
                        tempo_inizio_pausa = pygame.time.get_ticks()
                    if dialogue_step == "PC_Q":
                        if btn_left.collidepoint(m_pos):
                            if watch_clicked and not mostrato_certificato_p10: 
                                mostrato_certificato_p10 = True
                                assegna_attestato(lang["cert_p10_name"], lang["cert_p10_body"])
                                state = CERTIFICATE
                            else: state = STUDY
                        elif btn_right.collidepoint(m_pos): 
                            watch_clicked = checkpoint["watch_clicked"]
                            phone_clicked = checkpoint["phone_clicked"]
                            lamp_clicked = checkpoint["lamp_clicked"]
                            books_clicked = checkpoint["books_clicked"]
                            mostrato_certificato_p10 = checkpoint["mostrato_certificato_p10"]
                            avviso_cellulare_mostrato = checkpoint["avviso_cellulare_mostrato"]
                            attestati_raccolti = checkpoint["attestati_raccolti"].copy()
                            char_index = 0
                            message_text = lang["pc_wrong"]
                            state = THOUGHT
                    elif dialogue_step == "WATCH_Q":
                        if btn_left.collidepoint(m_pos):
                            if pc_clicked and not mostrato_certificato_p10: 
                                mostrato_certificato_p10 = True
                                assegna_attestato(lang["cert_p10_name"], lang["cert_p10_body"])
                                state = CERTIFICATE
                            else: state = STUDY
                        elif btn_right.collidepoint(m_pos): 
                            pc_clicked = checkpoint["pc_clicked"]
                            phone_clicked = checkpoint["phone_clicked"]
                            lamp_clicked = checkpoint["lamp_clicked"]
                            books_clicked = checkpoint["books_clicked"]
                            mostrato_certificato_p10 = checkpoint["mostrato_certificato_p10"]
                            avviso_cellulare_mostrato = checkpoint["avviso_cellulare_mostrato"]
                            attestati_raccolti = checkpoint["attestati_raccolti"].copy()
                            char_index = 0
                            message_text = lang["watch_wrong"]
                            state = THOUGHT
                    elif dialogue_step == "LAMP_Q1":
                        if btn_left.collidepoint(m_pos):
                            dialogue_step = "LAMP_Q2"
                            timer_inizio = pygame.time.get_ticks()
                            tempo_pausa = 0
                            timer_pausato = False
                        elif btn_right.collidepoint(m_pos):
                            pc_clicked = checkpoint["pc_clicked"]
                            watch_clicked = checkpoint["watch_clicked"]
                            phone_clicked = checkpoint["phone_clicked"]
                            books_clicked = checkpoint["books_clicked"]
                            mostrato_certificato_p10 = checkpoint["mostrato_certificato_p10"]
                            avviso_cellulare_mostrato = checkpoint["avviso_cellulare_mostrato"]
                            attestati_raccolti = checkpoint["attestati_raccolti"].copy()
                            char_index = 0
                            message_text = lang["lamp_q1_wrong"]
                            state = THOUGHT
                    elif dialogue_step == "LAMP_Q2":
                        if btn_right.collidepoint(m_pos):
                            assegna_attestato(lang["cert_p8_name"], lang["cert_p8_body"])
                            state = CERTIFICATE
                        elif btn_left.collidepoint(m_pos):
                            pc_clicked = checkpoint["pc_clicked"]
                            watch_clicked = checkpoint["watch_clicked"]
                            phone_clicked = checkpoint["phone_clicked"]
                            books_clicked = checkpoint["books_clicked"]
                            mostrato_certificato_p10 = checkpoint["mostrato_certificato_p10"]
                            avviso_cellulare_mostrato = checkpoint["avviso_cellulare_mostrato"]
                            attestati_raccolti = checkpoint["attestati_raccolti"].copy()
                            char_index = 0
                            message_text = lang["lamp_q2_wrong"]
                            state = THOUGHT
                    elif dialogue_step == 1:
                        if btn_large_left.collidepoint(m_pos): 
                            dialogue_step = 2
                            timer_inizio = pygame.time.get_ticks()
                            tempo_pausa = 0
                            timer_pausato = False
                        elif btn_large_right.collidepoint(m_pos): 
                            pc_clicked = checkpoint["pc_clicked"]
                            watch_clicked = checkpoint["watch_clicked"]
                            lamp_clicked = checkpoint["lamp_clicked"]
                            books_clicked = checkpoint["books_clicked"]
                            mostrato_certificato_p10 = checkpoint["mostrato_certificato_p10"]
                            avviso_cellulare_mostrato = checkpoint["avviso_cellulare_mostrato"]
                            attestati_raccolti = checkpoint["attestati_raccolti"].copy()
                            char_index = 0
                            message_text = lang["phone_q1_wrong"]
                            state = THOUGHT
                            dialogue_step = 0
                    elif dialogue_step == 2:
                        if btn_large_right.collidepoint(m_pos): 
                            dialogue_step = 3
                            timer_inizio = pygame.time.get_ticks()
                            tempo_pausa = 0
                            timer_pausato = False
                        elif btn_large_left.collidepoint(m_pos): 
                            pc_clicked = checkpoint["pc_clicked"]
                            watch_clicked = checkpoint["watch_clicked"]
                            lamp_clicked = checkpoint["lamp_clicked"]
                            books_clicked = checkpoint["books_clicked"]
                            mostrato_certificato_p10 = checkpoint["mostrato_certificato_p10"]
                            avviso_cellulare_mostrato = checkpoint["avviso_cellulare_mostrato"]
                            attestati_raccolti = checkpoint["attestati_raccolti"].copy()
                            char_index = 0
                            message_text = lang["phone_q2_wrong"]
                            state = THOUGHT
                            dialogue_step = 0
                    elif dialogue_step == 3:
                        if btn_large_right.collidepoint(m_pos): 
                            vittoria = True
                            assegna_attestato(lang["cert_p5_name"], lang["cert_p5_body"])
                            state = CERTIFICATE
                        elif btn_large_left.collidepoint(m_pos): 
                            watch_clicked = checkpoint["watch_clicked"]
                            lamp_clicked = checkpoint["lamp_clicked"]
                            books_clicked = checkpoint["books_clicked"]
                            mostrato_certificato_p10 = checkpoint["mostrato_certificato_p10"]
                            avviso_cellulare_mostrato = checkpoint["avviso_cellulare_mostrato"]
                            attestati_raccolti = checkpoint["attestati_raccolti"].copy()
                            char_index = 0
                            message_text = lang["phone_q3_wrong"]
                            state = THOUGHT
                            dialogue_step = 0

        # --- LOGICA TRASCINAMENTO (Fuori dal ciclo eventi) ---
        if trascinando_volume and state == SETTINGS:
            bar_rect = pygame.Rect((L_VIRTUAL - 400) // 2, 315, 400, 20)
            volume_audio = (m_pos[0] - bar_rect.x) / bar_rect.width
            volume_audio = max(0.0, min(1.0, volume_audio))
            if musica_attiva:
                pygame.mixer.music.set_volume(volume_audio)
        
        # --- RENDERING ---
        if state == MENU:
            overlay = pygame.Surface((L_VIRTUAL, A_VIRTUAL), pygame.SRCALPHA)
            overlay.fill((0,0,0,195))
            canvas.blit(overlay, (0,0))
            draw_text_centered(canvas, lang["game_title"], 150, GOLD, True, font_titolo)
            draw_text_centered(canvas, lang["game_subtitle"], 240, WHITE, False, font_vittoria)
            draw_text_centered(canvas, lang["intro"], 380, GRAY, False, font)
            draw_button(canvas, btn_start_game, lang["start"], m_pos)
            draw_button(canvas, btn_exit_game, lang["exit"], m_pos)

        elif state == RULES:
            canvas.fill(BLACK) 
            pygame.draw.rect(canvas, GOLD, (250, 150, 1100, 600), 3, border_radius=15)
            draw_text_centered(canvas, lang["rules_title"], 200, GOLD, True)
            
            # Mostra la regola corrente
            if regola_corrente <= 3:
                draw_text_centered(canvas, lang[f"rule{regola_corrente}"], 400, WHITE, False)
            else:
                draw_text_centered(canvas, lang["rule_final"], 400, WHITE, False)
            


        elif state == STUDY:
            draw_interactive_object(canvas, pc_rect, m_pos)
            draw_interactive_object(canvas, watch_rect, m_pos)
            if vittoria and lamp_clicked: draw_interactive_object(canvas, books_rect, m_pos)
            if mostrato_certificato_p10: draw_lamp_glow(canvas, m_pos)
            if mostrato_certificato_p10: draw_interactive_object(canvas, phone_rect, m_pos)
            if pc_clicked: draw_checkmark(canvas, pc_rect)
            if watch_clicked: draw_checkmark(canvas, watch_rect)
            if lamp_clicked: draw_checkmark(canvas, lamp_rect)
            if vittoria: draw_checkmark(canvas, phone_rect) 
            if books_clicked and vittoria and lamp_clicked: draw_checkmark(canvas, books_rect)
            draw_button(canvas, btn_pause_toggle, lang["pause"], m_pos)
            if attestati_raccolti: 
                draw_button(canvas, btn_zaino, f" {lang['certificates']} ({len(attestati_raccolti)})", m_pos)
            
            # Effetto glitch progressivo basato su glitch_intensity
            if glitch_intensity > 0 and random.random() < (0.1 + glitch_intensity * 0.3):
                num_glitches = int(2 + glitch_intensity * 5)  # Da 2 a 7 glitch
                for _ in range(num_glitches):
                    gx_range = int(5 + glitch_intensity * 20)  # Offset orizzontale aumenta con intensità
                    gx = random.randint(-gx_range, gx_range)
                    gy = random.randint(0, A_VIRTUAL - 50)
                    gw = L_VIRTUAL
                    gh = random.randint(int(3 + glitch_intensity * 10), int(15 + glitch_intensity * 40))
                    try:
                        glitch_strip = canvas.subsurface((0, gy, gw, gh)).copy()
                        canvas.blit(glitch_strip, (gx, gy))
                        if random.random() < (0.2 + glitch_intensity * 0.3): 
                            intensity_color = int(50 + glitch_intensity * 150)
                            pygame.draw.rect(canvas, (random.randint(intensity_color, 255), 0, 0, 80), (0, gy, gw, gh), special_flags=pygame.BLEND_ADD)
                    except: pass

        elif state == DIALOGUE:
            pygame.draw.rect(canvas, DARK_BAR, (0, Y_FASCIA, L_VIRTUAL, ALTEZZA_FASCIA))
            rimanente = max(0, (TEMPO_RISPOSTA - (pygame.time.get_ticks() - timer_inizio - tempo_pausa)) // 1000)
            txt_timer = font_vittoria.render(f"{lang['time']} {rimanente}s", True, RED if rimanente < 4 else WHITE)
            canvas.blit(txt_timer, (1250, 30))
            draw_button(canvas, btn_pause_toggle, lang["pause"], m_pos)
            
            # Determina il testo della domanda in base al dialogue_step
            if dialogue_step == "PC_Q":
                txt_main = lang["pc_question"]
                draw_button(canvas, btn_left, lang["pc_ans1"], m_pos)
                draw_button(canvas, btn_right, lang["pc_ans2"], m_pos)
            elif dialogue_step == "WATCH_Q":
                txt_main = lang["watch_question"]
                draw_button(canvas, btn_left, lang["watch_ans1"], m_pos)
                draw_button(canvas, btn_right, lang["watch_ans2"], m_pos)
            elif dialogue_step == "LAMP_Q1":
                txt_main = lang["lamp_q1"]
                draw_button(canvas, btn_left, lang["lamp_q1_a1"], m_pos)
                draw_button(canvas, btn_right, lang["lamp_q1_a2"], m_pos)
            elif dialogue_step == "LAMP_Q2":
                txt_main = lang["lamp_q2"]
                draw_button(canvas, btn_left, lang["lamp_q2_a1"], m_pos)
                draw_button(canvas, btn_right, lang["lamp_q2_a2"], m_pos)
            elif dialogue_step == 1:
                txt_main = lang["phone_q1"]
                draw_button(canvas, btn_large_left, lang["phone_q1_a1"], m_pos)
                draw_button(canvas, btn_large_right, lang["phone_q1_a2"], m_pos)
            elif dialogue_step == 2:
                txt_main = lang["phone_q2"]
                draw_button(canvas, btn_large_left, lang["phone_q2_a1"], m_pos)
                draw_button(canvas, btn_large_right, lang["phone_q2_a2"], m_pos)
            elif dialogue_step == 3:
                txt_main = lang["phone_q3"]
                draw_button(canvas, btn_large_left, lang["phone_q3_a1"], m_pos)
                draw_button(canvas, btn_large_right, lang["phone_q3_a2"], m_pos)
            
            # Disegna la domanda centrata nella parte alta della fascia nera
            lines = txt_main.split('\n')
            start_y = Y_FASCIA + 60  # Domanda nella parte alta della fascia
            
            for i, line in enumerate(lines): 
                t_s = font_domanda.render(line, True, WHITE)
                t_r = t_s.get_rect(center=(L_VIRTUAL // 2, start_y + (i * 30)))
                canvas.blit(t_s, t_r)

        elif state == THOUGHT:
            overlay = pygame.Surface((L_VIRTUAL, A_VIRTUAL), pygame.SRCALPHA)
            overlay.fill((0,0,0,180))
            canvas.blit(overlay, (0,0))
            draw_text_centered(canvas, message_text, 400, WHITE)
            # Effetto glitch progressivo basato su glitch_intensity
            if glitch_intensity > 0 and random.random() < (0.1 + glitch_intensity * 0.3):
                num_glitches = int(2 + glitch_intensity * 5)  # Da 2 a 7 glitch
                for _ in range(num_glitches):
                    gx_range = int(5 + glitch_intensity * 20)  # Offset orizzontale aumenta con intensità
                    gx = random.randint(-gx_range, gx_range)
                    gy = random.randint(0, A_VIRTUAL - 50)
                    gw = L_VIRTUAL
                    gh = random.randint(int(3 + glitch_intensity * 10), int(15 + glitch_intensity * 40))
                    try:
                        glitch_strip = canvas.subsurface((0, gy, gw, gh)).copy()
                        canvas.blit(glitch_strip, (gx, gy))
                        if random.random() < (0.2 + glitch_intensity * 0.3): 
                            intensity_color = int(50 + glitch_intensity * 150)
                            pygame.draw.rect(canvas, (random.randint(intensity_color, 255), 0, 0, 80), (0, gy, gw, gh), special_flags=pygame.BLEND_ADD)
                    except: pass


        elif state == CERTIFICATE:
            overlay = pygame.Surface((L_VIRTUAL, A_VIRTUAL), pygame.SRCALPHA)
            overlay.fill((0,0,0,240))
            canvas.blit(overlay, (0,0))
            pygame.draw.rect(canvas, GOLD, (300, 200, 1000, 450), 4, border_radius=15)
            draw_text_centered(canvas, titolo_cert, 250, GOLD, True, font_cert)
            draw_text_centered(canvas, corpo_cert, 400, WHITE)
        
        elif state == PAUSE:
            overlay = pygame.Surface((L_VIRTUAL, A_VIRTUAL), pygame.SRCALPHA)
            overlay.fill((0,0,0,200))
            canvas.blit(overlay, (0,0))
            draw_text_centered(canvas, lang["pause_title"], 120, WHITE, True)
            draw_button(canvas, btn_resume, lang["resume"], m_pos)
            draw_button(canvas, btn_restart, lang["restart"], m_pos)
            draw_button(canvas, btn_help, lang["help"], m_pos)
            draw_button(canvas, btn_settings, lang["settings"], m_pos)
            draw_button(canvas, btn_back_menu, lang["menu"], m_pos)
            draw_button(canvas, btn_quit, lang["quit"], m_pos)
        
        elif state == SETTINGS:
            overlay = pygame.Surface((L_VIRTUAL, A_VIRTUAL), pygame.SRCALPHA)
            overlay.fill((0,0,0,230))
            canvas.blit(overlay, (0,0))
            draw_text_centered(canvas, lang["settings"], 120, GOLD, True, font_titolo)
            draw_text_centered(canvas, f"{lang['volume']} {int(volume_audio * 100)}%", 250, WHITE)
            bar_width, bar_height = 400, 20
            bar_x, bar_y = (L_VIRTUAL - bar_width) // 2, 315
            pygame.draw.rect(canvas, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height), border_radius=10)
            pygame.draw.rect(canvas, COBALT_BLUE, (bar_x, bar_y, int(bar_width * volume_audio), bar_height), border_radius=10)
            pygame.draw.rect(canvas, WHITE, (bar_x, bar_y, bar_width, bar_height), 2, border_radius=10)
            pos_pallino = bar_x + int(bar_width * volume_audio)
            pygame.draw.circle(canvas, WHITE, (pos_pallino, bar_y + 10), 10)
            # Toggle switch per la musica
            draw_text_centered(canvas, lang['music'], 360, WHITE)
            
            # Disegna il toggle switch
            toggle_width, toggle_height = 100, 40
            toggle_x = L_VIRTUAL // 2 - toggle_width // 2
            toggle_y = 400
            toggle_rect = pygame.Rect(toggle_x, toggle_y, toggle_width, toggle_height)
            
            # Colore di sfondo del toggle
            toggle_bg_color = COBALT_BLUE if musica_attiva else (100, 100, 100)
            pygame.draw.rect(canvas, toggle_bg_color, toggle_rect, border_radius=toggle_height // 2)
            
            # Posizione del pallino
            pallino_radius = toggle_height // 2 - 4
            if musica_attiva:
                pallino_x = toggle_x + toggle_width - pallino_radius - 6
            else:
                pallino_x = toggle_x + pallino_radius + 6
            pallino_y = toggle_y + toggle_height // 2
            
            # Disegna il pallino bianco
            pygame.draw.circle(canvas, WHITE, (pallino_x, pallino_y), pallino_radius)
            
            # Aggiorna il rect del bottone per il click
            btn_toggle_music.x = toggle_x
            btn_toggle_music.y = toggle_y
            btn_toggle_music.width = toggle_width
            btn_toggle_music.height = toggle_height
            
            draw_button(canvas, btn_back_from_settings, lang["back_game"], m_pos)

        elif state == FINAL_SCREEN:
            overlay = pygame.Surface((L_VIRTUAL, A_VIRTUAL), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 245))
            canvas.blit(overlay, (0, 0))
            draw_text_centered(canvas, lang["mission_complete"], 100, GOLD, True, font_titolo)
            draw_text_centered(canvas, lang["final_conclusion"], 220, WHITE)
            draw_text_centered(canvas, lang["certificates_obtained"], 380, GOLD, True)
            lista_finale = list(dict.fromkeys(attestati_raccolti))
            for i, a in enumerate(lista_finale):
                t_s = font_corsivo_attestati.render(f" {a}", True, GREEN)
                t_r = t_s.get_rect(center=(L_VIRTUAL // 2, 440 + (i * 45)))
                canvas.blit(t_s, t_r)
            draw_button(canvas, btn_final_menu, lang["main_menu"], m_pos)
            draw_button(canvas, btn_final_exit, lang["exit_game"], m_pos)
        
        elif state == PORTFOLIO:
            overlay = pygame.Surface((L_VIRTUAL, A_VIRTUAL), pygame.SRCALPHA)
            overlay.fill((0,0,0,230))
            canvas.blit(overlay, (0,0))
            draw_text_centered(canvas, lang["your_certificates"], 150, GOLD, True)
            lista_port = list(dict.fromkeys(attestati_raccolti))
            for i, a in enumerate(lista_port): 
                draw_text_centered(canvas, f" {a}", 300 + (i*80), WHITE, custom_font=font_corsivo_attestati)
        
        elif state == END:
            overlay = pygame.Surface((L_VIRTUAL, A_VIRTUAL), pygame.SRCALPHA)
            overlay.fill((0,0,0,200))
            canvas.blit(overlay, (0,0))
            draw_text_centered(canvas, message_text, 400, RED, True)
            draw_text_centered(canvas, lang["click_menu"], 650, WHITE)
        
        elif state == CREDITS:
            overlay = pygame.Surface((L_VIRTUAL, A_VIRTUAL), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 255))
            canvas.blit(overlay, (0, 0))
            testo_credits = lang["credits"]
            for i, linea in enumerate(testo_credits):
                t_s = font_vittoria.render(linea, True, GOLD if i == 0 else WHITE)
                t_r = t_s.get_rect(center=(L_VIRTUAL // 2, y_credits + (i * 60)))
                canvas.blit(t_s, t_r)
            y_credits -= 2 
            if y_credits < -(len(testo_credits) * 60): state = FINAL_SCREEN 

        screen.blit(pygame.transform.smoothscale(canvas, (real_w, real_h)), (0, 0))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()

if __name__ == "__main__": 
    main()
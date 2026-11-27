"""
PORTALE 2030 - Launcher interattivo degli SDGs
Passa il mouse sui colori della barra SDG per esplorare ogni obiettivo.

Requisiti: pygame, Pillow (PIL)
Installa con: pip install pygame pillow

Metti questo file nella stessa cartella di:
  - PORTALE_2030.jpg
  - agenda-2030-sviluppo-sostenibile-pace-giustizia-istituzioni-obiettivo-16.jpg

ADATTIVO: la logica interna lavora sempre in coordinate virtuali 1600×900,
poi tutto viene scalato allo schermo reale.
"""

import pygame
import sys
import os
import math
from PIL import Image
import json

# ─── Risoluzione virtuale di riferimento (NON cambiare) ───────────────────────
VIRT_W, VIRT_H = 1600, 900
FPS = 60
ASSETS_DIR = os.path.dirname(os.path.abspath(__file__))

# ─── Hitbox verticali delle barre SDG (coordinate virtuali @ 1600×900) ────────
TOP_BAR_Y0 = 0
TOP_BAR_Y1 = 121
BOT_BAR_Y0 = 859
BOT_BAR_Y1 = 900

# Pannelli interni (coordinate virtuali)
LEFT_PANEL_W  = 550
RIGHT_PANEL_W = 650
PANEL_MARGIN  = 30

# ─── Colori SDG con descrizioni ────────────────────────────────────────────────
SDG_DATA = [
    ((230, 34,  57),  "OBIETTIVO 1",  "Sconfiggere la\nPovertà",
     "Porre fine ad ogni forma di povertà nel mondo."),
    ((220, 162,  0),  "OBIETTIVO 2",  "Sconfiggere\nla Fame",
     "Azzerare la fame, raggiungere la sicurezza alimentare."),
    (( 35, 154, 34),  "OBIETTIVO 3",  "Salute e\nBenessere",
     "Garantire salute e benessere per tutti."),
    ((198,  43,  0),  "OBIETTIVO 4",  "Istruzione di\nQualità",
     "Istruzione equa, inclusiva e di qualità per tutti."),
    ((255,   4,  0),  "OBIETTIVO 5",  "Parità di\nGenere",
     "Raggiungere l'uguaglianza di genere."),
    ((  0, 180, 210),  "OBIETTIVO 6",  "Acqua Pulita e\nIgiene",
     "Garantire disponibilità e accesso all'acqua pulita."),
    ((245, 178,  1),  "OBIETTIVO 7",  "Energia Pulita\ne Accessibile",
     "Accesso all'energia pulita a costi accessibili."),
    ((130,  28,  0),  "OBIETTIVO 8",  "Lavoro Dignitoso\ne Crescita",
     "Promuovere crescita economica inclusiva e sostenibile."),
    ((255,  97,  0),  "OBIETTIVO 9",  "Imprese,\nInfrastrutture",
     "Costruire infrastrutture resilienti e sostenibili."),
    ((252,   0, 101),  "OBIETTIVO 10", "Ridurre le\nDisuguaglianze",
     "Ridurre le disuguaglianze all'interno dei Paesi."),
    ((255, 158,  0),  "OBIETTIVO 11", "Città e\nComunità",
     "Città e comunità inclusive e sostenibili."),
    ((186, 122,  0),  "OBIETTIVO 12", "Consumo\nResponsabile",
     "Garantire modelli di consumo e produzione sostenibili."),
    (( 36, 122, 59),  "OBIETTIVO 13", "Lotta contro\nil Clima",
     "Adottare misure urgenti contro i cambiamenti climatici."),
    ((  0, 149, 215),  "OBIETTIVO 14", "Vita\nSott'Acqua",
     "Conservare oceani, mari e risorse marine."),
    (( 16, 181,  0),  "OBIETTIVO 15", "Vita\nsulla Terra",
     "Gestire foreste, desertificazione e biodiversità."),
    ((  1,  98, 149),  "OBIETTIVO 16", "Pace, Giustizia\ne Istituzioni",
     "Pace, giustizia e istituzioni forti e inclusive."),
    ((  0,  72, 110),  "OBIETTIVO 17", "Partnership\nper gli Obiettivi",
     "Rafforzare i mezzi di attuazione dello sviluppo sostenibile."),
]

for i, entry in enumerate(SDG_DATA):
    if len(entry) == 4:
        SDG_DATA[i] = entry + (False,)

# ─── Segmenti X (coordinate virtuali @ 1600px) ────────────────────────────────
SDG_SEGMENTS = [
    (  0,  84),   # 1
    ( 92, 176),   # 2
    (187, 268),   # 3
    (282, 365),   # 4
    (375, 465),   # 5
    (471, 553),   # 6
    (565, 649),   # 7
    (659, 748),   # 8
    (750, 836),   # 9
    (845, 930),   # 10
    (939, 1025),  # 11
    (1035,1118),  # 12
    (1132,1214),  # 13
    (1229,1312),  # 14
    (1324,1406),  # 15
    (1416,1502),  # 16
    (1514,1600),  # 17
]


# ─── Gruppi di goal collegati (stesso videogioco) ─────────────────────────────
# Ogni goal mappa all'insieme di tutti i goal nel suo gruppo
_RAW_GROUPS = [
    {1, 2},
    {14, 15},
    {13, 7},
    {5, 10},
    {12, 17},
]
LINKED_GOALS: dict[int, set] = {}
for _grp in _RAW_GROUPS:
    for _g in _grp:
        LINKED_GOALS[_g] = _grp

# ─── Helpers ──────────────────────────────────────────────────────────────────
def pil_to_surface(pil_img: Image.Image) -> pygame.Surface:
    mode = pil_img.mode
    if mode not in ("RGBA", "RGB"):
        pil_img = pil_img.convert("RGBA")
        mode = "RGBA"
    raw = pil_img.tobytes()
    size = pil_img.size
    return pygame.image.fromstring(raw, size, mode)


def load_image(path: str, size=None) -> pygame.Surface | None:
    if not os.path.exists(path):
        return None
    try:
        pil_img = Image.open(path).convert("RGBA")
        if size:
            pil_img = pil_img.resize(size, Image.LANCZOS)
        return pil_to_surface(pil_img)
    except Exception as e:
        print(f"Errore caricamento {path}: {e}")
        return None


def draw_text_wrapped(surface, text, font, color, rect, line_spacing=4):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        if font.size(test)[0] <= rect.width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)

    y = rect.top
    for line in lines:
        if y + font.get_height() > rect.bottom:
            break
        surf = font.render(line, True, color)
        surface.blit(surf, (rect.left, y))
        y += font.get_height() + line_spacing


# ─── Pannello sinistro ─────────────────────────────────────────────────────────
class SDGPanel:
    def __init__(self, rect: pygame.Rect, goal_index: int, data: tuple, img_path: str | None):
        self.rect = rect
        self.goal_index = goal_index
        self.data = data
        self.anim_time = 0

        self.sdg_img = None
        if img_path and os.path.exists(img_path):
            try:
                pil = Image.open(img_path).convert("RGBA")
                iw, ih = pil.size
                max_h = rect.height - 20
                max_w = rect.width - 20
                scale = min(max_w / iw, max_h / ih)
                new_size = (int(iw * scale), int(ih * scale))
                pil = pil.resize(new_size, Image.LANCZOS)
                self.sdg_img = pil_to_surface(pil)
            except Exception as e:
                print(f"Errore caricamento immagine SDG: {e}")

        pygame.font.init()
        self.font_title = pygame.font.SysFont("Arial", 28, bold=True)
        self.font_body  = pygame.font.SysFont("Arial", 18)

    def update(self):
        self.anim_time += 1

    def draw(self, target: pygame.Surface):
        color = self.data[0]
        label = self.data[1]

        s = pygame.Surface(self.rect.size, pygame.SRCALPHA)


        if self.sdg_img:
            img_x = (self.rect.width - self.sdg_img.get_width()) // 2
            img_y = 100
            s.blit(self.sdg_img, (img_x, img_y))
        else:
            num_font = pygame.font.SysFont("Arial Black", 80, bold=True)
            num = num_font.render(str(self.goal_index), True, color)
            s.blit(num, (self.rect.width // 2 - num.get_width() // 2, 40))
            label_surf = self.font_title.render(label, True, (255, 255, 255))
            s.blit(label_surf, (self.rect.width // 2 - label_surf.get_width() // 2, 160))

        target.blit(s, self.rect.topleft)


# ─── Pannello destro ──────────────────────────────────────────────────────────
class GenericRightPanel:
    def __init__(self, rect: pygame.Rect, goal_index: int, data: tuple):
        self.rect = rect
        self.goal_index = goal_index
        self.data = data
        self.anim_time = 0

        pygame.font.init()
        self.font_big   = pygame.font.SysFont("Arial Black", 32, bold=True)
        self.font_med   = pygame.font.SysFont("Arial", 22)
        self.font_small = pygame.font.SysFont("Arial", 16)

    def update(self):
        self.anim_time += 1

    def draw(self, target: pygame.Surface):
        color = self.data[0]
        label = self.data[1]
        short = self.data[2]
        desc  = self.data[3]

        s = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        s.fill((248, 248, 248, 240))

        stripe_w = 8
        pygame.draw.rect(s, color, (0, 0, stripe_w, self.rect.height))

        num_font = pygame.font.SysFont("Arial Black", 90, bold=True)
        num_surf = num_font.render(str(self.goal_index), True, color + (30,))
        s.blit(num_surf, (self.rect.width - num_surf.get_width() - 20, 20))

        label_surf = self.font_big.render(label, True, color)
        s.blit(label_surf, (stripe_w + 20, 20))

        y = 70
        for line in short.split("\n"):
            line_surf = self.font_med.render(line, True, (50, 50, 50))
            s.blit(line_surf, (stripe_w + 20, y))
            y += 30

        y += 10
        pygame.draw.line(s, color, (stripe_w + 20, y), (self.rect.width - 20, y), 2)
        y += 15

        draw_text_wrapped(s, desc, self.font_med, (80, 80, 80),
                          pygame.Rect(stripe_w + 20, y, self.rect.width - stripe_w - 40, 120))
        y += 130

        btn_y = self.rect.height - 70
        btn_w, btn_h = 200, 44
        btn_x = stripe_w + 20
        pygame.draw.rect(s, color, (btn_x, btn_y, btn_w, btn_h), border_radius=6)
        btn_text = self.font_med.render("Scopri di più →", True, (255, 255, 255))
        s.blit(btn_text, (btn_x + btn_w // 2 - btn_text.get_width() // 2,
                           btn_y + btn_h // 2 - btn_text.get_height() // 2))

        pulse = abs(math.sin(self.anim_time * 0.05))
        border_alpha = int(100 + 155 * pulse)
        pygame.draw.rect(s, color + (border_alpha,), (0, 0, self.rect.width, self.rect.height), 3)

        target.blit(s, self.rect.topleft)


# ─── Classe principale ─────────────────────────────────────────────────────────

# ─── Pannello destro con immagine ─────────────────────────────────────────────
class ImageRightPanel:
    def __init__(self, rect, goal_index, data, img_path, keep_original_size=False):
        self.rect = rect
        self.goal_index = goal_index
        self.data = data
        self.anim_time = 0
        self.img = None
        if img_path and os.path.exists(img_path):
            try:
                pil = Image.open(img_path).convert("RGBA")
                if keep_original_size:
                    # Mantieni altezza originale, adatta solo la larghezza proporzionalmente
                    iw, ih = pil.size
                    scale = rect.width / iw
                    new_w = rect.width
                    new_h = int(ih * scale)
                    pil = pil.resize((new_w, new_h), Image.LANCZOS)
                else:
                    pil = pil.resize((rect.width, rect.height), Image.LANCZOS)
                self.img = pil_to_surface(pil)
            except Exception as e:
                print(f"Errore caricamento immagine pannello destro: {e}")

    def update(self):
        self.anim_time += 1

    def draw(self, target):
        s = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        if self.img:
            s.blit(self.img, (0, 0))
        target.blit(s, self.rect.topleft)

class Portale2030:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("PORTALE 2030 – Agenda 2030 per lo Sviluppo Sostenibile")

        # ── Rileva risoluzione dello schermo reale ────────────────────────────
        info = pygame.display.Info()
        screen_w = info.current_w
        screen_h = info.current_h

        usable_w = int(screen_w * 0.95)
        usable_h = int(screen_h * 0.92)
        scale_fit = min(usable_w / VIRT_W, usable_h / VIRT_H)

        self.win_w = int(VIRT_W * scale_fit)
        self.win_h = int(VIRT_H * scale_fit)
        self.scale_x = self.win_w / VIRT_W
        self.scale_y = self.win_h / VIRT_H

        self.virt_surf = pygame.Surface((VIRT_W, VIRT_H))

        self.screen = pygame.display.set_mode(
            (self.win_w, self.win_h),
            pygame.RESIZABLE
        )
        self.clock = pygame.time.Clock()

        self.bg_img = load_image(
            os.path.join(ASSETS_DIR, "PORTALE_2030.jpg"),
            (VIRT_W, VIRT_H)
        )
        if not self.bg_img:
            self.bg_img = pygame.Surface((VIRT_W, VIRT_H))
            self.bg_img.fill((240, 240, 240))

        self.hovered_goal  = 1
        self.prev_hovered  = 1
        self.alt_timer     = 0      # timestamp ms per alternanza pannello sinistro
        self.alt_index     = 0      # 0 = goal primario, 1 = goal collegato
        self.keyboard_goal = None   # goal selezionato da tastiera (None = tastiera inattiva)
        self.keyboard_active = False  # True quando le frecce hanno preso il controllo
        self.locked_goal   = 1      # goal bloccato da click (rimane anche senza hover)
        self._panels_cache: dict = {}

        self.font_hint  = pygame.font.SysFont("Arial", 14)
        # Font per le frecce ">" sopra i segmenti SDG
        self.font_arrow = pygame.font.SysFont("Arial Black", 20, bold=True)
        self.transition_alpha = 255
        self.arrow_anim_time = 0   # contatore animazione frecce

        print("PORTALE 2030 avviato.")
        print(f"Schermo rilevato: {screen_w}×{screen_h}")
        print(f"Finestra: {self.win_w}×{self.win_h}  (scala: {self.scale_x:.3f}×{self.scale_y:.3f})")
        print("Passa il mouse sui colori per esplorare gli SDGs.")
        print("[← →] Naviga con tastiera   [F] Fullscreen   [ESC] Esci")

    # ── Aggiorna le scale quando la finestra viene ridimensionata ─────────────
    def _update_scales(self):
        sw, sh = self.screen.get_size()
        self.win_w = sw
        self.win_h = sh
        self.scale_x = sw / VIRT_W
        self.scale_y = sh / VIRT_H

    # ── Converte coordinate mouse reali → virtuali ────────────────────────────
    def _to_virt(self, mx: int, my: int) -> tuple[int, int]:
        return int(mx / self.scale_x), int(my / self.scale_y)

    # ── Calcola il goal sotto il mouse ────────────────────────────────────────
    def get_goal_at(self, mx: int, my: int) -> int | None:
        rx, ry = self._to_virt(mx, my)

        in_top    = TOP_BAR_Y0 <= ry < TOP_BAR_Y1
        in_bottom = BOT_BAR_Y0 <= ry <= BOT_BAR_Y1

        if not (in_top or in_bottom):
            return None

        for i, (x0, x1) in enumerate(SDG_SEGMENTS):
            if x0 <= rx < x1:
                return i + 1
        return None

    # ── Costruisce i pannelli (lavora sempre in coord virtuali) ───────────────
    def get_panels(self, goal: int):
        if goal in self._panels_cache:
            return self._panels_cache[goal]

        idx  = goal - 1
        data = SDG_DATA[idx]

        panel_top_v = TOP_BAR_Y1 + PANEL_MARGIN
        panel_h_v   = BOT_BAR_Y0 - TOP_BAR_Y1 - PANEL_MARGIN * 2

        left_rect  = pygame.Rect(PANEL_MARGIN, panel_top_v, LEFT_PANEL_W, panel_h_v)
        right_rect = pygame.Rect(
            VIRT_W - RIGHT_PANEL_W - PANEL_MARGIN,
            panel_top_v, RIGHT_PANEL_W, panel_h_v
        )

        img_path = os.path.join(r"C:\Users\XXX\Documenti\portale_giochi", f"{goal}.png")

        left_panel  = SDGPanel(left_rect, goal, data, img_path)
        if goal in (5, 10):
            kiss_me_path = r"C:\Users\XXX\Documenti\portale_giochi\screen_home_kiss_me.png"
            img_x = PANEL_MARGIN + LEFT_PANEL_W + 20
            img_w = VIRT_W - img_x - PANEL_MARGIN
            img_rect = pygame.Rect(img_x, panel_top_v, img_w, panel_h_v)
            right_panel = ImageRightPanel(img_rect, goal, data, kiss_me_path)
        elif goal in (1, 2):
            ss_path = r"C:\Users\XXX\Documenti\portale_giochi\SS_1_2.png"
            img_x = PANEL_MARGIN + LEFT_PANEL_W + 20
            img_w = VIRT_W - img_x - PANEL_MARGIN
            img_offset_y = 100  # allineata alla foto del pannello sinistro
            img_rect = pygame.Rect(img_x, panel_top_v + img_offset_y, img_w, panel_h_v - img_offset_y)
            right_panel = ImageRightPanel(img_rect, goal, data, ss_path, keep_original_size=True)
        else:
            right_panel = GenericRightPanel(right_rect, goal, data)

        self._panels_cache[goal] = (left_panel, right_panel)
        return left_panel, right_panel

    # ── Disegna le frecce ">" sopra ogni segmento della barra superiore ───────
    def _draw_arrows(self):
        v = self.virt_surf
        self.arrow_anim_time += 1

        # Offset verticale oscillante (effetto bounce)
        bounce = int(math.sin(self.arrow_anim_time * 0.08) * 3)

        # Posizione Y: appena sopra la barra superiore (che inizia a Y=0)
        # Le frecce vengono disegnate all'interno della barra, centrate verticalmente
        arrow_y = TOP_BAR_Y0 + (TOP_BAR_Y1 - TOP_BAR_Y0) // 2 - 10 + bounce

        # Set dei goal collegati all'attivo (per illuminare le frecce)
        linked_set = LINKED_GOALS.get(self.hovered_goal, set()) if self.hovered_goal else set()

        for i, (x0, x1) in enumerate(SDG_SEGMENTS):
            goal_num = i + 1
            is_hovered = (self.hovered_goal == goal_num)
            is_linked  = (goal_num in linked_set and not is_hovered)

            # Colore: giallo se bloccato, bianco brillante se hovered, ciano se collegato, bianco semi-trasparente altrimenti
            is_locked  = (self.locked_goal == goal_num)
            if is_locked:
                color = (255, 255, 255)
                alpha = 255
                extra_bounce = int(math.sin(self.arrow_anim_time * 0.12) * 4)
                y = arrow_y + extra_bounce - bounce
            elif is_hovered:
                color = (255, 255, 255)
                alpha = 255
                # Offset bounce più accentuato per quello hovered
                extra_bounce = int(math.sin(self.arrow_anim_time * 0.12) * 4)
                y = arrow_y + extra_bounce - bounce  # annulla il bounce base e usa quello speciale
            elif is_linked:
                color = (255, 255, 255)
                alpha = 255
                extra_bounce = int(math.sin(self.arrow_anim_time * 0.12) * 4)
                y = arrow_y + extra_bounce - bounce
            else:
                color = (255, 255, 255)
                alpha = 160
                y = arrow_y

            # Renderizza il simbolo ">"
            arrow_surf = self.font_arrow.render(">", True, color)
            arrow_surf.set_alpha(alpha)

            # Centra la freccia nel segmento
            cx = (x0 + x1) // 2
            ax = cx - arrow_surf.get_width() // 2
            ay = y - arrow_surf.get_height() // 2

            v.blit(arrow_surf, (ax, ay))

    # ── Loop principale ───────────────────────────────────────────────────────
    def run(self):
        running = True

        while running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.VIDEORESIZE:
                    self._update_scales()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.locked_goal is not None:
                            # Prima ESC sblocca, seconda ESC esce
                            self.locked_goal   = None
                            self.keyboard_goal = None
                        else:
                            running = False
                    elif event.key == pygame.K_f:
                        self._toggle_fullscreen()
                    elif event.key == pygame.K_RIGHT:
                        # La tastiera prende il controllo anche se il mouse è sui rettangoli
                        base = self.locked_goal or self.keyboard_goal
                        if base is None:
                            self.keyboard_goal = 1
                        else:
                            self.keyboard_goal = (base % len(SDG_SEGMENTS)) + 1
                        self.locked_goal = self.keyboard_goal
                        self.keyboard_active = True
                        self.alt_timer = pygame.time.get_ticks()
                        self.alt_index = 0
                    elif event.key == pygame.K_LEFT:
                        base = self.locked_goal or self.keyboard_goal
                        if base is None:
                            self.keyboard_goal = len(SDG_SEGMENTS)
                        else:
                            self.keyboard_goal = ((base - 2) % len(SDG_SEGMENTS)) + 1
                        self.locked_goal = self.keyboard_goal
                        self.keyboard_active = True
                        self.alt_timer = pygame.time.get_ticks()
                        self.alt_index = 0

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Click sinistro: seleziona il goal sotto il cursore
                    mx_e, my_e = event.pos
                    clicked = self.get_goal_at(mx_e, my_e)
                    if clicked is not None:
                        self.locked_goal     = clicked
                        self.keyboard_goal   = clicked
                        self.keyboard_active = False
                        self.alt_timer = pygame.time.get_ticks()
                        self.alt_index = 0

            # ── Priorità: locked > mouse hover > tastiera ─────────────────────
            mx, my = pygame.mouse.get_pos()
            mouse_goal = self.get_goal_at(mx, my)

            if self.keyboard_active:
                # Tastiera ha priorità assoluta: il mouse NON sovrascrive mai
                self.hovered_goal = self.locked_goal
            elif mouse_goal is not None:
                # Mouse su un segmento: aggiorna selezione
                self.locked_goal   = mouse_goal
                self.hovered_goal  = mouse_goal
                self.keyboard_goal = None
            # Se mouse fuori dalle barre: mantieni l'ultimo goal attivo (hovered_goal invariato)

            if self.hovered_goal != self.prev_hovered:
                self.prev_hovered = self.hovered_goal
                self.transition_alpha = 255 if self.hovered_goal else 0
            # Se c'è un goal attivo, i pannelli devono essere sempre visibili
            if self.hovered_goal is not None:
                self.transition_alpha = 255
            if self.hovered_goal:
                lp, rp = self.get_panels(self.hovered_goal)
                lp.update()
                rp.update()

            # ── Alternanza automatica pannello sinistro per goal bloccati e collegati ────
            if self.locked_goal is not None and self.locked_goal in LINKED_GOALS:
                now = pygame.time.get_ticks()
                if now - self.alt_timer >= 1500:  # 1.5 secondi reali
                    self.alt_timer = now
                    self.alt_index = 1 - self.alt_index
            else:
                self.alt_timer = pygame.time.get_ticks()
                self.alt_index = 0

            self._render()

        pygame.quit()
        sys.exit()

    # ── Fullscreen toggle ─────────────────────────────────────────────────────
    def _toggle_fullscreen(self):
        flags = self.screen.get_flags()
        if flags & pygame.FULLSCREEN:
            self.screen = pygame.display.set_mode(
                (self.win_w, self.win_h), pygame.RESIZABLE
            )
        else:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self._update_scales()

    # ── Blit la superficie virtuale scalata sullo schermo reale ───────────────
    def _blit_virt(self):
        sw, sh = self.screen.get_size()
        if sw == VIRT_W and sh == VIRT_H:
            self.screen.blit(self.virt_surf, (0, 0))
        else:
            scaled = pygame.transform.smoothscale(self.virt_surf, (sw, sh))
            self.screen.blit(scaled, (0, 0))

    # ── Render ────────────────────────────────────────────────────────────────
    def _render(self):
        v = self.virt_surf
        v.fill((200, 200, 200))

        if self.bg_img:
            v.blit(self.bg_img, (0, 0))

        # ── Disegna sempre le frecce ">" sopra la barra superiore ──
        self._draw_arrows()

        if self.hovered_goal and self.transition_alpha > 0:
            lp, rp = self.get_panels(self.hovered_goal)

            # Se bloccato su un goal collegato, il pannello sinistro alterna
            if self.locked_goal is not None and self.locked_goal in LINKED_GOALS:
                linked = sorted(LINKED_GOALS[self.locked_goal])
                alt_goal = linked[self.alt_index % len(linked)]
                lp, _ = self.get_panels(alt_goal)

            panel_surf = pygame.Surface((VIRT_W, VIRT_H), pygame.SRCALPHA)
            lp.draw(panel_surf)
            rp.draw(panel_surf)

            panel_surf.set_alpha(self.transition_alpha)
            v.blit(panel_surf, (0, 0))

            self._draw_highlight()

        if not self.hovered_goal:
            self._draw_hint()

        self._blit_virt()
        pygame.display.flip()

    def _draw_highlight(self):
        if not self.hovered_goal:
            return
        v = self.virt_surf

        is_locked = (self.locked_goal == self.hovered_goal)

        # Tutti i goal da evidenziare: quello attivo + i suoi collegati
        linked = LINKED_GOALS.get(self.hovered_goal, {self.hovered_goal})

        for goal_num in linked:
            idx = goal_num - 1
            x0, x1 = SDG_SEGMENTS[idx]

            is_primary = (goal_num == self.hovered_goal)

            if is_locked:
                color = (255, 255, 255)
                thickness = 7 if is_primary else 5
            else:
                color = (255, 255, 255)
                thickness = 3

            pygame.draw.rect(v, color,
                             (x0, TOP_BAR_Y0, x1 - x0, TOP_BAR_Y1 - TOP_BAR_Y0), thickness)
            pygame.draw.rect(v, color,
                             (x0, BOT_BAR_Y0, x1 - x0, BOT_BAR_Y1 - BOT_BAR_Y0), thickness)

    def _draw_hint(self):
        v = self.virt_surf
        hint = self.font_hint.render(
            "Passa il mouse sui colori  •  oppure usa ← → per navigare gli Obiettivi di Sviluppo Sostenibile",
            True, (100, 100, 100)
        )
        x = VIRT_W // 2 - hint.get_width() // 2
        y = VIRT_H // 2 - hint.get_height() // 2
        bg = pygame.Surface((hint.get_width() + 20, hint.get_height() + 10), pygame.SRCALPHA)
        bg.fill((255, 255, 255, 160))
        v.blit(bg, (x - 10, y - 5))
        v.blit(hint, (x, y))


# ─── Avvio ─────────────────────────────────────────────name──────────────────────────────
if __name__ == "__main__":
    app = Portale2030()
    app.run()
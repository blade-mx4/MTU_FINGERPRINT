"""
enrollment_gui.py
-----------------
CustomTkinter front-end for client.py (fingerprint enrollment).

Flow (from the "GUI NOTES" in client.py):
    1. Operator fills in the student details.
    2. "Capture fingerprint" -> scan is taken on a worker thread.
    3. The captured image is shown so the operator can judge its quality.
    4. "Enroll student" (upload + DB row)  or  "Retake".

COM port and baud rate are constants. Everything slow (sensor read, HTTP upload)
runs on a background thread; results come back to the UI through a queue.

Requires:  pip install customtkinter pillow pandas requests
"""

import json
import os
import queue
import threading

import customtkinter as ctk
import pandas as pd
import requests as rq
from PIL import Image

from getImage import getFingerprintImage
from client import Client, url, img_folder_path, cw_fldr

# ============================== CONSTANTS =================================== #
PORT = "COM9"
BAUD_RATE = 115200
LEVELS = ["100", "200", "300", "400", "500"]
MATRIC_LEN = 11
PREVIEW_BOX = (300, 330)          # max width, height of the fingerprint preview

# Colours are (light mode, dark mode) pairs
BG_CARD = ("#ffffff", "#171a21")
BG_WELL = ("#eef1f5", "#0d0f14")
TEXT_MUTED = ("#6b7280", "#8b93a3")
ACCENT = ("#0f766e", "#14b8a6")
ACCENT_HOVER = ("#115e59", "#0d9488")
OK = "#22c55e"
WARN = "#f59e0b"
ERR = "#ef4444"
INFO = "#8b93a3"
# ============================================================================ #


class EnrollmentSession(Client):
    """
    Client, with post_data_img() split in two so the operator can look at the scan
    before anything is sent to the server or written to DB.csv.
    """

    def capture(self) -> str:
        self.filename = f"{self.ID}.bmp"
        self.img_path = os.path.join(img_folder_path, self.filename)
        ok = getFingerprintImage(
            portNum=self.port,
            baudRate=self.baud_rate,
            outputFileName=self.img_path,
        )
        if not ok or not os.path.exists(self.img_path):
            raise RuntimeError("The sensor did not return an image. Check the connection and try again.")
        return self.img_path

    def upload(self) -> dict:
        # Built before main_csv() (which turns Matric into a str), same as client.py
        data = {
            "ID": self.ID,
            "Name": self.Name,
            "Surname": self.Surname,
            "Matric": self.Matric,
            "Level": self.Level,
            "Dept": self.Dept,
        }
        with open(self.img_path, "rb") as img:
            resp = rq.post(
                url,
                data={"student_data": json.dumps(data)},
                files={"student_img": img},
                timeout=15,
            )
        resp.raise_for_status()

        # Server accepted it -> now record the student locally
        if self.main_csv() is not True:
            raise RuntimeError("Image uploaded, but writing DB.csv failed. Check Enrollment.log.")
        self.record.append(self.Matric)

        try:
            return resp.json()
        except ValueError:
            return {}


class EnrollmentApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Fingerprint enrollment")
        self.geometry("980x660")
        self.minsize(900, 620)
        self.configure(fg_color=("#e5e9f0", "#0b0d11"))

        self.msgs: queue.Queue = queue.Queue()   # worker threads -> UI
        self.mode = "idle"                       # idle | capturing | review | uploading
        self.session: EnrollmentSession | None = None
        self.entries: dict[str, ctk.CTkEntry] = {}

        self._blank = ctk.CTkImage(Image.new("RGBA", (1, 1), (0, 0, 0, 0)), size=(1, 1))
        self._build_ui()
        self._set_mode("idle")
        self._set_status("Fill in the student details, then capture a fingerprint.")
        self.after(100, self._poll_queue)

    # ------------------------------------------------------------------ UI -- #
    def _build_ui(self):
        self.grid_columnconfigure((0, 1), weight=1, uniform="cols")
        self.grid_rowconfigure(1, weight=1)

        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=28, pady=(22, 10))
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(header, text="Fingerprint enrollment",
                     font=ctk.CTkFont(size=26, weight="bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(header, text=f"Sensor on {PORT} at {BAUD_RATE} baud",
                     font=ctk.CTkFont(size=13), text_color=TEXT_MUTED).grid(row=1, column=0, sticky="w")
        self.theme_switch = ctk.CTkSwitch(header, text="Dark mode", command=self._toggle_theme,
                                          progress_color=ACCENT)
        self.theme_switch.select()
        self.theme_switch.grid(row=0, column=1, rowspan=2, sticky="e")

        # ---- Left card: student details ----
        left = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=18)
        left.grid(row=1, column=0, sticky="nsew", padx=(28, 12), pady=8)
        left.grid_columnconfigure((0, 1), weight=1, uniform="f")

        ctk.CTkLabel(left, text="Student details",
                     font=ctk.CTkFont(size=17, weight="bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", padx=24, pady=(22, 6))

        self._field(left, "ID", "Student ID", "e.g. 2", 1, 0)
        self._field(left, "Matric", "Matric number", f"{MATRIC_LEN} digits", 1, 1)
        self._field(left, "Name", "First name", "", 2, 0)
        self._field(left, "Surname", "Surname", "", 2, 1)
        self._field(left, "Dept", "Department", "e.g. Cyb", 3, 0)

        lvl_box = ctk.CTkFrame(left, fg_color="transparent")
        lvl_box.grid(row=3, column=1, sticky="ew", padx=24, pady=(8, 0))
        lvl_box.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(lvl_box, text="Level", font=ctk.CTkFont(size=12),
                     text_color=TEXT_MUTED).grid(row=0, column=0, sticky="w")
        self.level_menu = ctk.CTkOptionMenu(lvl_box, values=LEVELS, height=38, corner_radius=10,
                                            fg_color=BG_WELL, button_color=BG_WELL,
                                            button_hover_color=BG_WELL,
                                            text_color=("#111827", "#e5e7eb"),
                                            dropdown_fg_color=BG_CARD,
                                            dropdown_text_color=("#111827", "#e5e7eb"))
        self.level_menu.grid(row=1, column=0, sticky="ew", pady=(4, 0))
        self.level_menu.set(LEVELS[0])

        left.grid_rowconfigure(4, weight=1)
        btns = ctk.CTkFrame(left, fg_color="transparent")
        btns.grid(row=5, column=0, columnspan=2, sticky="ew", padx=24, pady=(0, 24))
        btns.grid_columnconfigure(0, weight=1)

        self.capture_btn = ctk.CTkButton(btns, text="Capture fingerprint", height=46, corner_radius=12,
                                         font=ctk.CTkFont(size=15, weight="bold"),
                                         fg_color=ACCENT, hover_color=ACCENT_HOVER,
                                         command=self._on_capture)
        self.capture_btn.grid(row=0, column=0, sticky="ew")
        self.clear_btn = ctk.CTkButton(btns, text="Clear form", height=36, corner_radius=12,
                                       fg_color="transparent", border_width=1,
                                       border_color=TEXT_MUTED, text_color=TEXT_MUTED,
                                       hover_color=BG_WELL, command=self._on_clear)
        self.clear_btn.grid(row=1, column=0, sticky="ew", pady=(10, 0))

        # ---- Right card: fingerprint preview ----
        right = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=18)
        right.grid(row=1, column=1, sticky="nsew", padx=(12, 28), pady=8)
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(right, text="Scan preview",
                     font=ctk.CTkFont(size=17, weight="bold")).grid(
            row=0, column=0, sticky="w", padx=24, pady=(22, 6))

        well = ctk.CTkFrame(right, fg_color=BG_WELL, corner_radius=14)
        well.grid(row=1, column=0, sticky="nsew", padx=24, pady=6)
        well.grid_propagate(False)
        well.grid_columnconfigure(0, weight=1)
        well.grid_rowconfigure(0, weight=1)
        self.preview = ctk.CTkLabel(well, text="", image=self._blank, compound="top",
                                    text_color=TEXT_MUTED, font=ctk.CTkFont(size=14))
        self.preview.grid(row=0, column=0)

        self.hint = ctk.CTkLabel(right, text="", text_color=TEXT_MUTED, font=ctk.CTkFont(size=12),
                                 wraplength=340, justify="left")
        self.hint.grid(row=2, column=0, sticky="w", padx=24, pady=(4, 0))

        rbtns = ctk.CTkFrame(right, fg_color="transparent")
        rbtns.grid(row=3, column=0, sticky="ew", padx=24, pady=(10, 24))
        rbtns.grid_columnconfigure((0, 1), weight=1, uniform="b")
        self.retake_btn = ctk.CTkButton(rbtns, text="Retake", height=44, corner_radius=12,
                                        fg_color=BG_WELL, hover_color=("#dde2ea", "#1f232c"),
                                        text_color=("#111827", "#e5e7eb"), command=self._on_retake)
        self.retake_btn.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        self.accept_btn = ctk.CTkButton(rbtns, text="Enroll student", height=44, corner_radius=12,
                                        font=ctk.CTkFont(size=14, weight="bold"),
                                        fg_color=ACCENT, hover_color=ACCENT_HOVER,
                                        command=self._on_accept)
        self.accept_btn.grid(row=0, column=1, sticky="ew", padx=(6, 0))

        # ---- Status bar ----
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.grid(row=2, column=0, columnspan=2, sticky="ew", padx=28, pady=(8, 18))
        bar.grid_columnconfigure(1, weight=1)
        self.dot = ctk.CTkLabel(bar, text="●", font=ctk.CTkFont(size=14), text_color=INFO, width=18)
        self.dot.grid(row=0, column=0)
        self.status = ctk.CTkLabel(bar, text="", anchor="w", font=ctk.CTkFont(size=13))
        self.status.grid(row=0, column=1, sticky="ew", padx=(6, 12))
        self.progress = ctk.CTkProgressBar(bar, width=180, height=6, mode="indeterminate",
                                           progress_color=ACCENT)
        self.progress.grid(row=0, column=2, sticky="e")
        self.progress.grid_remove()

        # keep the preview well a fixed size so the layout doesn't jump
        well.configure(width=PREVIEW_BOX[0] + 20, height=PREVIEW_BOX[1] + 20)

    def _field(self, parent, key, label, placeholder, row, col):
        box = ctk.CTkFrame(parent, fg_color="transparent")
        box.grid(row=row, column=col, sticky="ew", padx=24, pady=(8, 0))
        box.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(box, text=label, font=ctk.CTkFont(size=12),
                     text_color=TEXT_MUTED).grid(row=0, column=0, sticky="w")
        entry = ctk.CTkEntry(box, placeholder_text=placeholder, height=38, corner_radius=10,
                             fg_color=BG_WELL, border_width=1, border_color=BG_WELL)
        entry.grid(row=1, column=0, sticky="ew", pady=(4, 0))
        entry.default_border = BG_WELL
        self.entries[key] = entry

    # --------------------------------------------------------------- state -- #
    def _set_mode(self, mode: str):
        self.mode = mode
        form_on = "normal" if mode == "idle" else "disabled"
        for e in self.entries.values():
            e.configure(state=form_on)
        self.level_menu.configure(state=form_on)

        def on(flag):
            return "normal" if flag else "disabled"

        self.capture_btn.configure(state=on(mode == "idle"))
        self.clear_btn.configure(state=on(mode in ("idle", "review")))
        self.retake_btn.configure(state=on(mode == "review"))
        self.accept_btn.configure(state=on(mode == "review"))

        if mode in ("capturing", "uploading"):
            self.progress.grid()
            self.progress.start()
        else:
            self.progress.stop()
            self.progress.grid_remove()

    def _set_status(self, text: str, kind: str = "info"):
        colour = {"info": INFO, "busy": ACCENT, "ok": OK, "warn": WARN, "error": ERR}[kind]
        self.dot.configure(text_color=colour)
        self.status.configure(text=text)

    def _toggle_theme(self):
        ctk.set_appearance_mode("dark" if self.theme_switch.get() else "light")

    # ---------------------------------------------------------- validation -- #
    def _collect(self):
        """Return (values, error). Highlights offending fields."""
        for e in self.entries.values():
            e.configure(border_color=e.default_border)

        v = {k: e.get().strip() for k, e in self.entries.items()}
        v["Level"] = self.level_menu.get()

        problems = []
        if not v["ID"].isdigit():
            problems.append(("ID", "Student ID must be a whole number."))
        if not (v["Matric"].isdigit() and len(v["Matric"]) == MATRIC_LEN):
            problems.append(("Matric", f"Matric number must be exactly {MATRIC_LEN} digits."))
        for key, label in (("Name", "First name"), ("Surname", "Surname"), ("Dept", "Department")):
            if not v[key]:
                problems.append((key, f"{label} is required."))

        if problems:
            for key, _ in problems:
                self.entries[key].configure(border_color=ERR)
            return None, problems[0][1]
        return v, None

    @staticmethod
    def _already_enrolled(student_id: str, matric: str):
        path = os.path.join(cw_fldr, "DB.csv")
        if not os.path.exists(path):
            return None
        try:
            df = pd.read_csv(path, dtype=str)
        except Exception:
            return None
        df.columns = df.columns.str.strip()      # header is written as "ID " in client.py
        if "Matric" in df and matric in set(df["Matric"].astype(str).str.strip()):
            return "That matric number is already enrolled."
        if "ID" in df:
            ids = {s.strip().lstrip("0") or "0" for s in df["ID"].astype(str)}
            if (student_id.lstrip("0") or "0") in ids:
                return "That student ID is already in use."
        return None

    # ------------------------------------------------------------ actions --- #
    def _on_capture(self):
        values, error = self._collect()
        if error:
            return self._set_status(error, "error")
        dup = self._already_enrolled(values["ID"], values["Matric"])
        if dup:
            return self._set_status(dup, "error")

        self.session = EnrollmentSession(
            PORT, BAUD_RATE,
            int(values["ID"]), values["Name"], values["Surname"],
            int(values["Matric"]), values["Dept"], int(values["Level"]),
        )
        self._start_capture()

    def _on_retake(self):
        if self.session:
            self._start_capture()

    def _start_capture(self):
        self._show_placeholder("Waiting for finger…")
        self._set_mode("capturing")
        self._set_status("Place the finger on the sensor and hold still.", "busy")
        threading.Thread(target=self._capture_worker, args=(self.session,), daemon=True).start()

    def _on_accept(self):
        if not self.session:
            return
        self._set_mode("uploading")
        self._set_status("Uploading to the image server…", "busy")
        threading.Thread(target=self._upload_worker, args=(self.session,), daemon=True).start()

    def _on_clear(self):
        self._discard_image()
        self._reset_form()
        self._set_status("Form cleared.")

    # ------------------------------------------------------------- workers -- #
    def _capture_worker(self, session):
        try:
            self.msgs.put(("captured", session.capture()))
        except Exception as e:
            self.msgs.put(("capture_error", str(e)))

    def _upload_worker(self, session):
        try:
            self.msgs.put(("uploaded", session.upload()))
        except rq.ConnectionError:
            self.msgs.put(("upload_error", f"Can't reach the image server at {url}. Is it running?"))
        except rq.Timeout:
            self.msgs.put(("upload_error", "The image server took too long to respond."))
        except Exception as e:
            self.msgs.put(("upload_error", str(e)))

    def _poll_queue(self):
        try:
            while True:
                kind, payload = self.msgs.get_nowait()
                getattr(self, f"_on_{kind}")(payload)
        except queue.Empty:
            pass
        self.after(100, self._poll_queue)

    # ------------------------------------------------- worker -> UI handlers -- #
    def _on_captured(self, path):
        try:
            self._show_image(path)
        except Exception as e:
            self._discard_image()
            self._reset_form()
            return self._set_status(f"Captured, but the image couldn't be opened: {e}", "error")
        self.hint.configure(text="Check that the ridges are clear, centred and not smudged. "
                                 "Retake if in doubt.")
        self._set_mode("review")
        self._set_status("Scan captured. Review it, then enroll or retake.", "ok")

    def _on_capture_error(self, msg):
        self._discard_image()
        self._reset_form()
        self._set_status(msg, "error")

    def _on_uploaded(self, resp):
        who = f"{self.session.Name} {self.session.Surname}"
        self.session = None
        self._reset_form()
        self._set_status(f"{who} enrolled.", "ok")

    def _on_upload_error(self, msg):
        self._set_mode("review")          # scan is still there, the operator can retry
        self._set_status(f"Not enrolled: {msg}", "error")

    # ------------------------------------------------------------- helpers -- #
    def _show_image(self, path):
        with Image.open(path) as im:       # context manager releases the file lock (Windows)
            img = im.convert("RGB")
        w, h = img.size
        scale = min(PREVIEW_BOX[0] / w, PREVIEW_BOX[1] / h)
        size = (max(1, int(w * scale)), max(1, int(h * scale)))
        self._preview_img = ctk.CTkImage(img, size=size)   # keep a reference
        self.preview.configure(image=self._preview_img, text="")

    def _show_placeholder(self, text="No scan yet"):
        self.preview.configure(image=self._blank, text=text)
        self.hint.configure(text="")

    def _discard_image(self):
        """Delete the scan that was never enrolled."""
        path = getattr(self.session, "img_path", None)
        if path and os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass
        self.session = None

    def _reset_form(self):
        self._set_mode("idle")             # entries must be enabled before they can be cleared
        for e in self.entries.values():
            e.delete(0, "end")
            e.configure(border_color=e.default_border)
        self.level_menu.set(LEVELS[0])
        self._show_placeholder()


if __name__ == "__main__":
    EnrollmentApp().mainloop()
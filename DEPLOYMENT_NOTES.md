# AirBoard Deployment & Troubleshooting Notes

This document summarizes the deployment process, issues encountered, and solutions applied while preparing the AirBoard Virtual Gesture Keyboard for demonstration and distribution.

## 🚀 Deployment Goal
Convert the working Python project into a standalone `.exe` so it can run on any Windows machine without requiring Python or libraries to be installed.

## 🛠 Tools Used
- Python 3.x
- OpenCV
- cvzone (MediaPipe-based hand tracking)
- pynput (keyboard controller)
- PyInstaller (for .exe conversion)

---

## ✅ Initial Deployment Attempt
The project was packaged using:

```
pyinstaller --onefile --windowed main.py
```

This successfully generated an `.exe`, but running it caused errors.

---

## ❗ Issue #1 — Missing MediaPipe Model Files

### Error Output
```
FileNotFoundError: mediapipe/modules/hand_landmark/hand_landmark_tracking_cpu.binarypb
```

### Reason
MediaPipe uses external machine learning model files that PyInstaller does not automatically include.

### ✅ Solution
We located the MediaPipe installation path and manually added required resources during packaging:

```
pyinstaller --onefile --windowed ^
--add-data "C:/Users/user/PycharmProjects/PythonProject/.venv1/lib/site-packages/mediapipe/modules;mediapipe/modules" ^
main.py
```

This ensured the necessary `.binarypb` model files were packaged.

---

## ❗ Issue #2 — Cannot Rebuild `.exe`

### Error
```
PermissionError: [WinError 5] Access is denied: 'dist/main.exe'
```

### Cause
The previous `main.exe` was still running.

### ✅ Solution
- Closed the EXE window OR
- Used Task Manager → End Task → `main.exe`
- Re-ran PyInstaller

---

## ❗ Issue #3 — Typing Only Worked Inside App Window

Typing did not appear inside Notepad because we originally used:

```
keyboard_controller.type()
```

This sends text only to the active OpenCV window.

### ✅ Solution — Use Real Key Press Events

```
keyboard_controller.press(btn.text)
keyboard_controller.release(btn.text)
```

Now typing works in any application (Notepad, Chrome, Word, etc.).

---

## ❗ Issue #4 — AirBoard Window Disappeared When Switching to Notepad

To type in Notepad, users click another window — which made AirBoard go behind.

### ✅ Solution — Keep AirBoard Window Always On Top

```
cv2.namedWindow("AirBoard", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("AirBoard", cv2.WND_PROP_TOPMOST, 1)
```

This allowed:
- Notepad to stay active (receives typing)
- AirBoard to remain visible on top

---

## 🎯 Final Result
- The application runs correctly as `.exe`
- Gesture-based typing works globally
- UI remains visible during typing
- Deployment is stable for classroom/lab demonstration

---

## 💡 Key Learnings
| Challenge | Insight Gained |
|---------|----------------|
| Packaging ML models | Some dependencies require manual resource bundling |
| Windows file locking | Close executables before rebuilding |
| Global keyboard input | Use hardware-level key events instead of `.type()` |
| Multi-window workflows | Use `WND_PROP_TOPMOST` to maintain UI visibility |

---

End of Documentation ✅

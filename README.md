# 🔊 SoundListenerToARDUINO

SoundListenerToARDUINO bestaat uit **drie onderdelen** die samenwerken om audio‑activiteit in een browser‑tab om te zetten naar een signaal voor een Arduino.  
Wanneer de tab geluid afspeelt, stuurt de extensie een boolean naar Python, die dit doorstuurt naar de Arduino om hardware te activeren.

---

## 📦 Onderdelen

### 1️⃣ Browser‑extensie  
Detecteert of een specifieke tab audio afspeelt.  
Stuurt `"True"` of `"False"` via WebSockets naar de Python‑listener.

### 2️⃣ Python‑listener  
Ontvangt het signaal van de extensie, verwerkt het en stuurt het door naar de Arduino via de seriële poort.

### 3️⃣ Arduino‑code  
Ontvangt `"True"` of `"False"` via USB‑serial en voert een actie uit (bijv. LED, motor, relais).  
Je kunt de `.cpp` code uit deze repository **direct kopiëren en plakken in de Arduino IDE**.

---

## 🚀 Installatie & gebruik

### 🔧 1. Browser‑extensie installeren

1. Open Chrome of Edge  
2. Ga naar **Extensions**  
3. Zet **Developer Mode** aan  
4. Klik **Load unpacked**  
5. Selecteer de map `audioExtension2`

De extensie is nu actief en luistert naar audio in de tab.

---

### 🔌 2. Arduino voorbereiden

1. Sluit je Arduino aan via USB  
2. Open de meegeleverde `.cpp` file in de Arduino IDE  
3. Upload de sketch naar je Arduino  
4. Pas de code aan naar eigen voorkeur (LED, motor, relais, etc.)

De Arduino ontvangt `"True"` of `"False"` via de seriële verbinding.

---

### 🐍 3. Python‑listener starten

In de projectmap staat:

run.bat

Dubbelklik hierop. Het script:

- controleert of Python is geïnstalleerd  
- installeert automatisch de benodigde packages  
- start de listener via Main (`Main.py`)

Je hebt **geen PyCharm of IDE** nodig om het project te draaien.

---

## 📜 Dependencies

De Python‑kant gebruikt:
```text
websockets
pyserial
```

Deze worden automatisch geïnstalleerd via `run.bat`.

---

## 📂 Projectstructuur
```text
SoundListenerToARDUINO/
│
├── Listener.py
├── Main.py
├── requirements.txt
├── run.bat
│
├── audioExtension2/
│   ├── background.js
│   ├── content.js
│   ├── manifest.json
│
├── Arduino/
    ├── sound_listener.cpp   ← copy‑paste voor Arduino IDE
```


---

## 💡 Tips

- Zorg dat de extensie actief is in de tab die audio afspeelt  
- Start de Python‑listener voordat de Arduino signalen ontvangt  
- Gebruik `serial.tools.list_ports` om de juiste COM‑poort te vinden  
- Je kunt de Arduino‑code volledig aanpassen naar jouw hardware‑setup  

---

## 🛠 Arduino‑code

De Arduino‑code staat in de map `Arduino/`.  
Open het `.cpp` bestand in de Arduino IDE en upload het naar je board.  
Je kunt deze code direct gebruiken of aanpassen naar je eigen project.

---


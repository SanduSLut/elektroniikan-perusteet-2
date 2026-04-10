# Pommin purkaus -peli (Code)

Tämä repositorio sisältää projektin **Arduino + Python koodin**, joka ohjaa laitteen toimintaa.

---

## Sisältö

- Arduino-koodi (C++)
- Python käyttöliittymä (UI)
- Sarjaportin kautta toimiva kommunikaatio

---

## Python-asetukset (TÄRKEÄ)

Ennen ohjelman ajamista sinun täytyy muokata `main.py` tiedostoa:

### 1. COM-portti

Muokkaa oikea USB-portti:

```python
SERIAL_PORT = "COM3"

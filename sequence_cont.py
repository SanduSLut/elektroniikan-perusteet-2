

sequence = [
    ("msg", "Terminal started...", 0),
    ("msg", "Initializing system...", 200),
    ("msg", "Checking connections...", 650),
    ("msg", "Device detected!", 200),
    ("msg", "Loading modules...", 450),
    # Loading bar steps
    ("bar", 1, 220),
    ("bar", 8, 240),
    ("bar", 19, 300),
    ("bar", 23, 230),
    ("bar", 29, 200),
    ("bar", 36, 320),
    ("bar", 41, 200),
    ("bar", 49, 1100),
    ("bar", 50, 200),
    # ... continue until full
    ("msg", "Trying to decrypt incoming data...", 200),
    ("msg", "Decrypting key: 3F4A-9B2C", 500),
    ("msg", "Analyzing protocol packets...", 300),
    ("msg", "Checksum verified.", 200),
    ("msg", "Running pattern recognition...", 600),
    ("msg", "Re-calibrating sensors...", 200),
    ("msg", "Warning: minor anomalies detected.", 100),
]


correct_pot = [
    ("", 10),
    ("[DEBUG] Accessing encrypted sector...", 900),
    ("[INFO] Sector decryption key matched. Data integrity verified...", 2000),
    ("[DEBUG] Hash comparison successful. Payload decoded.", 300),
    ("[SUCCESS] Sequence unlocked. System stability normal.", 600),
]

correct_rgb = [
    ("", 10),
    ("[INFO] RGB input sequence verified: pattern match confirmed.", 1500),
    ("[SUCCESS] Signal alignment within expected parameters.", 900),
    ("[SYSTEM] Input accepted. Restoring normal operational flow.", 500),
    ("[DEBUG] Logging successful interaction for performance tracking.", 1000),
    ("************************************************************************", 50), 
    ("[STATUS] RGB MODULE SUCCESSFULLY COMPLETED", 50), 
    ("************************************************************************", 50), 
]

wrong_pot = [
    ("", 10),
    ("[WARNING] Potentiometer reading out of bounds: value mismatch detected.", 1500),
    ("[ERROR] Input validation failed. User response does not meet criteria.", 900),
    ("[ALERT] System flagged potential configuration error. Immediate review recommended.", 500),
    ("[DEBUG] Logging invalid attempt for audit trail and future diagnostics.", 1000),
    ("************************************************************************", 50), 
    ("[ALERT] !!! TWO MINUTES HAS BEEN REDUCED FROM THE TIMER !!!", 50), 
    ("************************************************************************", 50), 
]

wrong_rgb = [
    ("", 10),
    ("[WARNING] RGB input mismatch detected: invalid button sequence.", 1500),
    ("[ERROR] Signal pattern does not match expected profile response.", 900),
    ("[ALERT] Visual timer feedback compromised. Display integrity overridden.", 500),
    ("[DEBUG] Masking countdown output to prevent further user synchronization.", 1000),
    ("************************************************************************", 50), 
    ("[ALERT] !!! TIMER VISUAL HAS BEEN CORRUPTED: DISPLAY SHOWING XX:XX !!!", 50), 
    ("************************************************************************", 1800),
    ("", 10),
    ("FINAL TASK: Cut the correct wire!", 10),
]


device_info = [
    ("", 10),
    ("[INIT] Initializing administrative interface...", 700),
    ("[LINK] Connecting to device bus on /dev/ttyUSB0...", 900),
    ("[SCAN] Scanning for connected objects...", 1200),
    ("[SCAN] Device signature detected. Resolving identity...", 1200),
    ("[VERIFY] Certificate chain validation... OK", 600),
    ("[VERIFY] Firmware checksum verified... OK", 600),
    ("[CRYPT] Negotiating encryption protocol... AES-256-GCM", 500),
    ("[CRYPT] Secure tunnel established.", 600),
    ("[SYNC] Retrieving device metadata...", 1100),
    ("[DEBUG] Parsing response buffer...", 400)
]

profile1 = [
    ("************************************************************************", 50),
    ("[DEVICE] ID: 01A23B9F", 50),
    ("[DEVICE] MODEL: EX-1200 Rev.B", 50),
    ("[DEVICE] SERIAL: SN-8842-91XZ", 50),
    ("[DEVICE] HASH: A9F3-22BC-77D1", 50),
    ("[DEVICE] MANUFACTURER: NexaCore Systems", 50),
    ("[DEVICE] FIRMWARE: v3.4.7", 50),
    ("[DEVICE] STATUS: CONNECTED (SECURE)", 50),
    ("************************************************************************", 50),
    ("[COMPLETE] Operation finished successfully.", 700),
]


profile2 = [
    ("************************************************************************", 50),
    ("[DEVICE] ID: 02B56T4K", 50),
    ("[DEVICE] MODEL: DDEF-3000 Model X", 50),
    ("[DEVICE] SERIAL: SN-9932-77QW", 50),
    ("[DEVICE] HASH: B4D7-11AC-55F3", 50),
    ("[DEVICE] MANUFACTURER: QuantumTech Labs", 50),
    ("[DEVICE] FIRMWARE: v2.9.1", 50),
    ("[DEVICE] STATUS: CONNECTED (SECURE)", 50),
    ("************************************************************************", 50),
    ("[COMPLETE] Operation finished successfully.", 700),
]


profile3 = [
    ("************************************************************************", 50),
    ("[DEVICE] ID: 03C88M7L", 50),
    ("[DEVICE] MODEL: ZX-900 Pro", 50),
    ("[DEVICE] SERIAL: SN-4481-XX98", 50),
    ("[DEVICE] HASH: C7E1-44BC-88D2", 50),
    ("[DEVICE] MANUFACTURER: NexaCore Systems", 50),
    ("[DEVICE] FIRMWARE: v4.0.3", 50),
    ("[DEVICE] STATUS: CONNECTED (SECURE)", 50),
    ("************************************************************************", 50),
    ("[COMPLETE] Operation finished successfully.", 700),
]
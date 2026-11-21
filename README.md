# Blockchain-Based Secure Communication Framework

A secure communication framework that protects messages with a custom blockchain and encryption, and monitors IoT devices through a security gateway that scores trust and blocks risky devices.

## About the Project

Connected devices such as medical devices and security cameras can be tampered with or impersonated, and a single compromised device can put the whole network at risk. This project addresses that in two ways.

**1. Tamper-proof messaging.** Messages are stored in a custom blockchain. Each block is linked using SHA-256 hashing and secured with proof-of-work, so changing any past message breaks the chain and is detected. Messages are encrypted with RSA and AES, and sender authentication checks that a message really came from the claimed sender, so tampering is detected in real time.

**2. Device trust monitoring.** The CyberGuard Gateway dashboard watches a fleet of devices and gives each one a trust score based on accuracy, stability and latency. Devices are classified as Normal, Suspicious, Probation or Blocked, and high-risk devices are isolated automatically.

## Features
- Custom blockchain with SHA-256 hashing and proof-of-work
- RSA and AES encryption for message confidentiality
- Sender authentication to verify who sent each message
- Real-time detection of tampered messages
- Live dashboard with a fleet overview (total, authorized, suspicious and blocked devices)
- Per-device trust score built from accuracy, stability and latency
- Security states (Normal, Suspicious, Probation, Blocked) with automatic blocking of high-risk devices

## Screenshots
![CyberGuard Gateway Dashboard](screenshots/dashboard.png)

## Tech Stack
Python, Flask, RSA/AES encryption, SHA-256, HTML/CSS/JavaScript

## Project Structure
```
├── main file(s)        application code
├── templates/          dashboard pages (if using Flask)
├── static/             CSS and JavaScript
├── requirements.txt    Python libraries
└── screenshots/        dashboard images
```

## Installation
1. Install Python 3.8 or newer
2. Clone the repository:
   `git clone https://github.com/vasanthi1136/blockchain-secure-communication-framework.git`
3. Go into the folder:
   `cd blockchain-secure-communication-framework`
4. Install the libraries:
   `pip install -r requirements.txt`
5. Start the application:
   `python app.py`
6. Open `http://127.0.0.1:5000` in your browser

## How It Works
1. A message is created and encrypted with AES, and the AES key is protected with RSA.
2. The message is added to a block, and the block is hashed with SHA-256.
3. Proof-of-work is completed before the block is added to the chain.
4. The receiver verifies the sender and the hash chain. Any mismatch is flagged as tampering.
5. On the dashboard, each device's trust score is calculated from accuracy, stability and latency. Low-scoring devices are marked High Risk and blocked.

## Future Improvements
- Connect real IoT devices instead of simulated ones
- Add user login for the dashboard
- Store the blockchain in a database

## Author
**Namala Vasanthi**

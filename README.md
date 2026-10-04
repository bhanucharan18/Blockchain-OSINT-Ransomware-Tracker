# Blockchain OSINT Ransomware Tracker

A Python-based security research project for investigating suspicious cryptocurrency wallets and following potential ransomware payment trails.

The idea behind this project is simple: **cryptocurrency transactions are public, but following the money across multiple wallets can become difficult very quickly.** This project combines blockchain data, known ransomware wallet information, graph-based transaction tracing, OSINT correlation, and risk scoring to make that investigation easier to understand.

---

## What does this project do?

The Blockchain OSINT Ransomware Tracker takes a cryptocurrency wallet address and attempts to build an investigation around it.

The tool can:

1.Identify whether an address looks like a Bitcoin or Ethereum address
2.Retrieve Bitcoin transaction information through the BlockCypher API
3.Check wallets against a small database of known ransomware-associated addresses
4.Trace relationships between wallets using a directed graph
5.Calculate the number of hops between wallets
6.Identify simulated mixer-related paths
7.Correlate wallet information with predefined OSINT/dark-web references
8.Assign a basic risk score based on multiple indicators
9.Visualize wallet relationships using NetworkX and Matplotlib
10.Export investigation information as JSON

The purpose is not to say *"this wallet belongs to an attacker"* based on one indicator. Instead, the project demonstrates how several pieces of information can be combined to support a blockchain investigation.

---

## Why I built it

Ransomware investigations often involve more than finding the initial payment address.

Once cryptocurrency is received, funds can move through intermediate wallets, aggregation addresses, split transactions, mixers, and other services. Looking at individual transactions one by one makes these relationships difficult to understand.

I built this project to experiment with a more investigation-oriented workflow:

```text
Wallet Address
      ↓
Blockchain Data
      ↓
Transaction History
      ↓
Known Ransomware Checks
      ↓
Wallet-to-Wallet Relationships
      ↓
Graph / Hop Analysis
      ↓
OSINT Correlation
      ↓
Risk Score
      ↓
Investigation Report
```

---

## Main Features

### 1. Wallet and cryptocurrency identification

The application accepts a wallet address and performs a basic format check.

Currently, the interface recognizes common:

1.Bitcoin addresses
2.Ethereum addresses

The application then uses the detected type to decide how the address should be handled.

---

### 2. Blockchain transaction lookup

For Bitcoin addresses, the project uses the **BlockCypher API** to retrieve blockchain transaction information.

The current implementation extracts information such as:

1. Transaction hash
2.Transaction amount
3.Confirmations
4.Transaction history

This gives the investigation a starting point based on publicly available blockchain data.

---

### 3. Known ransomware wallet database

The project contains a small local database of ransomware-associated wallet addresses.

The current database includes example entries associated with:

1.WannaCry
2.Locky
3.REvil

A wallet is compared against this database before being given a ransomware match.

This is intentionally treated as an **indicator**, not as conclusive attribution.

---

### 4. Transaction graph analysis

One of the main parts of the project is representing wallet movement as a graph.

Each wallet is treated as a node, while a transaction or transfer relationship is represented as an edge.

For example:

```text
Victim Wallet
     │
     ▼
Ransom Wallet
     │
     ▼
Intermediate Wallet
     │
     ▼
Aggregator
    / \
   /   \
  ▼     ▼
Split A Split B
   \     /
    \   /
      ▼
     Mixer
      │
      ▼
Attacker Storage
```

The project uses **NetworkX** to create and analyze these relationships.

The graph tracker also calculates the shortest path between a source and target wallet and reports the number of hops involved.

---

### 5. Mixer detection

The project includes a basic mixer detection mechanism.

During graph analysis, wallet paths containing a node identified as a mixer are flagged.

For example:

```text
Ransom Wallet
      ↓
Intermediate Wallet
      ↓
Aggregator
      ↓
Mixer
      ↓
Final Wallet
```

A mixer indicator contributes to the overall risk score.

> This is a simplified research implementation. Real-world mixer identification requires much richer blockchain heuristics and external intelligence.

---

### 6. OSINT / dark-web correlation

Blockchain information becomes more useful when it can be correlated with information from other sources.

The project includes a simple OSINT correlation layer that can associate a wallet with a predefined intelligence reference.

For example:

```text
Wallet Address
      ↓
OSINT Check
      ↓
Known ransomware-related reference
      ↓
Correlation result
```

This demonstrates how blockchain investigation can be combined with threat intelligence rather than relying only on transaction data.

---

### 7. Risk scoring

The project includes a basic scoring mechanism to combine multiple indicators.

The current model considers factors such as:

| Indicator                  | Score |
| -------------------------- | ----: |
| Ransomware wallet match    |   +40 |
| 3 or more transaction hops |   +20 |
| Mixer detected             |   +25 |
| Dark-web/OSINT mention     |   +15 |

The final score is capped at 100.

Conceptually:

```text
Risk Score =
    Ransomware Match
  + Hop Analysis
  + Mixer Indicator
  + OSINT Correlation
```

This is intended as a prioritization mechanism for investigation, **not as a machine-learning prediction or legal attribution system**.

---

## Example Investigation

A simulated transaction trail is included in the project so that the graph-analysis functionality can be tested without relying on real criminal transactions.

The example follows a path similar to:

```text
Victim Wallet
      ↓
Ransom Address
      ↓
Intermediate Wallet
      ↓
Aggregator Wallet
      ↓
   ┌──┴──┐
   ↓     ↓
Split A Split B
   └──┬──┘
      ↓
Mixer Entry
      ↓
Attacker Cold Storage
```

This makes it easier to understand how funds can move through multiple addresses and why graph analysis is useful during an investigation.

---

## Project Structure

```text
Blockchain-OSINT-Ransomware-Tracker/
│
├── main.py
├── blockchain_api.py
├── ransomware_db.py
├── graph_function.py
├── correlation_reporting.py
├── enhancements.py
├── simulation_trail.py
├── required_packages.py
├── Untitled-1.ipynb
└── README.md
```

### `main.py`

Main desktop application.

It provides the Tkinter interface where a user can enter a wallet address, start the analysis, view logs, and display the transaction graph.

### `blockchain_api.py`

Handles blockchain API communication and wallet-related checks.

It currently uses the BlockCypher Bitcoin API to retrieve wallet transaction data.

### `ransomware_db.py`

Contains the local list of known ransomware-associated wallet addresses used for matching.

### `graph_function.py`

Builds a directed NetworkX graph from transaction relationships and calculates paths and hop counts.

### `correlation_reporting.py`

Contains the OSINT correlation, graph visualization, and JSON report functionality.

### `enhancements.py`

Contains additional investigation logic such as:

* Risk scoring
* Mixer detection

### `simulation_trail.py`

Contains a simulated blockchain transaction trail used for testing graph tracing without depending on a real investigation.

### `required_packages.py`

Contains the Python modules used by the project, including:

1.Tkinter
2.NetworkX
3.Matplotlib
4.ttkbootstrap
5.Web browser utilities

### `Untitled-1.ipynb`

Notebook used during the project's development and experimentation.

---

## Technologies Used

1.**Python**
2.**Tkinter** – desktop GUI
3.**NetworkX** – graph and path analysis
4.**Matplotlib** – transaction graph visualization
5.**Requests** – API communication
6.**BlockCypher API** – Bitcoin blockchain data
7.**JSON** – investigation report output
8.**OSINT concepts** – intelligence correlation
9.**Blockchain analysis** – transaction tracing

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/bhanucharan18/Blockchain-OSINT-Ransomware-Tracker.git
cd Blockchain-OSINT-Ransomware-Tracker
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the dependencies

Install the required Python packages:

```bash
pip install requests networkx matplotlib ttkbootstrap
```

Tkinter is normally included with standard Python installations on Windows. On some Linux distributions, it may need to be installed separately.

### 4. Run the application

```bash
python main.py
```

The graphical interface should open.

---

## Basic Usage

1. Start the application.
2. Enter a Bitcoin wallet address.
3. Click **Start AML Trace**.
4. The application performs the basic wallet and reputation checks.
5. Blockchain transaction information is retrieved where supported.
6. Wallet relationships can be represented as a graph.
7. The investigation logic checks for ransomware, mixer, and OSINT indicators.
8. The resulting information can be used to understand the possible transaction trail.

For initial testing, the application contains a Bitcoin example address in the interface.

---

## How the investigation logic works

The project follows a simple layered approach.

### Layer 1 — Address validation

The wallet format is checked to determine whether it resembles a supported cryptocurrency address.

### Layer 2 — Blockchain information

Transaction information is retrieved for supported Bitcoin addresses.

### Layer 3 — Known indicators

The wallet is compared against the project's known ransomware wallet database.

### Layer 4 — Relationship analysis

Wallet relationships are converted into a directed graph.

### Layer 5 — Path analysis

The graph is searched for paths between source and destination wallets.

### Layer 6 — OSINT correlation

Additional predefined intelligence information is checked against the wallet.

### Layer 7 — Risk calculation

The available indicators are combined into a simple risk score.

This gives the investigator a single workflow instead of looking at each piece of information separately.

---

## Important limitation

This project is a **research and educational prototype**.

A ransomware wallet match, a transaction path, a mixer indicator, or an OSINT mention should not by itself be treated as proof that a specific person or organization is responsible for a crime.

Real blockchain investigations normally require additional evidence, such as:

1.Larger and continuously updated wallet datasets
2.Blockchain clustering techniques
3.Exchange intelligence
4.Transaction timing analysis
5.Address reuse analysis
6.Entity attribution
7.Threat intelligence feeds
8.Dark-web intelligence
9.Law-enforcement or exchange records
10.Manual investigation and verification

The current ransomware database and OSINT data are intentionally small examples for demonstrating the concept.

---

## What I learned from this project

Building this project helped me understand how different areas of cybersecurity can work together.

The main concepts I worked with were:

1.Blockchain transaction analysis
2.Cryptocurrency wallets
3.OSINT
4.Ransomware investigations
5.Graph theory
6.Shortest-path analysis
7.Threat intelligence correlation
8.Risk scoring
9.Security-focused data visualization
10.Python automation

One of the biggest lessons was that **following a cryptocurrency transaction is not the same as identifying an attacker**. The blockchain can show how funds move between addresses, but attribution requires additional intelligence and evidence.

---

## Future Improvements

There are several areas where I would like to take the project further:

1.Add support for more blockchain networks
2.Integrate larger ransomware wallet datasets
3.Connect to live threat-intelligence feeds
4.Improve wallet clustering
5.Add transaction timeline analysis
6.Detect more sophisticated mixer patterns
7.Add exchange and service identification
8.Improve OSINT source correlation
9.Generate detailed investigation reports
10.Add interactive graph exploration
11.Store investigation cases in a database
12.Add stronger evidence and confidence scoring
13.Build a web-based investigation dashboard

---

## Disclaimer

This project is intended for **educational, cybersecurity research, and authorized investigation purposes only**.

Do not use it to harass, identify, or accuse individuals based solely on blockchain addresses or automated results.

Always independently verify intelligence before making investigative or security decisions.

---

## Author

**Bhanu Charan Dappu**

Cybersecurity enthusiast interested in:

* Security Operations
* Digital Forensics
* Threat Intelligence
* OSINT
* Blockchain Security
* Incident Response

GitHub: [@bhanucharan18](https://github.com/bhanucharan18)

---

## License

This project is provided for educational and research purposes. Add an explicit open-source license to the repository if you intend to permit reuse, modification, and redistribution.

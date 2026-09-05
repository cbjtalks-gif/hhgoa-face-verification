# hhgoa-face-verification



\# 🛡️ Biometric Face Identification \& Polygon Amoy Attestation Pipeline

> \*\*Hacker House Goa 2026 - Task #3 Prototype\*\*



An end-to-end decentralized biometric verification protocol that captures facial biometrics, extracts cryptographically secure feature hashes, discovers associated OSINT web identities, and permanently notarizes the record onto the \*\*Polygon Amoy Testnet\*\* via an EVM smart contract.



\---



\## ⚡ Key Highlights \& Architecture



1\. \*\*Biometric Extraction \& Matching:\*\* Crops region-of-interest (ROI) face vectors, evaluates similarity thresholds against recognized entities, and generates SHA-256 image hashes.

2\. \*\*OSINT Identity Discovery:\*\* Correlates verified physical identities with public online footprints (X/Twitter, Web OSINT).

3\. \*\*Composite Fingerprint:\*\* Binds biometric hashes, identity names, and social URLs into an immutable cryptographic payload:

&#x20;  $$\\text{Composite Hash} = \\text{SHA-256}(\\text{FaceHash} \\parallel \\text{PostURL} \\parallel \\text{SubjectName})$$

4\. \*\*On-Chain Smart Contract Notarization:\*\* Deployed to Polygon Amoy EVM network. Writes state via `registerRecord()` and verifies integrity via `verifyRecord()`.



\---



\## 🔗 Live On-Chain Deployments (Polygon Amoy - Chain ID 80002)



| Component | Value / Link |

|---|---|

| \*\*Smart Contract Address\*\* | \[`0x3e522c318A239d7eD818803217a35023596123EE`](https://amoy.polygonscan.com/address/0x3e522c318A239d7eD818803217a35023596123EE) |

| \*\*Proof Registration Tx\*\* | \[`0xc5d8d03cc51aa1bbeb11ae0cbc9ac81147e7ed667b934405a53bd15dfa360a9f`](https://amoy.polygonscan.com/tx/0xc5d8d03cc51aa1bbeb11ae0cbc9ac81147e7ed667b934405a53bd15dfa360a9f) |

| \*\*Block Number\*\* | `46794363` |

| \*\*Integrity State\*\* | `VERIFIED / NOTARIZED ON-CHAIN` |



\---



\## 🚀 Setup \& Execution



\### 1. Installation

```bash

git clone \[https://github.com/cbjtalks-gif/hhgoa-face-verification.git](https://github.com/cbjtalks-gif/hhgoa-face-verification.git)

cd hhgoa-face-verification

python -m venv venv

venv\\Scripts\\activate

pip install -r requirements.txt


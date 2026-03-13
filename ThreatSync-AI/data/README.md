# ThreatSync AI - CVE Sample Dataset

## Overview
This directory contains sample CVE (Common Vulnerabilities and Exposures) data for building the ThreatSync AI capstone project.

## Files

### `sample_cves_10.json`
- 10 high-profile CVEs from 2023-2024
- Includes: Microsoft Outlook RCE, XZ Utils backdoor, HTTP/2 Rapid Reset, Fortinet RCE
- Good for initial testing and demos

### `full_cves_100.json` (To be generated)
- 100 real CVEs from NVD
- Mix of vendors: Microsoft, Apache, Fortinet, VMware, Cisco, AWS, Adobe
- Mix of severity: Critical (40%), High (40%), Medium (20%)
- Mix of types: RCE, Auth Bypass, SQL Injection, XSS, DoS, Privilege Escalation

## Data Structure

Each CVE has the following fields:
```json
{
  "cve_id": "CVE-YYYY-NNNNN",
  "description": "Detailed vulnerability description",
  "cvss_score": 9.8,
  "cvss_severity": "CRITICAL",
  "cvss_vector": "CVSS:3.1/AV:N/AC:L/...",
  "published_date": "YYYY-MM-DD",
  "affected_products": ["Product 1", "Product 2"],
  "vulnerability_type": "Remote Code Execution",
  "cwe": "CWE-XXX: Description",
  "exploit_available": true/false,
  "exploit_maturity": "Active Exploitation|Proof of Concept|Not Available",
  "references": ["URL1", "URL2"],
  "patch_available": true/false,
  "patch_date": "YYYY-MM-DD",
  "vendor_advisory": "Advisory reference"
}
```

## Usage in LangFlow

### Option 1: Load from JSON
1. Use File Loader component
2. Point to `sample_cves_10.json` or `full_cves_100.json`
3. Parse JSON with Text Splitter
4. Embed with OpenAI Embeddings
5. Store in ChromaDB

### Option 2: Manual Import
1. Copy CVE data
2. Create Documents in LangFlow
3. Embed and store

## Extending the Dataset

To add more CVEs:
1. Visit NVD: https://nvd.nist.gov/
2. Search for recent CVEs
3. Extract data using NVD API or manual copy
4. Add to JSON following the structure above

## License
CVE data is public domain (from NVD).
This dataset is for educational purposes (capstone project).

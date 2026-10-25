# 50+ Industry Benchmark Financial Datasets
## Profit Predictor & Enterprise CFO Operating System

This archive contains 55+ benchmark datasets spanning 10 global super-sectors and 50+ specialized industries, along with the standard startup reference datasets.

### Super-Sectors Included:
1. **Technology & SaaS** (B2B SaaS, Cloud AI & MLOps, Cybersecurity, Consumer Mobile, Fintech Payments, Web3 Infrastructure, EdTech, Gaming Studios, PropTech, HRTech)
2. **Retail & E-Commerce** (D2C Fashion, Beauty & Personal Care, Consumer Electronics, Luxury Goods, B2B Wholesale)
3. **Healthcare & Life Sciences** (Biotech Therapeutics, Medical Devices, Telehealth, Specialty Pharmaceuticals, HealthTech SaaS)
4. **Industrial & Manufacturing** (Electric Vehicles, Semiconductor Foundry, Industrial Robotics, Aerospace & Defense, Specialty Chemicals)
5. **Financial Services** (Digital Neobanking, InsurTech, Quantitative Asset Management, Microfinance & Lending, Algorithmic Trading)
6. **CleanTech & Energy** (Solar & Renewable Power, Grid Battery Storage, Carbon Accounting & Climate SaaS, EV Charging Infra, Circular Recycling)
7. **Logistics & Supply Chain** (Autonomous Fleet Logistics, Quick Commerce, Cold Chain Storage, 3PL Fulfillment, Freight Intelligence)
8. **Consulting & Professional Services** (IT Systems Integration, Management Consulting, Digital Growth Agencies, LegalTech AI, Creative Studios)
9. **Media & Consumer Tech** (OTT Streaming, Interactive Gaming, Fitness & Wellness Tech, TravelTech)
10. **Frontier & Deep Tech** (Quantum Computing, SpaceTech & Satellites, Synthetic Biology, Vertical AgriTech)

### Schema:
Every dataset contains:
- `Company_ID`: Unique enterprise identifier
- `Company_Name`: Synthetic enterprise name
- `R&D_Spend`: Research & Development budget in INR (₹)
- `Administration`: Administrative and operational overhead in INR (₹)
- `Marketing_Spend`: Marketing, customer acquisition, and branding spend in INR (₹)
- `State`: Operating region (California, New York, Florida, Texas, etc.)
- `Profit`: Resulting net profit in INR (₹)
- `Revenue`: Calibrated gross revenue
- `Gross_Margin`: Sector-specific gross margin
- `Sector`: Industry subsector classification

### Usage:
- Open directly in Microsoft Excel, Google Sheets, or Python Pandas:
  ```python
  import pandas as pd
  df = pd.read_csv("b2b_saas.csv")
  print(df.head())
  ```
- Use directly in the Streamlit app under **Tab 7 (Batch Scoring Studio)** or calibrate in **Tab 8 (Model Governance & 50 Datasets)**.

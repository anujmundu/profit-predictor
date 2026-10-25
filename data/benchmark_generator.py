import json
import logging
from pathlib import Path
from typing import Dict, List, Any
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

BASE_DIR = Path(__file__).resolve().parent.parent
BENCHMARKS_DIR = BASE_DIR / "data" / "benchmarks"

# 50 Industry Sector Profiles across 10 Super-Sectors
SECTOR_PROFILES: List[Dict[str, Any]] = [
    # 1. Tech & Software (10)
    {"slug": "b2b_saas", "name": "B2B Enterprise SaaS", "super_sector": "Technology", "gross_margin": 0.78, "rnd_ratio": 0.28, "mktg_ratio": 0.32, "admin_ratio": 0.12, "base_rev": 2500000},
    {"slug": "cloud_ai_mlops", "name": "Cloud AI & MLOps Infrastructure", "super_sector": "Technology", "gross_margin": 0.72, "rnd_ratio": 0.38, "mktg_ratio": 0.22, "admin_ratio": 0.10, "base_rev": 3000000},
    {"slug": "cybersecurity", "name": "Cybersecurity & Identity", "super_sector": "Technology", "gross_margin": 0.82, "rnd_ratio": 0.26, "mktg_ratio": 0.34, "admin_ratio": 0.11, "base_rev": 2800000},
    {"slug": "consumer_mobile_apps", "name": "Consumer Mobile & Social Apps", "super_sector": "Technology", "gross_margin": 0.68, "rnd_ratio": 0.18, "mktg_ratio": 0.45, "admin_ratio": 0.09, "base_rev": 1800000},
    {"slug": "fintech_payments", "name": "Fintech & Payment Gateways", "super_sector": "Technology", "gross_margin": 0.65, "rnd_ratio": 0.24, "mktg_ratio": 0.25, "admin_ratio": 0.16, "base_rev": 3500000},
    {"slug": "web3_crypto_infra", "name": "Web3 & Blockchain Infrastructure", "super_sector": "Technology", "gross_margin": 0.75, "rnd_ratio": 0.40, "mktg_ratio": 0.20, "admin_ratio": 0.12, "base_rev": 2200000},
    {"slug": "edtech", "name": "EdTech & Corporate Learning", "super_sector": "Technology", "gross_margin": 0.62, "rnd_ratio": 0.16, "mktg_ratio": 0.38, "admin_ratio": 0.12, "base_rev": 1500000},
    {"slug": "gaming_studios", "name": "Gaming Studios & Interactive", "super_sector": "Technology", "gross_margin": 0.70, "rnd_ratio": 0.32, "mktg_ratio": 0.30, "admin_ratio": 0.10, "base_rev": 2400000},
    {"slug": "proptech", "name": "PropTech & Real Estate SaaS", "super_sector": "Technology", "gross_margin": 0.66, "rnd_ratio": 0.19, "mktg_ratio": 0.33, "admin_ratio": 0.13, "base_rev": 1900000},
    {"slug": "hrtech_workforce", "name": "HRTech & WorkOS Platforms", "super_sector": "Technology", "gross_margin": 0.76, "rnd_ratio": 0.22, "mktg_ratio": 0.35, "admin_ratio": 0.11, "base_rev": 2100000},

    # 2. E-Commerce & Retail (5)
    {"slug": "d2c_fashion", "name": "D2C Fashion & Apparel", "super_sector": "Retail & E-Commerce", "gross_margin": 0.52, "rnd_ratio": 0.05, "mktg_ratio": 0.36, "admin_ratio": 0.08, "base_rev": 1600000},
    {"slug": "beauty_personal_care", "name": "Beauty & Personal Care", "super_sector": "Retail & E-Commerce", "gross_margin": 0.65, "rnd_ratio": 0.07, "mktg_ratio": 0.40, "admin_ratio": 0.08, "base_rev": 1400000},
    {"slug": "electronics_retail", "name": "Consumer Electronics Retail", "super_sector": "Retail & E-Commerce", "gross_margin": 0.32, "rnd_ratio": 0.04, "mktg_ratio": 0.18, "admin_ratio": 0.06, "base_rev": 4200000},
    {"slug": "luxury_goods", "name": "Luxury Consumer Goods", "super_sector": "Retail & E-Commerce", "gross_margin": 0.72, "rnd_ratio": 0.08, "mktg_ratio": 0.35, "admin_ratio": 0.12, "base_rev": 2600000},
    {"slug": "b2b_wholesale", "name": "B2B Wholesale Marketplaces", "super_sector": "Retail & E-Commerce", "gross_margin": 0.28, "rnd_ratio": 0.08, "mktg_ratio": 0.12, "admin_ratio": 0.05, "base_rev": 5500000},

    # 3. Healthcare & Life Sciences (5)
    {"slug": "biotech_therapeutics", "name": "Biotech Therapeutics & Genomics", "super_sector": "Healthcare", "gross_margin": 0.85, "rnd_ratio": 0.55, "mktg_ratio": 0.10, "admin_ratio": 0.14, "base_rev": 3800000},
    {"slug": "medical_devices", "name": "Medical Devices & Diagnostic Tools", "super_sector": "Healthcare", "gross_margin": 0.68, "rnd_ratio": 0.22, "mktg_ratio": 0.24, "admin_ratio": 0.12, "base_rev": 2900000},
    {"slug": "telehealth_digital_health", "name": "Telehealth & Digital Clinics", "super_sector": "Healthcare", "gross_margin": 0.58, "rnd_ratio": 0.15, "mktg_ratio": 0.30, "admin_ratio": 0.13, "base_rev": 1700000},
    {"slug": "specialty_pharma", "name": "Specialty Pharmaceuticals", "super_sector": "Healthcare", "gross_margin": 0.78, "rnd_ratio": 0.35, "mktg_ratio": 0.25, "admin_ratio": 0.10, "base_rev": 4800000},
    {"slug": "healthtech_saas", "name": "HealthTech EHR & Hospital SaaS", "super_sector": "Healthcare", "gross_margin": 0.74, "rnd_ratio": 0.25, "mktg_ratio": 0.28, "admin_ratio": 0.12, "base_rev": 2300000},

    # 4. Manufacturing & Industrial (5)
    {"slug": "ev_automotive", "name": "Electric Vehicles & Smart Mobility", "super_sector": "Industrial & Manufacturing", "gross_margin": 0.22, "rnd_ratio": 0.15, "mktg_ratio": 0.08, "admin_ratio": 0.05, "base_rev": 8500000},
    {"slug": "semiconductor_fab", "name": "Semiconductor Design & Foundry", "super_sector": "Industrial & Manufacturing", "gross_margin": 0.48, "rnd_ratio": 0.24, "mktg_ratio": 0.06, "admin_ratio": 0.06, "base_rev": 7200000},
    {"slug": "industrial_robotics", "name": "Industrial Robotics & Automation", "super_sector": "Industrial & Manufacturing", "gross_margin": 0.45, "rnd_ratio": 0.20, "mktg_ratio": 0.12, "admin_ratio": 0.07, "base_rev": 3600000},
    {"slug": "aerospace_defense", "name": "Aerospace & Defense Systems", "super_sector": "Industrial & Manufacturing", "gross_margin": 0.35, "rnd_ratio": 0.18, "mktg_ratio": 0.05, "admin_ratio": 0.08, "base_rev": 9200000},
    {"slug": "specialty_chemicals", "name": "Specialty Chemicals & Polymers", "super_sector": "Industrial & Manufacturing", "gross_margin": 0.38, "rnd_ratio": 0.10, "mktg_ratio": 0.09, "admin_ratio": 0.06, "base_rev": 5000000},

    # 5. Financial Services (5)
    {"slug": "neobanking", "name": "Digital Neobanking & Wallets", "super_sector": "Financial Services", "gross_margin": 0.60, "rnd_ratio": 0.25, "mktg_ratio": 0.28, "admin_ratio": 0.15, "base_rev": 3200000},
    {"slug": "insurtech", "name": "InsurTech & Automated Underwriting", "super_sector": "Financial Services", "gross_margin": 0.54, "rnd_ratio": 0.20, "mktg_ratio": 0.26, "admin_ratio": 0.14, "base_rev": 2700000},
    {"slug": "asset_management", "name": "Quantitative Asset Management", "super_sector": "Financial Services", "gross_margin": 0.85, "rnd_ratio": 0.15, "mktg_ratio": 0.15, "admin_ratio": 0.20, "base_rev": 4500000},
    {"slug": "digital_lending", "name": "Microfinance & Digital Lending", "super_sector": "Financial Services", "gross_margin": 0.48, "rnd_ratio": 0.14, "mktg_ratio": 0.22, "admin_ratio": 0.12, "base_rev": 3100000},
    {"slug": "algorithmic_trading", "name": "Algorithmic Trading & Market Making", "super_sector": "Financial Services", "gross_margin": 0.90, "rnd_ratio": 0.35, "mktg_ratio": 0.05, "admin_ratio": 0.15, "base_rev": 6000000},

    # 6. CleanTech & Energy (5)
    {"slug": "solar_renewables", "name": "Solar & Renewable Power EPC", "super_sector": "CleanTech & Energy", "gross_margin": 0.30, "rnd_ratio": 0.08, "mktg_ratio": 0.09, "admin_ratio": 0.06, "base_rev": 6500000},
    {"slug": "battery_energy_storage", "name": "Grid Battery & Energy Storage", "super_sector": "CleanTech & Energy", "gross_margin": 0.38, "rnd_ratio": 0.22, "mktg_ratio": 0.08, "admin_ratio": 0.07, "base_rev": 5200000},
    {"slug": "carbon_accounting_esg", "name": "Carbon Accounting & Climate SaaS", "super_sector": "CleanTech & Energy", "gross_margin": 0.78, "rnd_ratio": 0.28, "mktg_ratio": 0.32, "admin_ratio": 0.10, "base_rev": 2000000},
    {"slug": "ev_charging_infra", "name": "EV Charging Station Networks", "super_sector": "CleanTech & Energy", "gross_margin": 0.35, "rnd_ratio": 0.12, "mktg_ratio": 0.14, "admin_ratio": 0.08, "base_rev": 3400000},
    {"slug": "waste_recycling_tech", "name": "Circular Waste Recycling Tech", "super_sector": "CleanTech & Energy", "gross_margin": 0.42, "rnd_ratio": 0.09, "mktg_ratio": 0.08, "admin_ratio": 0.06, "base_rev": 3900000},

    # 7. Media & Consumer Services (5)
    {"slug": "streaming_media_ott", "name": "Streaming Media & OTT Networks", "super_sector": "Media & Entertainment", "gross_margin": 0.45, "rnd_ratio": 0.18, "mktg_ratio": 0.32, "admin_ratio": 0.09, "base_rev": 4600000},
    {"slug": "digital_ad_agencies", "name": "Performance Digital Ad Agencies", "super_sector": "Media & Entertainment", "gross_margin": 0.55, "rnd_ratio": 0.06, "mktg_ratio": 0.20, "admin_ratio": 0.15, "base_rev": 1900000},
    {"slug": "traveltech_hospitality", "name": "TravelTech & Hospitality Platforms", "super_sector": "Media & Entertainment", "gross_margin": 0.62, "rnd_ratio": 0.14, "mktg_ratio": 0.35, "admin_ratio": 0.10, "base_rev": 2800000},
    {"slug": "quick_commerce", "name": "Quick-Commerce Grocery Logistics", "super_sector": "Media & Entertainment", "gross_margin": 0.24, "rnd_ratio": 0.10, "mktg_ratio": 0.25, "admin_ratio": 0.08, "base_rev": 5800000},
    {"slug": "fitness_wellness", "name": "Connected Fitness & Digital Wellness", "super_sector": "Media & Entertainment", "gross_margin": 0.58, "rnd_ratio": 0.14, "mktg_ratio": 0.34, "admin_ratio": 0.09, "base_rev": 1700000},

    # 8. Logistics & Supply Chain (5)
    {"slug": "freight_smart_logistics", "name": "Smart Freight & Trucking Logistics", "super_sector": "Logistics & Supply Chain", "gross_margin": 0.22, "rnd_ratio": 0.08, "mktg_ratio": 0.07, "admin_ratio": 0.05, "base_rev": 7800000},
    {"slug": "fulfillment_3pl", "name": "3PL Omnichannel Fulfillment", "super_sector": "Logistics & Supply Chain", "gross_margin": 0.26, "rnd_ratio": 0.06, "mktg_ratio": 0.08, "admin_ratio": 0.06, "base_rev": 6100000},
    {"slug": "cold_chain_logistics", "name": "Cold-Chain Pharma & Food Storage", "super_sector": "Logistics & Supply Chain", "gross_margin": 0.34, "rnd_ratio": 0.05, "mktg_ratio": 0.06, "admin_ratio": 0.06, "base_rev": 4700000},
    {"slug": "autonomous_delivery", "name": "Autonomous Delivery Drones & Bots", "super_sector": "Logistics & Supply Chain", "gross_margin": 0.40, "rnd_ratio": 0.32, "mktg_ratio": 0.14, "admin_ratio": 0.08, "base_rev": 2200000},
    {"slug": "commercial_fleet_mgmt", "name": "Commercial Fleet Telematics SaaS", "super_sector": "Logistics & Supply Chain", "gross_margin": 0.70, "rnd_ratio": 0.20, "mktg_ratio": 0.25, "admin_ratio": 0.11, "base_rev": 2400000},

    # 9. Frontier & DeepTech (5)
    {"slug": "quantum_computing", "name": "Quantum Computing & Quantum SaaS", "super_sector": "Frontier & DeepTech", "gross_margin": 0.82, "rnd_ratio": 0.60, "mktg_ratio": 0.12, "admin_ratio": 0.14, "base_rev": 3200000},
    {"slug": "spacetech_satellites", "name": "Commercial Satellites & SpaceTech", "super_sector": "Frontier & DeepTech", "gross_margin": 0.42, "rnd_ratio": 0.42, "mktg_ratio": 0.08, "admin_ratio": 0.10, "base_rev": 4500000},
    {"slug": "autonomous_driving", "name": "Autonomous Vehicle AI Systems", "super_sector": "Frontier & DeepTech", "gross_margin": 0.65, "rnd_ratio": 0.48, "mktg_ratio": 0.15, "admin_ratio": 0.10, "base_rev": 3900000},
    {"slug": "synthetic_biology", "name": "Synthetic Biology Biofoundries", "super_sector": "Frontier & DeepTech", "gross_margin": 0.75, "rnd_ratio": 0.50, "mktg_ratio": 0.14, "admin_ratio": 0.12, "base_rev": 3100000},
    {"slug": "vertical_agritech", "name": "Vertical Indoor Agritech & Robotics", "super_sector": "Frontier & DeepTech", "gross_margin": 0.44, "rnd_ratio": 0.22, "mktg_ratio": 0.12, "admin_ratio": 0.08, "base_rev": 2700000},

    # 10. Professional & Enterprise Services (5)
    {"slug": "it_consulting", "name": "IT Modernization & Cloud Integration", "super_sector": "Professional Services", "gross_margin": 0.40, "rnd_ratio": 0.08, "mktg_ratio": 0.12, "admin_ratio": 0.12, "base_rev": 4200000},
    {"slug": "legaltech_ai", "name": "LegalTech & Contract Intelligence", "super_sector": "Professional Services", "gross_margin": 0.80, "rnd_ratio": 0.30, "mktg_ratio": 0.32, "admin_ratio": 0.11, "base_rev": 2000000},
    {"slug": "management_consulting", "name": "Strategy & Corporate Transformation", "super_sector": "Professional Services", "gross_margin": 0.52, "rnd_ratio": 0.05, "mktg_ratio": 0.15, "admin_ratio": 0.16, "base_rev": 3300000},
    {"slug": "creative_studios", "name": "Creative Media & Design Studios", "super_sector": "Professional Services", "gross_margin": 0.48, "rnd_ratio": 0.06, "mktg_ratio": 0.18, "admin_ratio": 0.12, "base_rev": 1800000},
    {"slug": "renewable_epc_engineering", "name": "Clean Energy Engineering & EPC", "super_sector": "Professional Services", "gross_margin": 0.28, "rnd_ratio": 0.07, "mktg_ratio": 0.08, "admin_ratio": 0.06, "base_rev": 6800000},
]

def generate_all_50_benchmarks():
    """Generates all 50 curated industry benchmark CSV files and catalog.json."""
    BENCHMARKS_DIR.mkdir(parents=True, exist_ok=True)
    catalog = []

    regions = ["North America", "Europe", "Asia-Pacific", "India", "Latin America"]

    for idx, profile in enumerate(SECTOR_PROFILES):
        np.random.seed(100 + idx)
        n_companies = np.random.randint(50, 75)
        companies = []

        for c_idx in range(n_companies):
            reg = np.random.choice(regions, p=[0.35, 0.25, 0.20, 0.15, 0.05])
            scale_factor = np.random.lognormal(mean=0.0, sigma=0.45)
            rev = profile["base_rev"] * scale_factor * (1 + np.random.normal(0, 0.05))

            cogs = rev * (1.0 - profile["gross_margin"]) * (1 + np.random.normal(0, 0.03))
            gross_profit = rev - cogs

            rnd = rev * profile["rnd_ratio"] * (1 + np.random.normal(0, 0.06))
            mktg = rev * profile["mktg_ratio"] * (1 + np.random.normal(0, 0.06))
            admin = rev * profile["admin_ratio"] * (1 + np.random.normal(0, 0.04))

            # Profit = Gross Profit - (R&D + Marketing + Admin)
            profit = gross_profit - (rnd + mktg + admin)
            margin_pct = (profit / rev) * 100.0 if rev > 0 else 0.0

            companies.append({
                "Company": f"{profile['name'].split()[0]}_{c_idx+1}",
                "Region": reg,
                "R&D Spend": round(max(5000.0, rnd), 2),
                "Administration": round(max(5000.0, admin), 2),
                "Marketing Spend": round(max(5000.0, mktg), 2),
                "Revenue": round(rev, 2),
                "COGS": round(cogs, 2),
                "Profit": round(profit, 2),
                "Margin_Pct": round(margin_pct, 2),
            })

        df = pd.DataFrame(companies)
        csv_path = BENCHMARKS_DIR / f"{profile['slug']}.csv"
        df.to_csv(csv_path, index=False)

        avg_profit = float(df["Profit"].mean())
        avg_rev = float(df["Revenue"].mean())
        avg_margin = float(df["Margin_Pct"].mean())

        catalog.append({
            "id": idx + 1,
            "slug": profile["slug"],
            "name": profile["name"],
            "super_sector": profile["super_sector"],
            "companies_count": n_companies,
            "benchmark_gross_margin": f"{profile['gross_margin']*100:.0f}%",
            "benchmark_rnd_ratio": f"{profile['rnd_ratio']*100:.0f}%",
            "benchmark_mktg_ratio": f"{profile['mktg_ratio']*100:.0f}%",
            "benchmark_admin_ratio": f"{profile['admin_ratio']*100:.0f}%",
            "avg_revenue": round(avg_rev, 2),
            "avg_profit": round(avg_profit, 2),
            "avg_margin_pct": round(avg_margin, 2),
            "file_path": str(csv_path.relative_to(BASE_DIR)),
        })

    catalog_path = BENCHMARKS_DIR / "catalog.json"
    with open(catalog_path, "w") as f:
        json.dump(catalog, f, indent=2)

    logging.info(f"Successfully generated 50 industry benchmark datasets in {BENCHMARKS_DIR}")
    logging.info(f"Catalog saved with {len(catalog)} sectors.")
    return catalog

if __name__ == "__main__":
    generate_all_50_benchmarks()

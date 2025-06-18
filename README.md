# 🚓 EnforceIQ - Traffic Stop Analytics

A dynamic **Streamlit-based dashboard** integrated with **PostgreSQL** to monitor, analyze, and forecast traffic stop outcomes.  
This project supports **data-driven policing** through SQL-powered insights, interactive visualizations, and intelligent form-based predictions.

---

## 📌 Project Overview

**🎯 Objective**  
To digitize and analyze police traffic stop logs by providing a centralized system for data entry, pattern recognition, and predictive insights.

**🛠️ Challenges Solved**
- Eliminates inefficiencies from manual recordkeeping.
- Enables centralized access to multi-point traffic stop data.
- Provides immediate insights into arrest trends, driver demographics, and violations.

---

## 🧩 Key Features

- ✅ Instant recording of traffic stop events by police
- 📊 Essential insights into arrests, searches, violations, and driver profiles
- 📈 Interactive visual dashboards powered by **Plotly** for deeper exploration
- 🔍 14 mid-level SQL query selections via user-friendly dropdown
- 🧠 6 advanced SQL analytics (joins, subqueries, window functions)
- 🧮 Smart prediction module for stop outcomes and likely violations
- 💬 Streamlined UI using **Streamlit** for intuitive navigation
- 🔐 Robust **PostgreSQL** integration for secure, scalable data storage

---

## 📂 Dataset Structure

| Field               | Example         | Description                         |
|--------------------|-----------------|-------------------------------------|
| stop_date          | 2024-06-10      | Date of vehicle stop                |
| driver_age         | 27              | Cleaned driver age                  |
| driver_gender      | M / F           | Gender of the driver                |
| violation          | Speeding / DUI  | Reason for the stop                 |
| stop_outcome       | Warning / Arrest| Final result of the stop            |
| search_conducted   | True / False    | Whether a search was performed      |
| drugs_related_stop | True / False    | Whether it was drug-related         |

---

## 📦 Project Structure
## 📁 EnforceIQ Folder Layout
├── 🧠 `testproject.py` – Main Streamlit dashboard app  
├── 📦 `requirements.txt` – Python dependencies  
├── 🗃️ `sql/` – SQL query scripts (optional)  
├── 📑 `docs/` – Project documentation (e.g., Police.docx)  
└── 📘 `README.md` – Project overview and guide 



🤝 **Contributors**  
👨‍💻 Santhanalakshmi V  
👩‍🏫 Guided by: GUVI x HCL Capstone Team




---
## ✅ Conclusion

**EnforceIQ** is a streamlined, interactive dashboard that simplifies traffic stop analysis for law enforcement and analysts.  
With a user-friendly interface, powerful insights, and clean visuals, it promotes **data-driven decisions**, **safer roads**, and **community trust**.

With a clean UI and easy deployment via Streamlit, this project showcases the potential of data analytics in public safety.

**🚦 Drive Safe. Analyze Smarter. Save Lives. ❤️**

---




# 🧭 Job Listings Scraper

A simple Python project that **collects job listings from a website** and shows them in an **easy-to-use web app**. You can search, filter, and download the jobs as a CSV file.

This project is great for beginners who want to learn **web scraping** and **building a web app** with Python.

---

## 📖 Introduction

Have you ever wanted to collect information from a website automatically, instead of copying it by hand? That is called **web scraping**.

This project scrapes job listings from the [Fake Python Jobs website](https://realpython.github.io/fake-jobs/) — a website made specially for practicing web scraping. It is safe to use because it does not block scrapers or require login.

The project does two main things:

1. **Scrapes the website** — Downloads the page and pulls out useful information for each job: the **job title**, **company name**, **location**, and the **link to apply**.
2. **Shows the data in a web app** — Using a tool called **Streamlit**, the scraped data is displayed in a clean, interactive dashboard where you can search, filter, and download the results.

You don't need to know web scraping or Streamlit before starting. This README explains everything in simple words.

---

## ✨ Features

- 🔍 Scrapes all job listings automatically (title, company, location, apply link)
- 🖥️ Interactive web dashboard (built with Streamlit) — no coding needed to use it
- 🔎 Search jobs by title or company name
- 📍 Filter jobs by location
- 📊 Charts showing top locations and top companies
- ⬇️ Download the results as a CSV file (opens in Excel, Google Sheets, etc.)
- 🔄 "Refresh" button to scrape the website again anytime
- ⚠️ Handles errors nicely (e.g. if the website is down, or a job is missing some information)

---

## 🗂️ Project Structure

Here is what each file and folder does:

```
job_scraper_app/
├── app.py                  # The main file — this runs the web app
├── scraper/                # A small "package" that does the scraping
│   ├── __init__.py         # Connects everything inside the scraper folder
│   ├── fetcher.py          # Downloads the raw webpage (the HTML)
│   ├── parser.py           # Reads the HTML and pulls out job details
│   └── exporter.py         # Converts job details into a table or a CSV file
├── data/                   # Where downloaded CSV files can be saved
├── .streamlit/
│   └── config.toml         # Controls the app's colors and look
├── requirements.txt        # List of libraries needed to run the project
└── README.md                # This file — explains the whole project
```

### Why is the code split into separate files?

Instead of writing everything in one big file, the project is broken into small pieces that each do **one job only**. This makes the code:

- **Easier to read** — you know exactly where to look for something
- **Easier to fix** — if something breaks, you only need to check one small file
- **Easier to reuse** — you can use the scraper part alone, without the web app, if you want

This is a common and recommended way of organizing real-world Python projects.

---

## ⚙️ How It Works (Step by Step)

1. The app opens and calls `fetch_page()` to **download the webpage** as raw HTML (this is the same code your browser reads to show you a page).
2. The raw HTML is sent to `parse_job_cards()`, which **reads through the HTML** and finds every job listing on the page.
3. For each job, it pulls out four pieces of information:
   - Job title
   - Company name
   - Location
   - Link to apply
4. All the jobs are collected into a **table** (using `to_dataframe()`), which is easy to search, sort, and filter.
5. The table is shown in the Streamlit app, where you can:
   - Type a keyword to search
   - Pick a location from a dropdown to filter
   - Click "Download CSV" to save the results
6. If you click **Refresh**, steps 1–4 run again to get the latest data.

---

## 🧩 Explanation of Each Function

### `scraper/fetcher.py`
| Function | What it does |
|---|---|
| `fetch_page(url)` | Sends a request to the website and downloads its HTML content. If the website is down or there's a network problem, it raises a clear error instead of crashing silently. |

### `scraper/parser.py`
| Function | What it does |
|---|---|
| `JobListing` | A simple data structure that holds one job's information: `title`, `company`, `location`, `url`. |
| `parse_job_cards(html)` | Looks through the HTML and finds every job "card" on the page. For each one, it reads the title, company, and location text, and grabs the "Apply" link. If any piece of information is missing, it fills in a placeholder like `"Unknown Location"` instead of crashing. |
| `_get_text_or_default(element, default)` | A small helper that safely reads text from a webpage element, and returns a default value if that element doesn't exist. |

### `scraper/exporter.py`
| Function | What it does |
|---|---|
| `to_dataframe(jobs)` | Converts the list of jobs into a **pandas DataFrame** — a table format that's easy to display, search, and filter in the app. |
| `save_to_csv(jobs, filepath)` | Saves the list of jobs into a `.csv` file on your computer, which you can open in Excel or Google Sheets. |

### `app.py`
This is the main file that builds the web page you see in your browser. It does the following:

- Sets up the page title, icon, and layout
- Calls the scraper functions to load job data (and **caches** the result for 10 minutes, so it doesn't re-download the page every time you click something)
- Builds the sidebar with a search box, location filter, and refresh button
- Displays summary numbers (total jobs, jobs matching your filter, unique companies)
- Shows the results in a table with clickable "Apply" links
- Adds a "Download CSV" button
- Shows two bar charts: top locations and top companies

---

## 🛠️ Technologies and Libraries Used

| Technology / Library | What it is used for |
|---|---|
| **[Python](https://www.python.org/)** | The programming language the whole project is written in. |
| **[Streamlit](https://streamlit.io/)** | Turns Python code into an interactive web app, without needing to know HTML, CSS, or JavaScript. Used to build the dashboard you see and click on. |
| **[Requests](https://docs.python-requests.org/)** | Downloads the raw content (HTML) of a webpage, just like a browser does when you visit a website. |
| **[Beautiful Soup (bs4)](https://www.crummy.com/software/BeautifulSoup/)** | Reads through messy HTML and helps pick out exactly the pieces of information you need (like a job title inside a specific tag). |
| **[pandas](https://pandas.pydata.org/)** | Organizes the scraped data into a table (called a DataFrame), which makes it easy to search, sort, filter, and export. |
| **`csv` module** | Part of Python's built-in toolkit. Used to save data into `.csv` files. |
| **`dataclasses` module** | Part of Python's built-in toolkit. Used to create the simple `JobListing` structure that holds each job's details. |

---

## 💻 Installation and Setup

### 1. Clone this repository

```bash
git clone https://github.com/your-username/job_scraper_app.git
cd job_scraper_app
```

### 2. Create a virtual environment (recommended, but optional)

A virtual environment keeps this project's libraries separate from other Python projects on your computer.

```bash
python -m venv .venv

# Activate it:
# On Mac/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

### 3. Install the required libraries

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

Your browser should open automatically at `http://localhost:8501`. If it doesn't, copy that link into your browser manually.

---

## 🚀 Using the App

1. When the app opens, it automatically scrapes the job listings.
2. Use the **search box** in the sidebar to look for a job title or company (e.g. type "python").
3. Use the **location dropdown** to only show jobs from a specific city.
4. Look at the **metrics** at the top to see how many jobs matched.
5. Scroll the table and click **"Apply →"** to open a job's detail page.
6. Click **"Download filtered results as CSV"** to save the current results to your computer.
7. Click **"🔄 Scrape / Refresh listings"** in the sidebar anytime you want fresh data.

---

## 🐍 Using the Scraper Without Streamlit

The scraping code also works completely on its own, if you just want the data without the web app:

```python
from scraper import fetch_page, parse_job_cards, save_to_csv

html = fetch_page("https://realpython.github.io/fake-jobs/")
jobs = parse_job_cards(html)
save_to_csv(jobs, "data/job_listings.csv")

print(f"Saved {len(jobs)} listings.")
```

---

## 🧠 What You Will Learn From This Project

- How to send a web request and download a webpage with `requests`
- How to read HTML and pull out specific data using `BeautifulSoup`
- How to organize data using `pandas`
- How to save data to a CSV file
- How to build a simple, interactive web app with `Streamlit`
- How to structure a Python project into clean, reusable files

---

## ⚠️ Notes and Limitations

- This project scrapes a **practice website** built for learning (`realpython.github.io/fake-jobs`). It is not meant for scraping real job sites, which may have different rules, structures, or protections.
- Always check a website's **Terms of Service** and `robots.txt` file before scraping it in real projects.
- If a job listing is missing information (like location), the app shows a placeholder instead of breaking.

---

## 🔮 Possible Future Improvements

- Add pagination support, for websites with multiple pages of listings
- Add more filters (e.g. by date posted)
- Store results in a database (like SQLite) instead of just CSV
- Add automated tests for the scraper functions
- Deploy the app online (e.g. with Streamlit Community Cloud) so others can use it without installing anything

---

## 📄 License

This project is open for learning and personal use. Feel free to fork it, modify it, and use it in your own portfolio.

---

## 🙋 Questions?

If something doesn't work or you have a question about the code, feel free to open an issue on this repository.
# python-job-listings-scraper

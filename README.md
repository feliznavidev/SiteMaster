# SiteMaster - Canvas Content Scraper

A Python tool that uses Selenium to authenticate with Canvas LMS and download course content for offline viewing.

## Features

- Automated Microsoft authentication for Canvas LMS
- Persistent browser session for reliable content scraping
- Downloads rendered HTML content including dynamic elements
- Handles file downloads with proper extensions
- Saves all content locally for offline access
- **Includes complete offline Canvas content for AI analysis**

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/SiteMaster.git
   cd SiteMaster
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install selenium requests beautifulsoup4 python-dotenv
   ```

4. **Configure environment**
   - Copy `.env.example` to `.env`
   - Fill in your Canvas credentials:
     ```
     site_url='https://your-institution.instructure.com'
     site_login='your_email@your-institution.edu'
     site_password='your_password_here'
     ```

5. **Install Chrome WebDriver**
   - Download ChromeDriver from https://chromedriver.chromium.org/
   - Ensure it's in your PATH or place in project directory

## Usage

```bash
python download_site.py
```

The script will:
1. Launch Chrome in headless mode
2. Navigate to your Canvas site
3. Handle Microsoft authentication automatically
4. Scrape and download all accessible course content
5. Save content to `offline_site/` directory

## AI Playground Ready

This repository includes complete offline Canvas content from multiple courses, making it perfect for:
- **Course preparation and analysis**
- **AI-powered study assistance** 
- **Offline content review**
- **Academic research and planning**

The scraped content includes syllabi, assignments, course modules, and instructional materials from:
- ENGL1301 - Rhetoric and Composition I (Dr. Troy White)
- Additional courses with full content structure

## Security Notes

- **Never commit your `.env` file** - it contains sensitive credentials
- The `.gitignore` file protects your environment variables and downloaded content
- Downloaded content may contain personal information and should be kept private

## Requirements

- Python 3.7+
- Chrome browser
- ChromeDriver
- Canvas LMS access with Microsoft authentication

## Project Structure

```
SiteMaster/
├── download_site.py     # Main scraper script
├── .env.example         # Environment template
├── .gitignore          # Git ignore patterns
├── README.md           # This file
└── offline_site/       # Downloaded Canvas content (339+ files)
    ├── courses/        # Course-specific content
    │   ├── 21350/     # ENGL1301 - Rhetoric and Composition I
    │   ├── 21716/     # Course materials and assignments
    │   └── 22126/     # Additional course content
    ├── files/         # Course documents (PDFs, DOCX, etc.)
    └── scraped_*/     # Direct page captures for analysis
```

## License

This project is for educational purposes. Respect your institution's terms of service when using this tool.

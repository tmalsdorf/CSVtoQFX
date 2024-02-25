

# CSV to OFX Converter

In a world where online converters are as plentiful as stars in the sky, the question isn't just about converting our CSV documents to OFX format; it's about trust. Can we really trust these online tools with our sensitive financial data? Enter our Flask-based CSV to OFX Converter, the in-house solution that promises not just conversion, but also confidentiality and security. This application allows users to upload CSV files containing transaction data and converts them to the OFX (Open Financial Exchange) forma, all while ensuring your financial data never lingers unnecessarily on any server. Ideal for importing transaction data into financial software that supports OFX, it's the trustworthy bridge between your CSV data and OFX-ready financial tools.

Its not pretty yet but it gets the job done.

## Features

- Upload a CSV file through a simple web interface.
- Converts CSV transaction data to OFX format.
- Download the converted OFX file.
- Health check endpoint for monitoring the application's status.

## Installation

Before running the application, ensure you have Python installed on your system. This application has been tested with Python 3.10.

1. **Clone the Repository**

   ```bash
   git clone https://github.com/tmalsdorf/CSVtoQFX.git
   cd CSVtoQFX
   ```

2. **Set Up a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r app/requirements.txt
   ```

## Running the Application

1. Start the Flask server:

   ```bash
   python app.py
   ```

2. Access the application via a web browser:

   ```
   http://localhost:5000/
   ```

## Usage

1. **CSV File Format**

   The CSV file should have the following headers:
   - Trans. Date (MM/DD/YYYY)
   - Post Date (MM/DD/YYYY)
   - Description
   - Amount
   - Category

2. **Uploading a CSV File**

   - Navigate to `http://localhost:5000/` on your web browser.
   - Click 'Choose File' and select your CSV file.
   - Click 'Upload' to submit the file for conversion.

3. **Downloading the OFX File**

   - After uploading, the converted OFX file will be automatically downloaded.

4. **Health Check**

   - To check if the application is running, access `http://localhost:5000/health`.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## License

GPL-3.0 license

---


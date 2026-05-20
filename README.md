# My Python Web Application

This is a simple web application built using Flask that connects to a MySQL database named "labtextil" located on a computer called "vi2wpc26462c".

## Project Structure

```
my-python-web-app
├── app
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   └── templates
│       └── index.html
├── config.py
├── requirements.txt
└── README.md
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd my-python-web-app
   ```

2. **Create a virtual environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Configure the database connection**:
   Update the `config.py` file with your MySQL database credentials if necessary.

5. **Run the application**:
   ```
   python app/__init__.py
   ```

6. **Access the application**:
   Open your web browser and go to `http://localhost:5000`.

## Usage

This application provides a simple interface to interact with the MySQL database. You can extend the functionality by adding more routes and templates as needed.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
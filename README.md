# Shop Backend

A full-featured e-commerce web application built with **Django** and **PostgreSQL**.

This project was developed as a practical full-stack web development project, with a focus on building a real-world online shopping platform, including product management, user accounts, shopping cart, orders, payment flow, multilingual support, and an administration panel.

## 🚀 Live Demo

**Live Website:** [Visit the live website](https://shop-backend-nu.vercel.app)

## ✨ Features

* User registration, login, logout, and account activation
* Password reset functionality
* User profile and account dashboard
* Product listing and product details
* Product categories
* Product variants such as size and color
* Product images and variant-specific images
* Shopping cart
* Order management
* Payment flow
* Product search and filtering
* Best-selling and newest product sections
* Responsive design for desktop and mobile devices
* Multilingual support (English / Persian)
* Translatable templates and JavaScript strings
* Jalali/Gregorian date support
* Django administration panel
* PostgreSQL database
* Cloudinary integration for media files

## 🛠️ Technologies

* **Python**
* **Django**
* **PostgreSQL**
* **JavaScript**
* **HTML5**
* **CSS3**
* **Bootstrap**
* **Git & GitHub**
* **Cloudinary**
* **Django Modeltranslation**

## 📁 Project Structure

The project is organized into separate Django applications for different parts of the website:

* `home_module` — Homepage and main website sections
* `product_module` — Products, categories, variants, and product details
* `account_module` — User authentication and account functionality
* `profile_module` — User profile and dashboard
* `order_module` — Cart, orders, and checkout
* `contact_module` — Contact functionality
* `article_module` — Articles
* `polls` — Poll functionality
* `aboutus_module` — About us section
* `sitsetting_module` — Website settings

## 🌐 Multilingual Support

The website supports both **English and Persian**.

The project uses Django's internationalization system to provide translated:

* Templates
* Form labels and messages
* Navigation elements
* JavaScript messages
* Product-related content

## 🗄️ Database

The project uses **PostgreSQL** as its primary database.

## 📱 Responsive Design

The interface is designed to work across different screen sizes, including desktop and mobile devices.

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Aysuda-dev/Shop-backend.git
cd Shop-backend
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create your environment variables and configure the database and other required settings.

Run migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

The project will then be available at:

```text
http://127.0.0.1:8000/
```

## 👩‍💻 About

This project was developed by **Aysuda Badrloo** as a practical Django web development project.

The project demonstrates experience with backend development using Django and Python, database integration, frontend interaction with JavaScript, authentication, e-commerce functionality, multilingual websites, and deployment workflows.

## 📌 Project Status

The project is currently deployed online and connected to GitHub.

## 📄 License

This project is created for portfolio and educational purposes.

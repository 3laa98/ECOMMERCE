# ECOMMERCE

A comprehensive e-commerce platform built with Django, featuring a robust backend, dynamic frontend, and seamless deployment on AWS using GitHub Actions.

## Features

- **User Authentication**: Secure user registration, login, and profile management.
- **Product Management**: CRUD operations for products with detailed views and categorization.
- **Shopping Cart**: Add, update, and remove items with real-time price calculations.
- **Order Processing**: Streamlined checkout process with order history tracking.
- **Payment Integration**: Secure payment processing using Stripe.
- **Search Functionality**: Full-text search to quickly find products.

## Technologies Used

- **Backend**:
  - **Django**: High-level Python web framework.
  - **Django Signals**: Implemented for decoupled event handling, such as sending confirmation emails upon successful orders.
  - **Django Forms**: Utilized for form handling, validation, and rendering in templates.
- **Frontend**:
  - **HTML & CSS**: Markup and styling.
  - **Bootstrap**: Responsive design framework.
  - **JavaScript & jQuery**: Enhanced interactivity and dynamic content loading.
- **Database**:
  - **PostgreSQL**: Robust and scalable relational database.
- **Deployment**:
  - **AWS EC2**: Hosting the application on a virtual server.
  - **GitHub Actions**: Continuous Integration and Deployment (CI/CD) pipeline for automated testing and deployment.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/3laa98/ECOMMERCE.git
   ```
2. **Navigate to the Project Directory**:
   ```bash
   cd ECOMMERCE
   ```
3. **Set Up Virtual Environment**:
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```
4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Configure Environment Variables**:
   - Create a `.env` file in the root directory.
   - Add the necessary environment variables as specified in `.envsample`.
6. **Apply Migrations**:
   ```bash
   python manage.py migrate
   ```
7. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```
8. **Collect Static Files**:
   ```bash
   python manage.py collectstatic
   ```
9. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

## Deployment

The application is deployed on AWS EC2 with automated deployment configured via GitHub Action
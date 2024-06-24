# Hotel_Room_Management

This project is a Django-based RESTful API for managing hotel room rates, including functionality for applying overridden rates and discounts. The API allows clients to retrieve the final rate for a specific room and date range, considering any overridden rates and applicable discounts.
The system handles default rates, overridden rates, and discounts, and provides API endpoints to create, update, delete, and display room rates. The system also contain discount logic and shows the lowest rates based on room ID, date range, and available discounts.

## Project Overview

This API allows hotels to manage and retrieve room rates, including the application of overridden rates and discounts. It provides endpoints to:
- Create and update room rates.
- Create and update overridden rates for specific dates.
- Create and update discounts applicable to room rates.
- Retrieve the final rate for a room within a specified date range.

## Features

- **Room Rate Management**: Default room rates can be set and retrieved.
- **Overridden Rates**: Specific rates can be set for particular dates, overriding the default rates.
- **Discounts**: Discounts (fixed or percentage) can be applied to room rates.
- **Final Rate Calculation**: Calculate the final rate for a room and date range, considering overridden rates and discounts.

## Setup Instructions

### Prerequisites

- Python 3.7+
- Django 3.0+
- SQLite for development

### Installation

1. **Clone the repository**:
   - git clone https://github.com/rswarn01/Hotel_Room_Management.git
   - cd hotel_management
   
3. **Create and activate a virtual environment**:
   - python3 -m venv venv
   - source venv/bin/activate  # On Windows use `venv\Scripts\activate`

4. **Install the required packages:**
   - pip install -r requirements.txt
   
5. **Apply the migrations:**
   - python manage.py makemigrations
   - python manage.py migrate

6. **Create a superuser:**
   - python manage.py createsuperuser

7. **Start the development server:**
   - python manage.py runserver

8. **Swagger documentation URL**:
   - http://127.0.0.1:8000/swagger/


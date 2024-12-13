# Security Best Practices for Django Application

## Overview
This README outlines the key steps and configurations implemented to enhance the security of a Django application. These measures are aimed at mitigating vulnerabilities like Cross-Site Scripting (XSS), Cross-Site Request Forgery (CSRF), and SQL Injection.

---

## Steps Implemented

### 1. **Secure Settings Configuration**
- Set `DEBUG` to `False` in production to prevent sensitive information from being displayed in error messages.
- Added the following settings in `settings.py` for additional security:
  ```python
  SECURE_BROWSER_XSS_FILTER = True
  X_FRAME_OPTIONS = 'DENY'
  SECURE_CONTENT_TYPE_NOSNIFF = True
  CSRF_COOKIE_SECURE = True
  SESSION_COOKIE_SECURE = True
  ```

### 2. **CSRF Token Implementation**
- All forms in the templates include the `{% csrf_token %}` tag to prevent CSRF attacks.
  Example:
  ```html
  <form method="POST" action="/submit-form/">
      {% csrf_token %}
      <input type="text" name="input_field">
      <button type="submit">Submit</button>
  </form>
  ```

### 3. **Secure Query Handling in Views**
- Used Django ORM to handle database queries safely and avoid SQL injection.
- Example of a secure query in `views.py`:
  ```python
  from django.shortcuts import render
  from .models import Book

  def search_books(request):
      query = request.GET.get('q', '')
      books = Book.objects.filter(title__icontains=query)
      return render(request, 'bookshelf/book_list.html', {'books': books})
  ```

### 4. **Content Security Policy (CSP)**
- Installed the `django-csp` middleware to define and enforce a CSP header.
- Added CSP configurations to `settings.py`:
  ```python
  CSP_DEFAULT_SRC = ("'self'",)
  CSP_SCRIPT_SRC = ("'self'", "https://trusted.cdn.com")
  CSP_STYLE_SRC = ("'self'", "https://trusted.cdn.com")
  ```

### 5. **Documentation and Testing**
- Added comments in code explaining each implemented security measure.
- Performed manual testing to validate:
  - CSRF protection on forms.
  - XSS protection by attempting to inject scripts in input fields.
  - SQL injection prevention by testing with malicious SQL queries.

---

## Testing the Application
### Manual Testing Steps
1. Assign `DEBUG = False` in the settings.
2. Create a test form and verify the presence of `{% csrf_token %}`.
3. Attempt XSS attacks by injecting scripts in form fields and ensure they're sanitized.
4. Use tools or manual input to check for SQL injection vulnerabilities.

### Key Files Updated
- `settings.py`: Added secure configurations.
- Templates: Included CSRF tokens in forms (e.g., `form_example.html`).
- `views.py`: Ensured ORM is used and user input is validated.

---

## Dependencies
- **Django CSP Middleware**
  Install via:
  ```bash
  pip install django-csp
  ```

---

## Additional Notes
- Always review Django's [official security guide](https://docs.djangoproject.com/en/stable/topics/security/) for the latest best practices.
- Regularly update dependencies to address known vulnerabilities.



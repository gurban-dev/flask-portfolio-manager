from app import db
from datetime import datetime

'''
Handles user authentication, profile management, and
relationships with accounts.
'''

# The db.Model inside the User class tells us that
# this User class will inherit from the db.Model class.

# db.Model is the parent class whereas User is the child class.
class User(db.Model):
  '''
  User model represents the user who register an account
  on the website.
  '''

  # **kwargs means accept any number of keyword arguments.

  # end='\n' is a keyword because the parameter name "end"
  # was explicitly written out.
  # print('Hello', end='\n')
  def __init__(self, **kwargs):
    '''Initialise the user with default values.'''

    # super() calls the constructor of the parent class.
    super(User, self).__init__(**kwargs)

    if not self.preferred_currency and self.country_code:
      # Set the default currency based on the country.
      currency_map = {
        'NO': 'NOK',
        'GB': 'GBP',
        'IT': 'EUR'
      }

      # Attempts to obtan the value that corresponds to the key
      # self.country_code. If a value for self.country_code doesn't
      # exist in the dictionary currency_map, fallback to 'EUR'.
      # .get(self.country_code, 'EUR')
      self.preferred_currency = currency_map.get(self.country_code, 'EUR')

  # The primary key is one way of uniquely identifying rows
  # in a database table.
  id = db.Column(db.Integer, primary_key=True)

  email_address = db.Column(db.String(120), unique=True, nullable=False)

  password_hash = db.Column(db.String(255), nullable=False)

  full_name = db.Column(db.String(100))
  phone_number = db.Column(db.String(20))

  # ISO country code (E.g. NO (Norway), IT (Italy))
  country_code = db.Column(db.String(2))

  # E.g. EUR, NOK
  preferred_currency = db.Column(db.String(3))

  # OAuth Fields (for Google)
  # E.g. 'google'
  oauth_provider = db.Column(db.String(20))

  oauth_id = db.Column(db.String(100))

  # Account status
  is_active = db.Column(db.Boolean, default=True)
  is_verified = db.Column(db.Boolean, default=False)
  verification_token = db.Column(db.String(100), unique=True)

  # Timestamps
  created_at = db.Column(
    db.DateTime,
    default=datetime.now(datetime.timezone.utc),
    nullable=False
  )

  updated_at = db.Column(
    db.DateTime,
    default=datetime.now(datetime.timezone.utc),
    onupdate=datetime.now(datetime.timezone.utc)
  )

  last_login = db.Column(db.DateTime)

  # Security
  two_factor_enabled = db.Column(db.Boolean, default=False)

  # Preferences
  notification_preferences = db.Column(db.JSON, {
    'email_address': True,
    'push': True,

    # Does the user want to receive a weekly summary of
    # the state of their investments?
    'weekly_summary': True
  })

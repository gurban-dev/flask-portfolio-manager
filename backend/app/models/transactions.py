from app import db
from datetime import datetime


class Transaction(db.Model):
  __tablename__ = 'transactions'

  # The primary key is the unique identifier for records/rows in a
  # database table.
  id = db.Column(db.Integer, primary_key=True)

  account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)

  # Monetary value of the transaction.
  amount = db.Column(db.Numeric(15, 2), nullable=False)

  # The type of currency the transaction is in.
  currency = db.Column(db.String(3), default='EUR')

  # BUY, SELL, DIVIDEND
  transaction_type = db.Column(db.String(20))

  # The name of the asset involved in the transaction.
  # Apple Inc., Tesla Energy ETF
  asset_name = db.Column(db.String(100))

  # The stock of asset symbol. Useful for linking market data
  # and tracking performance.
  # E.g. AAPL for Apple, TSLA for Tesla.
  asset_ticker = db.Column(db.String(10))

  # A numeric value that represent the environmental, social and
  # governance performance of an asset.
  # Range: 0-100
  esg_score = db.Column(db.Float)

  # Measures the carbon footprint associated with the asset or transaction.
  # Kilograms of CO2
  co2_impact = db.Column(db.Float)

  # The date and time the transaction occurred.
  timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

  # Additional details about the transaction.
  # E.g. Rationale, external links, or reminders.
  notes = db.Column(db.Text)
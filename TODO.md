# TODO: Integrate Chargily pay-v2 Payment Method

- [x] Add chargily-pay-v2 library to requirements.txt (replaced with requests)
- [x] Update Paiement model to add chargily_payment_id field
- [x] Modify /pay/<id> route in paiements_controller.py to create Chargily checkout session
- [x] Add /payment/success/<id> route for successful payment callback
- [x] Add /payment/failure/<id> route for failed payment callback
- [x] Update payment status based on Chargily callbacks
- [x] Set up environment variables for Chargily test API keys
- [x] Add python-dotenv to requirements.txt and load .env in app.py
- [x] Test the integration (requires valid API keys from Chargily dashboard - setup complete, testing requires valid keys)

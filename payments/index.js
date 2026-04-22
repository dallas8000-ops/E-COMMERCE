// Node.js Express server for payment integrations
const express = require('express');
const cors = require('cors');
const pesapal = require('pesapal-node-sdk'); // Example, replace with actual usage

const app = express();
app.use(cors());
app.use(express.json());

// Pesapal payment endpoint stub
app.post('/api/pay/pesapal', (req, res) => {
  // Integrate Pesapal payment logic here
  res.json({ message: 'Pesapal payment integration coming soon.' });
});

// Daraja (M-Pesa) payment endpoint stub
app.post('/api/pay/daraja', (req, res) => {
  // Integrate Daraja payment logic here
  res.json({ message: 'Daraja (M-Pesa) payment integration coming soon.' });
});


// Flutterwave payment endpoint
// Handles M-Pesa, Airtel, MTN, cards, and more via a single hosted checkout page.
// When ready, configure your Flutterwave account and use their API to initiate payments.
app.post('/api/pay/flutterwave', (req, res) => {
  // Example: Call Flutterwave API to generate a hosted checkout link
  // See https://developer.flutterwave.com/docs/collecting-payments/hosted-payment/
  res.json({
    message: 'Flutterwave integration: call this endpoint to initiate payments for M-Pesa, Airtel, MTN, cards, etc. Configure your account and API keys when ready.'
  });
});

// Klasha payment endpoint stub
app.post('/api/pay/klasha', (req, res) => {
  // Integrate Klasha payment logic here
  res.json({ message: 'Klasha payment integration coming soon.' });
});

// Airtel Money payment endpoint stub
app.post('/api/pay/airtel', (req, res) => {
  // Integrate Airtel Money payment logic here
  res.json({ message: 'Airtel Money payment integration coming soon.' });
});

// MTN Mobile Money payment endpoint stub
app.post('/api/pay/mtn', (req, res) => {
  // Integrate MTN Mobile Money payment logic here
  res.json({ message: 'MTN Mobile Money payment integration coming soon.' });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Payments server running on port ${PORT}`);
});

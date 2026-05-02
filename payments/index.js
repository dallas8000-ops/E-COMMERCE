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


// Generic placeholder — the Django site uses manual payment confirmation in admin by default.
app.post('/api/pay/checkout', (req, res) => {
  res.json({
    message:
      'Placeholder: add a third-party gateway here if required. Live flow uses MoMo / bank / WorldRemit with staff verification in Django admin.',
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

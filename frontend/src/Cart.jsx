import React, { useEffect, useMemo, useState } from 'react';

const BASE_CURRENCY = 'USD';
const SUPPORTED_CURRENCIES = ['USD', 'EUR', 'KES', 'UGX'];
const PAYMENT_METHODS = [
  { value: 'mtn', label: 'MTN Mobile Money' },
  { value: 'airtel', label: 'Airtel Money' },
  { value: 'pesapal', label: 'Pesapal' },
];

const FALLBACK_RATES = {
  USD: 1,
  EUR: 0.92,
  KES: 129.5,
  UGX: 3820,
};

function formatAmount(amount, currency) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
    maximumFractionDigits: currency === 'UGX' ? 0 : 2,
  }).format(amount);
}

function Cart() {
  const [currency, setCurrency] = useState('KES');
  const [paymentMethod, setPaymentMethod] = useState('mtn');
  const [rates, setRates] = useState(FALLBACK_RATES);
  const [ratesSource, setRatesSource] = useState('fallback');
  const [ratesUpdatedAt, setRatesUpdatedAt] = useState(null);
  const [paying, setPaying] = useState(false);
  const [result, setResult] = useState(null);

  // Example cart data - replace with real cart state when connected
  const cart = {
    items: [
      { id: 1, name: 'African Print Dress', price: 45, quantity: 1 },
      { id: 3, name: 'Gold Jewelry Set', price: 120, quantity: 1 },
    ],
    total: 165,
  };

  useEffect(() => {
    let cancelled = false;

    async function fetchRates() {
      try {
        const response = await fetch('https://api.frankfurter.app/latest?from=USD&to=EUR,KES,UGX');
        if (!response.ok) {
          throw new Error('Failed to fetch rates');
        }

        const data = await response.json();
        if (cancelled) {
          return;
        }

        setRates({
          USD: 1,
          EUR: data.rates?.EUR ?? FALLBACK_RATES.EUR,
          KES: data.rates?.KES ?? FALLBACK_RATES.KES,
          UGX: data.rates?.UGX ?? FALLBACK_RATES.UGX,
        });
        setRatesSource('live');
        setRatesUpdatedAt(data.date || new Date().toISOString().slice(0, 10));
      } catch {
        if (!cancelled) {
          setRates(FALLBACK_RATES);
          setRatesSource('fallback');
          setRatesUpdatedAt(new Date().toISOString().slice(0, 10));
        }
      }
    }

    fetchRates();
    return () => {
      cancelled = true;
    };
  }, []);

  const convertedItems = useMemo(() => {
    const rate = rates[currency] || 1;
    return cart.items.map((item) => ({
      ...item,
      convertedUnitPrice: item.price * rate,
      convertedLineTotal: item.price * item.quantity * rate,
    }));
  }, [cart.items, currency, rates]);

  const convertedTotal = useMemo(() => {
    const rate = rates[currency] || 1;
    return cart.total * rate;
  }, [cart.total, currency, rates]);

  const selectedMethodLabel = PAYMENT_METHODS.find((method) => method.value === paymentMethod)?.label || paymentMethod;

  const handlePay = async () => {
    setPaying(true);
    setResult(null);
    try {
      const res = await fetch('http://localhost:8000/api/inventory/pay/flutterwave/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          amount: Number(convertedTotal.toFixed(2)),
          currency,
          exchange_rate: rates[currency] || 1,
          base_currency: BASE_CURRENCY,
          payment_method: paymentMethod,
          customer: { email: 'customer@example.com', name: 'Jane Doe' },
          items: convertedItems,
          order_summary: {
            item_count: cart.items.length,
            total_quantity: cart.items.reduce((sum, item) => sum + item.quantity, 0),
          },
        }),
      });
      const data = await res.json();
      setResult({
        ...data,
        uiSummary: `${selectedMethodLabel} selected. ${formatAmount(convertedTotal, currency)} ready for checkout.`,
      });
    } catch {
      setResult({ error: 'Payment failed. Try again.' });
    }
    setPaying(false);
  };

  return (
    <div className="text-center">
      <h2>Your Cart</h2>
      {cart.items.length === 0 ? (
        <p>Your cart is empty. Start shopping!</p>
      ) : (
        <>
          <div className="card p-3 mb-3 text-start shadow-sm">
            <h5 className="mb-3">Order Information</h5>
            <div className="row g-3 align-items-end">
              <div className="col-md-4">
                <label className="form-label mb-1" htmlFor="currencySelect">Currency</label>
                <select id="currencySelect" className="form-select" value={currency} onChange={(event) => setCurrency(event.target.value)}>
                  {SUPPORTED_CURRENCIES.map((code) => (
                    <option key={code} value={code}>{code}</option>
                  ))}
                </select>
              </div>
              <div className="col-md-4">
                <label className="form-label mb-1" htmlFor="paymentMethodSelect">Payment Method</label>
                <select id="paymentMethodSelect" className="form-select" value={paymentMethod} onChange={(event) => setPaymentMethod(event.target.value)}>
                  {PAYMENT_METHODS.map((method) => (
                    <option key={method.value} value={method.value}>{method.label}</option>
                  ))}
                </select>
              </div>
              <div className="col-md-4">
                <small className="text-muted d-block">Rate Source: {ratesSource === 'live' ? 'Live API' : 'Fallback'}</small>
                <small className="text-muted d-block">Updated: {ratesUpdatedAt || 'loading...'}</small>
                <small className="text-muted d-block">1 USD = {rates[currency]?.toFixed(currency === 'UGX' ? 0 : 4)} {currency}</small>
              </div>
            </div>
          </div>

          <ul className="list-group mb-3">
            {convertedItems.map(item => (
              <li className="list-group-item d-flex justify-content-between align-items-center" key={item.id}>
                <span>{item.name} <span className="text-muted">x{item.quantity}</span></span>
                <span>{formatAmount(item.convertedLineTotal, currency)}</span>
              </li>
            ))}
          </ul>

          <div className="card p-3 mb-3 text-start shadow-sm">
            <h5 className="mb-2">Order Summary</h5>
            <div className="d-flex justify-content-between"><span>Items</span><span>{cart.items.length}</span></div>
            <div className="d-flex justify-content-between"><span>Quantity</span><span>{cart.items.reduce((sum, item) => sum + item.quantity, 0)}</span></div>
            <div className="d-flex justify-content-between"><span>Method</span><span>{selectedMethodLabel}</span></div>
            <hr className="my-2" />
            <h4 className="mb-0">Total: {formatAmount(convertedTotal, currency)}</h4>
          </div>

          <button className="btn btn-success mt-3" onClick={handlePay} disabled={paying}>
            {paying ? 'Processing...' : `Pay (${selectedMethodLabel})`}
          </button>
          {result && (
            <div className="mt-3 alert alert-info">
              {result.error ? result.error : (result.uiSummary || result.message)}
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default Cart;

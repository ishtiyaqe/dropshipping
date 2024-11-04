import React, { useEffect, useState } from 'react';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';

import bKashLogo from '../../assets/BKash_Logo.png';
import nagadLogo from '../../assets/nagad-logo.png';
import BankLogo from '../../assets/bank.png';
import WalletLogo from '../../assets/wallet.png';
import OrderSummaryItem from '../cart/OrderSummaryItem';
import clients from '../../components/api/Client';

export default function PaymentForm({ paymentInfo }) {
  const [paymentMethod, setPaymentMethod] = useState('Bkash');
  const [hiddenClass, sethiddenClass] = useState('');
  const [transactionId, setTransactionId] = useState('');
  const [WalletAmount, setWalletAmount] = useState('0');
  const [transactionImage, setTransactionImage] = useState(null);
  const [previewImage, setPreviewImage] = useState(null);
  
  const [bkashNumber, setBkashNumber] = useState('');
  const [nagadNumber, setNagadNumber] = useState('');
  const [bankNumber, setBankNumber] = useState('');
  useEffect(() => {
    clients.get('/api/Payment_numbers/').then(function (res) {
      setBkashNumber(res.data.site_identity.bkash);
      setNagadNumber(res.data.site_identity.Nagad);
      setBankNumber(res.data.site_identity.bank);
      
    });
  
  
  }, [setBkashNumber,])


  const handlePaymentMethodChange = (event) => {
    setPaymentMethod(event.target.value);
  };

  const handleTransactionIdChange = (event) => {
    setTransactionId(event.target.value);
  };

  const handleTransactionImageChange = (event) => {
    const file = event.target.files[0];
    setTransactionImage(file);

    // Create a preview URL for the selected image
    const reader = new FileReader();
    reader.onload = (e) => {
      setPreviewImage(e.target.result);
    };
    reader.readAsDataURL(file);
  };

  // Update the payment details whenever there's a change
  useEffect(() => {
    paymentInfo({
      paymentMethod,
      transactionId,
      transactionImage,
    });
  }, [paymentMethod, transactionId, transactionImage]);
  useEffect(() => {
    if (paymentMethod === 'Wallet') {
      clients.get('/wallet/balance/').then(function (res) {
        if (res.data.wallet_balance) {
          setWalletAmount(res.data.wallet_balance);
          setTransactionId("pay with wallet amount")
        }
      });
      sethiddenClass('hidden');
    } else {
      sethiddenClass('');

    }
  }, [paymentMethod]);

  const renderPaymentDetails = () => {
    if (paymentMethod === 'Bkash') {
      return (
        <div>
          <Typography variant="h6" gutterBottom>
            Bkash Details
          </Typography>
          <p>Instructions for Bkash payment:</p>
          <p>1. Go to Send Money Option.</p>
          <p>2. Type This Number " {bkashNumber} ".</p>
          <p>3. Enter Your Total Order Payment Amount.</p>
          <p>4. Reference Should Be Your Name Or Username else Leave Blank.</p>
          <p>5. Complete the process and copy the Transaction ID.</p>
        </div>
      );
    } else if (paymentMethod === 'Nagad') {
      // Add instructions for Nagad payment here
      return (
        <div>
          <Typography variant="h6" gutterBottom>
            Nagad Details
          </Typography>
          <p>Instructions for Nagad payment:</p>
          <p>1. Go to Send Money Option.</p>
          <p>2. Type This Number " {nagadNumber} ".</p>
          <p>3. Enter Your Total Order Payment Amount.</p>
          <p>4. Reference Should Be Your Name Or Username else Leave Blank.</p>
          <p>5. Complete the process and copy the Transaction ID.</p>
        </div>
      );
    } else if (paymentMethod === 'Bank') {
      // Add instructions for Bank payment here
      return (
        <div>
          <Typography variant="h6" gutterBottom>
            Bank Details
          </Typography>
          {/* Add Bank payment instructions */}
          <p> Bank Details:</p>
          <p>{bankNumber} </p>
          
        </div>
      );
    } else if (paymentMethod === 'Wallet') {
    
      return (
        <div>
          <Typography variant="h6" gutterBottom>
<div className="flex justify-between">
<span>

            Wallet Amount:
</span>
<span>

          ৳  {WalletAmount}
</span>
</div>
          </Typography>
          {/* Add Wallet payment instructions */}
        </div>
      );
    }
  };

  return (
    <React.Fragment>
      <div>
        <OrderSummaryItem />
      </div>
      <div className="border rounded-md shadow-md p-4">
        <Typography variant="h6" gutterBottom>
          Payment method
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Select
              required
              className="flex justify-center"
              id="paymentMethod"
              label="Payment Method"
              fullWidth
              variant="standard"
              name="t_m"
              value={paymentMethod}
              onChange={handlePaymentMethodChange}
            >
              <MenuItem value="Bkash">
                <img className="w-16 h-auto" src={bKashLogo} alt="" /> 
              </MenuItem>
              <MenuItem value="Nagad">
                <img className="w-16 h-auto" src={nagadLogo} alt="" /> 
              </MenuItem>
              <MenuItem value="Bank">
                <img className="w-16 h-auto" src={BankLogo} alt="" />
              </MenuItem>
              <MenuItem value="Wallet">
                <img className="w-16 h-auto" src={WalletLogo} alt="" /> 
              </MenuItem>
            </Select>
          </Grid>
          <Grid item xs={12} md={6}>
            {renderPaymentDetails()}
          </Grid>
          <Grid className={hiddenClass} item xs={12} md={6}>
            <TextField
              required
              id="transactionId"
              label="Transaction ID"
              fullWidth
              variant="standard"
              name="t_id"
              value={transactionId}
              onChange={handleTransactionIdChange}
            />
          </Grid>
          <Grid className={hiddenClass} item xs={12} md={6}>
            <input
              type="file"
              id="transactionImage"
              accept="image/*"
              className='overflow-hidden'
              onChange={handleTransactionImageChange}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            {previewImage && (
              <img src={previewImage} alt={paymentMethod} className="w-16 h-16" />
            )}
          </Grid>
        </Grid>
      </div>
    </React.Fragment>
  );
}

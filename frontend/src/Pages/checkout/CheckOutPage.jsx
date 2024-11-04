// CheckoutPage.js
import React, { useEffect, useState } from 'react';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Paper from '@mui/material/Paper';
import Stepper from '@mui/material/Stepper';
import Step from '@mui/material/Step';
import StepLabel from '@mui/material/StepLabel';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import AddressForm from './AddressForm';
import PaymentForm from './PaymentForm';
import Review from './Review';
import LoginPopup  from '../auth/LoginPopupPage'
import clients from '../../components/api/Client';
import { Link, useNavigate } from 'react-router-dom';
import { useCart } from 'react-use-cart';
const steps = ['Shipping address', 'Payment details', 'Review your order'];
import Confetti from 'react-confetti';
import emptyshoppingcart from '../../assets/empty-shopping-cart.webm'

export default function CheckoutPage() {
  const [activeStep, setActiveStep] = useState(0);
  const [address, setAddress] = useState(''); // State to store the address
  const [orderId, setorderId] = useState(''); // State to store the address
  const [payInfo, setPayInfo] = useState(''); // State to store payment information
  const [isNextButtonDisabled, setIsNextButtonDisabled] = useState(true);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showLoginPopup, setShowLoginPopup] = useState(false);
  
  const navigate = useNavigate();
  const {
    items,
    cartTotal,
    emptyCart
  } = useCart();
  useEffect(() => {
    clients.get("/api/user")
      .then(function (res) {
        setIsLoggedIn(true);
      })
      .catch(function (error) {
        setIsLoggedIn(false);
        navigate('/login');
      });
      
  }, [isLoggedIn]);
  useEffect(() => {
    // Check if all required fields are filled
    if (activeStep === 0) {
      setIsNextButtonDisabled(!addressIsValid());
    } else if (activeStep === 1) {
      setIsNextButtonDisabled(!paymentInfoIsValid());
    }
  }, [activeStep, address, payInfo]);

  const addressIsValid = () => {
    return address.full_name && address.address;
  };

  const paymentInfoIsValid = () => {
    return payInfo.paymentMethod && payInfo.transactionId && cartTotal > 0;
  };
  const handleNext = () => {
    setActiveStep(activeStep + 1);
  };

  const handleBack = () => {
    setActiveStep(activeStep - 1);
  };

  // Function to update the address based on payment data
  const updateAddress = (newAddress) => {
    setAddress(newAddress);
  };

  // Function to update payment information
  const paymentInfo = (paymentInfo) => {
    setPayInfo(paymentInfo);
  };

  const getStepContent = (step) => {
    switch (step) {
      case 0:
        return <AddressForm setAddress={updateAddress} />;
      case 1:
        return <PaymentForm paymentInfo={paymentInfo} />;
      case 2:
        return <Review address={address} payInfo={payInfo} />;
      default:
        throw new Error('Unknown step');
    }
  };
  const handleSubmit = async () => {
    // Calculate payable and due amounts
    const twentyPercent = 0.2; // 20% expressed as a decimal
    const totalPayableNow = cartTotal * twentyPercent;
    const payableNow = cartTotal - totalPayableNow;
    const dueAmount = cartTotal - payableNow;


    // Create an array to store product data
    const products = items.map(item => {
      const sizeText = item.sizesAndColors.map(sizeInfo => `color: ${sizeInfo.color || sizeInfo.material}, size: ${sizeInfo.size}, price:${sizeInfo.price}`).join(',/n');
    
      return {
        product_id: item.id,
        product_no: item.product_no,
        name: item.name,
        image: item.imageLink,
        price: item.price,
        quantity: item.quantity,
        size: sizeText,
        note: 'Note',
      };
    });
    
    console.log(items)

    // Create a data structure that matches the APIView's expected format
    const requestData = {
      t_m: payInfo.paymentMethod,
      paid: payableNow,
      due: dueAmount,
      addess: address.address,
      phone: address.phone,
      products,
      // Add other form data here
    };
    try {
      const response = await clients.post('/api/complete-order/', requestData);

      if (response.status === 200) {
        const responseData = response.data;
        setorderId(responseData.order_id)
        console.log('Order submitted successfully. Order ID:', responseData.order_id);
        // Add any success handling here
        emptyCart()
      } else {
        console.error('Failed to submit the order.');
        // Add error handling here
      }


    } catch (error) {
      console.error('An error occurred while submitting the order:', error);
      // Add error handling here
    }
  };

  return (
    <React.Fragment>
      
          <Container  component="main" maxWidth="lg" sx={{ mb: 4 }}>
          <div className=' p-4  rounded-md shadow-md dark:shadow-gray-400 m-4'  >
            <Typography component="h1" variant="h4" align="center">
              Checkout
            </Typography>
            <Stepper  activeStep={activeStep} sx={{ pt: 3, pb: 5 }}>
              {steps.map((label) => (
                <Step   key={label}>
                  <StepLabel>{label}</StepLabel>
                </Step>
              ))}
            </Stepper>
            {activeStep === steps.length ? (
              <React.Fragment>
                <Typography variant="h5" gutterBottom>
                  Thank you for your order.
                </Typography>
                <Typography variant="subtitle1">
                  Your order number is #{orderId}. We have emailed your order
                  confirmation, and will send you an update when your order has
                  shipped.
                </Typography>
                <div className='flex justify-evenly'>
                  <Link to='/myaccount/order'>
                  <button className='p-4 theme_color theme_colorl w-32 text-center shadow-md rounded-md dark:shadow-gray-400 text-white font-semibold'>My Orders</button>
                  </Link>
                  <Link to='/store'>
                  <button className='p-4 theme_color theme_colorl w-32 text-center shadow-md rounded-md dark:shadow-gray-400 text-white font-semibold'>Shop</button>
                  </Link>
                  </div>
                <Confetti width={window.innerWidth} height={window.innerHeight} />
              </React.Fragment>
            ) : (
              <React.Fragment>
                {getStepContent(activeStep)}
                <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
                  {activeStep !== 0 && (
                    <button className='mt-2 mr-2' onClick={handleBack} >
                      Back
                    </button>
                  )}
                   <button
               
                className={`p-2 mt-2 ml-2 rounded-md shadow-md ${isNextButtonDisabled ? 'bg-gray-200' : 'theme_color theme_colorl'}`}
                disabled={isNextButtonDisabled}
                onClick={() => {
                  if (activeStep === steps.length - 1) {
                    handleSubmit();
                    handleNext();
                  } else {
                    handleNext();
                  }
                }}
              >
                {activeStep === steps.length - 1 ? 'Place order' : 'Next'}
              </button>
                </Box>
              </React.Fragment>
            )}
          </div>
        </Container>
     
    </React.Fragment>
  );
  
}

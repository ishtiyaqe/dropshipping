import  { useEffect, useState } from 'react';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';

import bKashLogo from '../../../assets/BKash_Logo.png';
import nagadLogo from '../../../assets/nagad-logo.png';
import BankLogo from '../../../assets/bank.png';
import WalletLogo from '../../../assets/wallet.png';
import clients from '../../../components/api/client';
import OrderPaySUccessFUllPage from './OrderPaySUccessFUllPage';

const OrderDetailsPopup = ({ data, onClose }) => {
    const [paymentMethod, setPaymentMethod] = useState('Bkash');
    const [hiddenClass, sethiddenClass] = useState('');
    const [transactionId, setTransactionId] = useState('');
    const [WalletAmount, setWalletAmount] = useState('0');
    const [PaySuccessMessage, setPaySuccessMessage] = useState('');
    const [isPopupVisible, setIsPopupVisible] = useState(false); // State to manage popup visibility




    const handlePaymentMethodChange = (event) => {
        setPaymentMethod(event.target.value);
    };

    const handleTransactionIdChange = (event) => {
        setTransactionId(event.target.value);
    };

  
    const handleSubmit = async (e) => {
        e.preventDefault();
    
        const id = data.order.id; // Assuming 'data' contains the order details
        const amount = data.total.toFixed(2); // Use the 'Due' value from your data
        const t_m = paymentMethod;
        const t_id = transactionId;
        const t_imgInput = document.getElementById('transactionImage');
        const t_img = t_imgInput.files.length > 0 ? t_imgInput.files[0] : null;
    
        const formData = new FormData();
        formData.append('amount', amount);
        formData.append('t_m', t_m);
        formData.append('t_id', t_id);

    
        // You may also need to add additional form data like first_name, last_name, phone, and address to 'formData'
        if (t_img) {  // Only append 't_img' if a file has been selected
            formData.append('t_img', t_img);
        }
        // Send the data to the server
        clients.post(`api/paynowreq/${id}/`, formData)
            .then(function (res) {
                
                setPaySuccessMessage(res.data.message)
                if (res.data.message === 'Payment Successfull. Wait for the confirmation. We will notify you.'){
                    setIsPopupVisible(true);
                }
            })
            .catch(function (error) {
                console.error(error);
            });
    };
    

    // Update the payment details whenever there's 
    useEffect(() => {
        if (paymentMethod === 'wallet') {
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
                    <p>Bkash Personal Number: " 01******** ".</p>
                </div>
            );
        } else if (paymentMethod === 'Nagad') {
            // Add instructions for Nagad payment here
            return (
                <div>
                    <Typography variant="h6" gutterBottom>
                        Nagad Details
                    </Typography>
                    {/* Add Nagad payment instructions */}
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
        <div className="fixed inset-0 z-50 flex items-center justify-center backdrop-blur-sm ">
             {isPopupVisible && (
        <>

          <OrderPaySUccessFUllPage data={PaySuccessMessage}  />
        
        </>

      )}
            <div className="order-details-popup  border rounded-md  shadow-md dark:shadow-gray-200 bg-white w-96 p-4 text-black">
                <div className="popup-content">
                    <h2 className="flex justify-between">
                        <span className="self-center text-xl">Due Payment</span>
                        <button
                            className="rounded-md shadow-md dark:shadow-gray-200 bg-red-600 text-white p-1"
                            onClick={onClose}
                        >
                            Close
                        </button>
                    </h2>
                    <div className="text-xs">
                        <strong>Order ID:</strong> {data.order.order_id}
                    </div>
               
                    <div className="text-xs">
                        <strong>Shipping Charge:</strong> {data.charge.toFixed(2)}
                    </div>
                    <div className="text-xs">
                        <strong>Internal Shipping Charge:</strong> {data.internal.toFixed(2)}
                    </div>
                    <div className="text-xs">
                        <strong>Total:</strong> {data.total.toFixed(2)}
                    </div>
                </div>
                <div className="   overflow-hidden">
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
                        <Grid item>
                            {renderPaymentDetails()}
                        </Grid>
                        <Grid className={hiddenClass} item >
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
                            />
                        </Grid>

                    </Grid>
                </div>
                    <button  onClick={handleSubmit}>
                <div className="paynow p-2 text-center text-yellow-60 rounded-md shadow-md border text-white border-gray-200 theme_color theme_colorl  w-full">
                        Pay Now
                </div>
                    </button>
            </div>
        </div>
    );
};

export default OrderDetailsPopup;

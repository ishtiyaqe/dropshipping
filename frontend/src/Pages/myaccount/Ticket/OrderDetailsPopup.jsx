import { useEffect, useState } from 'react';
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


    const [subject, setSubject] = useState('');
    const [message, setMessage] = useState('');





    const handleCreateTicket  = async (e) => {
        e.preventDefault();



        // Send the data to the server
        clients.post(`/TIketost/`, {
            subject,
            message,
        })
            .then(function (res) {
    
                const newTicket = res.data.message;
    
    
                // Optional: Perform any additional actions or update state
                // ...
    
                setPaySuccessMessage(newTicket);
              
                setIsPopupVisible(true)
                // Clear form fields
                setSubject('');
                setMessage('');
            })
            .catch(function (error) {
                console.error(error);
            });
    }





return (
    <div className="fixed inset-0 z-50 flex items-center justify-center backdrop-blur-sm ">
        {isPopupVisible && (
            <>

                <OrderPaySUccessFUllPage data={PaySuccessMessage}  />

            </>

        )}
        <div className="order-details-popup  border rounded-md  shadow-md dark:shadow-gray-200 bg-white w-96 p-4 text-black">
            <div className="popup-content">
                <label>
                    Subject:*
                    <select required className='p-2 bg-white border rounded-md shadow-md w-full' value={subject} onChange={(e) => setSubject(e.target.value)}>
                        <option value="">Select Subject</option>
                        <option value="Return Product">Return Product</option>
                        <option value="General">General</option>
                        <option value="Missing Product">Missing Product</option>
                        <option value="Purchasing">Purchasing</option>
                        <option value="Delivery">Delivery</option>
                        <option value="Refund">Refund</option>
                        <option value="Payment">Payment</option>
                        <option value="Technical">Technical</option>
                        <option value="Discount/Coupon/Campaign issue">Discount/Coupon/Campaign issue</option>
                    </select>
                </label>
                <br />
                <label>
                    Message:*
                    <textarea required className='p-2 bg-white border rounded-md shadow-md w-full' value={message} onChange={(e) => setMessage(e.target.value)} />
                </label>
            </div>
            <button className='p-2 flex justify-center theme_color theme_colorl m-auto mt-4 text-white rounded-md shadow-md' onClick={handleCreateTicket}>Create Ticket</button>

        </div>
    </div>
)};



export default OrderDetailsPopup;

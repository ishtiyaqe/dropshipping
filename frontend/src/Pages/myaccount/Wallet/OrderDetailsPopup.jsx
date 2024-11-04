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


    const [amount, setAmount] = useState('');
    const [note, setNote] = useState('');
    const [t_m, setT_M] = useState('Bkash');  // Assuming 'Bkash' is the default payment method
    const [t_id, setT_Id] = useState('');  // Assuming 'Bkash' is the default payment method
  




    const handleCreateTicket  = async (e) => {
        e.preventDefault();



        // Send the data to the server
        clients.post(`wallet/balance/`, {
            amount,
        note,
        t_m,
        t_id,
        })
            .then(function (res) {
    
                const newTicket = res.data.message;
    
    
                // Optional: Perform any additional actions or update state
                // ...
    
                setPaySuccessMessage(newTicket);
              
                setIsPopupVisible(true)
                setAmount('');
      setNote('');
      setT_Id('');
      setT_M('Bkash');  // Resetting payment method to default
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
        Amount:*
        <input type="number" className='bg-white  p-2 w-full border m-1 rounded-md shadow-md' required value={amount} onChange={(e) => setAmount(e.target.value)} />
      </label>
      <br />
      <label>
        Note:*
        <textarea className='bg-white  p-2 w-full border m-1 rounded-md shadow-md' required value={note} onChange={(e) => setNote(e.target.value)} />
      </label>
      <br />
      <label>
        Payment Method:*
        <select className='bg-white  p-2 w-full border m-1 rounded-md shadow-md' required value={t_m} onChange={(e) => setT_M(e.target.value)}>
          <option value="Bkash">Bkash</option>
          <option value="Nagad">Nagad</option>
          <option value="Cash Pay">Cash Pay</option>
          <option value="Bank">Bank</option>
          <option value="Order Payment">Order Payment</option>
        </select>
      </label>
      <br />
      <label>
        Transaction ID:*
        <input className='bg-white  p-2 w-full border m-1 rounded-md shadow-md' required value={t_id} onChange={(e) => setT_Id(e.target.value)} />
      </label>
            </div>
            <button className='p-2 flex justify-center theme_color theme_colorl m-auto mt-4 text-white rounded-md shadow-md' onClick={handleCreateTicket}>Add Fund</button>

        </div>
    </div>
)};



export default OrderDetailsPopup;

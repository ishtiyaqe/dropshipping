


import { useEffect, useState } from 'react';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import EditLocationAltTwoToneIcon from '@mui/icons-material/EditLocationAltTwoTone';
import bKashLogo from '../../../assets/BKash_Logo.png';
import nagadLogo from '../../../assets/nagad-logo.png';
import BankLogo from '../../../assets/bank.png';
import WalletLogo from '../../../assets/wallet.png';
import clients from '../../../components/api/client';
import OrderPaySUccessFUllPage from './OrderPaySUccessFUllPage';

const DeliveryFormPage = ({ data, onClose }) => {
  const [deliveryCity, setDeliveryCity] = useState('Inside Dhaka'); // Assuming a default value
  const [isPopupVisible, setIsPopupVisible] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [PaySuccessMessage, setPaySuccessMessage] = useState('');
  const [formData, setFormData] = useState({
    full_name: '',
    phone: '',
    address: '',
  });

  useEffect(() => {
    clients.get("/api/user/profile/")
      .then(function (res) {
        const userProfile = res.data.user;
        setFormData(userProfile);
      })
      .catch(function (error) {
        setIsEditing(isEditing);
      });
  }, []);






  const handleDeliveryCityChange = (event) => {
    setDeliveryCity(event.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const id = data.order.shipping_id;

    const fData = new FormData();
    fData.append('orderi', id);
    fData.append('Name', formData.full_name); // Assuming 'Name' corresponds to first_name
    fData.append('Address', formData.address);
    fData.append('Phone', formData.phone);
    fData.append('Phone2', ''); // You may adjust this based on your requirements
    fData.append('city', deliveryCity);

    // Add additional fields as needed

    // Send the data to the server
    clients.post(`/ShippingOrderDeliveryRequest/${id}`, fData)
      .then(function (res) {
        setPaySuccessMessage(res.data.detail);
        if (res.data.detail === 'Delivery information added successfully.') {
          setIsPopupVisible(true);
        }
      })
      .catch(function (error) {
        console.error(error);
      });
  };

  const toggleEditing = () => {
    setIsEditing(!isEditing);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center backdrop-blur-sm ">
      {isPopupVisible && (
        <>
          <OrderPaySUccessFUllPage data={PaySuccessMessage} />
        </>
      )}
      <div className="order-details-popup  border rounded-md  shadow-md dark:shadow-gray-200 bg-white w-96 p-4 text-black">
        <div className="popup-content">
          <h2 className="flex justify-between">
            <span className="self-center text-xl">Delivery Request</span>
            <button
              className="rounded-md shadow-md dark:shadow-gray-200 bg-red-600 text-white p-1"
              onClick={onClose}
            >
              Close
            </button>
          </h2>
          <div className="text-xs">
            <strong>Order ID:</strong> {data.order.shipping_id}
          </div>
          <div className="text-xs">
            <strong>Delivery Charge:</strong> Inside Dhaka Cash on Delivery && Outside Dhaka City Sundarban courier delivery Charge need to pay.
          </div>
        </div>
        <div className="overflow-hidden">
          <Typography variant="h6" gutterBottom>
            Delivery Details
          </Typography>
          {isEditing ? (
                   <Grid container spacing={3}>
                   <Grid item xs={12} md={6}>
                       {/* Add a dropdown to select delivery city */}
                       <Select
                           required
                           className="flex justify-center"
                           id="deliveryCity"
                           label="Delivery City"
                           fullWidth
                           variant="standard"
                           name="city"
                           value={deliveryCity}
                           onChange={handleDeliveryCityChange}
                       >
                           <MenuItem value="Inside Dhaka">Inside Dhaka</MenuItem>
                           <MenuItem value="Outside Dhaka">Outside Dhaka</MenuItem>
                       </Select>
                   </Grid>
                   <Grid item xs={12} md={6}>
                       {/* Add fields for delivery details */}
                       <TextField
                           required
                           id="deliveryName"
                           label="Name"
                           fullWidth
                           variant="standard"
                           name="name"
                           value={deliveryName}
                           onChange={handleDeliveryNameChange}
                       />
                       <TextField
                           required
                           id="deliveryAddress"
                           label="Address"
                           fullWidth
                           variant="standard"
                           name="address"
                           value={deliveryAddress}
                           onChange={handleDeliveryAddressChange}
                       />
                       <TextField
                           required
                           id="deliveryPhone"
                           label="Phone"
                           fullWidth
                           variant="standard"
                           name="phone"
                           value={deliveryPhone}
                           onChange={handleDeliveryPhoneChange}
                       />
                       {/* Add an optional field for secondary phone */}
                       <TextField
                           id="deliveryPhone2"
                           label="Secondary Phone"
                           fullWidth
                           variant="standard"
                           name="phone2"
                           value={deliveryPhone2}
                           onChange={handleDeliveryPhone2Change}
                       />
                   </Grid>
                   
               </Grid>
               
                    ):(
                        <div className="band    p-4 rounded-md shadow-md mt-2 font-semibold text-md">
                        <div className='flex justify-between w-18'>
                          <div className="p-2">
                            <p>
                              First Name:<span>&nbsp;&nbsp;{formData.full_name}</span>
                            </p>
                            <p>
                              Phone:<span>&nbsp;&nbsp;{formData.phone}</span>
                            </p>
                            <p>
                              Address:<span>&nbsp;&nbsp;{formData.address}</span>
                            </p>
                          </div>
                          <div className="eadit p-4" style={{ cursor: 'pointer' }} onClick={toggleEditing}>
                            <EditLocationAltTwoToneIcon />
                          </div>
                        </div>
                      </div>  
                    )}
        </div>
        <button onClick={handleSubmit}>
          <div className="paynow p-2 text-center text-yellow-60 rounded-md shadow-md border text-white border-gray-200 theme_color theme_colorl  w-full">
            Request a Delivery
          </div>
        </button>
      </div>
    </div>
  );
};

export default DeliveryFormPage;

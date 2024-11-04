import React, { useEffect, useState } from 'react';
import EditLocationAltTwoToneIcon from '@mui/icons-material/EditLocationAltTwoTone';
import TextField from '@mui/material/TextField';
import Box from '@mui/system/Box';
import FormControlLabel from '@mui/material/FormControlLabel';
import { Button } from 'antd';
import LocalShippingOutlinedIcon from '@mui/icons-material/LocalShippingOutlined';
import PaidOutlinedIcon from '@mui/icons-material/PaidOutlined';
import ShoppingBasketTwoToneIcon from '@mui/icons-material/ShoppingBasketTwoTone';
import StoreTwoToneIcon from '@mui/icons-material/StoreTwoTone';
import RocketLaunchTwoToneIcon from '@mui/icons-material/RocketLaunchTwoTone';
import SummarizeTwoToneIcon from '@mui/icons-material/SummarizeTwoTone';
import clients from '../../../components/api/Client';
import { Link } from 'react-router-dom';
import LoadingBar from 'react-top-loading-bar'

const Dashboard = () => {
  const [progress, setProgress] = useState(0)
  const [isEditing, setIsEditing] = useState(false);
  const [totalOrder, setTotalOrder] = useState('0');
  const [totalShipping, setTotalShipping] = useState('0');
  const [totalReqOrder, setTotalReqOrder] = useState('0');
  const [totalOpenTiket, setTotalOpenTiket] = useState('0');
  const [profile, setProfile] = useState({
    full_name: '',
    phone: '',
    address: '',
  });

  useEffect(() => {
    setProgress(10);
    clients.get("/api/user/profile/")
    .then((res) => {
        setProgress(50);
        const userProfile = res.data.user;
        setProfile(userProfile);
        setProgress(100);
      })
      .catch(() => {
        setProgress(50);
        setIsEditing(true);
        setProgress(100);
      });

    clients.get("/api/total-order-products/")
      .then((res) => {
        const totalAmount = res.data.total_orders;
        setTotalOrder(totalAmount);
      })
      .catch(() => {
        setTotalOrder('0');
      });

    clients.get("/api/TotalShipingCount/")
      .then((res) => {
        const totalAmount = res.data.total_orders;
        setTotalShipping(totalAmount);
      })
      .catch(() => {
        setTotalOrder('0');
      });

    clients.get("/api/sticketCount/")
      .then((res) => {
        const totalAmount = res.data.total_orders;
        setTotalOpenTiket(totalAmount);
      })
      .catch(() => {
        setTotalOrder('0');
      });

    clients.get("/api/reqorder/")
      .then((res) => {
        const totalAmount = res.data.recount;
        setTotalReqOrder(totalAmount);
      })
      .catch(() => {
        setTotalReqOrder('0');
      });
  }, []);

  const toggleEditing = () => {
    setIsEditing(!isEditing);
  };

  const submitUserProfile = (e) => {
    e.preventDefault();
    clients.post("/api/user/profile/", profile)
      .then(() => {
        setIsEditing(false);
      })
      .catch((error) => {
        
      });
  }

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setProfile({ ...profile, [name]: value });
  };

  return (
    <div className='w-fill'>
       <LoadingBar
        color='#f11946'
        progress={progress}
        onLoaderFinished={() => setProgress(0)}
      />
      {isEditing ? (
        <div>
          <Box component="form" noValidate onSubmit={submitUserProfile} sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              name="full_name"
              label="First Name"
              id="full_name"
              value={profile.full_name}
              onChange={handleInputChange}
              autoComplete="first-name"
            />


            <TextField
              margin="normal"
              required
              fullWidth
              name="phone"
              label="Phone Number"
              id="phone"
              value={profile.phone}
              onChange={handleInputChange}
              autoComplete="tel"
            />

            <TextField
              margin="normal"
              required
              fullWidth
              name="address"
              label="Address"
              id="address"
              value={profile.address}
              onChange={handleInputChange}
              autoComplete="address"
            />

            <button className='theme_color theme_colorl p-4 w-full rounded-lg shadow-md text-white text-xl font-semibold' type="submit">Update Profile</button>
          </Box>
        </div>
      ) : (
        <div>
          <div className='grid grid-cols-2 lg:grid-cols-4 lg:gap-12 gap-4 p-2 w-92'>
            <Link to="/myaccount/order">
              <button className='lg:p-6 p-8 flex justify-center flex-col w-full h-32 text-white dark:shadow-gray-400 font-semibold text-xl text-center self-center rounded-md shadow-md bg-gradient-to-r from-lime-600 to-lime-400'>
                <ShoppingBasketTwoToneIcon className='text-white self-center' />
                <span className='text-sm whitespace-nowrap self-center'>Total Order:</span>
                <span className='self-center'>{totalOrder}</span>
              </button>
            </Link>
            <Link to="/myaccount/Request-Orders">
              <button className='lg:p-6 p-8 flex justify-center flex-col w-full h-32 text-white dark:shadow-gray-400 font-semibold text-xl text-center self-center rounded-md shadow-md bg-gradient-to-r from-green-600 to-green-400'>
                <StoreTwoToneIcon className='text-white self-center' />
                <span className='text-sm whitespace-nowrap self-center'>Total Request Order:</span>
                <span className='self-center'>{totalReqOrder}</span>
              </button>
            </Link>

            <div className='lg:p-6 p-8 flex justify-center flex-col w-full h-32 text-white dark:shadow-gray-400 font-semibold text-xl text-center self-center rounded-md shadow-md bg-gradient-to-r from-sky-600 to-sky-400'>
              <RocketLaunchTwoToneIcon className='text-white self-center' />
              <span className='text-sm whitespace-nowrap self-center'>Total Shipping: </span>
              <span className='self-center'>{totalShipping}</span>
            </div>
            <div className='lg:p-6 p-8 flex justify-center flex-col w-full h-32 text-white dark:shadow-gray-400 font-semibold text-xl text-center self-center rounded-md shadow-md bg-gradient-to-r from-blue-600 to-blue-400'>
              <SummarizeTwoToneIcon className='text-white self-center' />
              <span className='text-sm whitespace-nowrap self-center'>Open Ticket: </span>
              <span className='self-center'>{totalOpenTiket}</span>
            </div>
          </div>

          <div className="border dark:shadow-gray-400 p-4 rounded-md shadow-md mt-2 font-semibold text-md">
            <span className=''><LocalShippingOutlinedIcon className='text-orange-600' /> Delivery Details:</span>

            <div className='flex justify-between w-18'>
              <div className="p-2">
                <p>
                  First Name:<span>&nbsp;&nbsp;{profile.full_name}</span>
                </p>
                
                <p>
                  Phone:<span>&nbsp;&nbsp;{profile.phone}</span>
                </p>
                <p>
                  Address:<span>&nbsp;&nbsp;{profile.address}</span>
                </p>
              </div>
              <div className="eadit p-4" style={{ cursor: 'pointer' }} onClick={toggleEditing}>
                <EditLocationAltTwoToneIcon />
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;


import Divider from '@mui/material/Divider';
import Paper from '@mui/material/Paper';
import MenuList from '@mui/material/MenuList';
import MenuItem from '@mui/material/MenuItem';
import ListItemText from '@mui/material/ListItemText';
import ExitToAppTwoToneIcon from '@mui/icons-material/ExitToAppTwoTone';
import { Outlet, Link, useLocation } from 'react-router-dom';
import { deepOrange, deepPurple } from '@mui/material/colors';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import DashboardTwoToneIcon from '@mui/icons-material/DashboardTwoTone';
import ShoppingBasketTwoToneIcon from '@mui/icons-material/ShoppingBasketTwoTone';
import StoreTwoToneIcon from '@mui/icons-material/StoreTwoTone';
import RocketLaunchTwoToneIcon from '@mui/icons-material/RocketLaunchTwoTone';
import LocalShippingTwoToneIcon from '@mui/icons-material/LocalShippingTwoTone';
import SummarizeTwoToneIcon from '@mui/icons-material/SummarizeTwoTone';
import clients from '../../components/api/Client';
import Avatar from '@mui/material/Avatar';
import CreditScoreIcon from '@mui/icons-material/CreditScore';
import AccountBalanceWalletIcon from '@mui/icons-material/AccountBalanceWallet';


export default function IconMenu() {
  const [currentUser, setCurrentUser] = useState();
  const [fullName, setfullName] = useState('');
  const [fullNamefirstw, setfullNamefirstw] = useState('');
  const navigate = useNavigate();
  const location = useLocation();

  const onClick = (e) => {
    
  };

  function submitLogout(e) {
    e.preventDefault();
    clients.post("/api/logout/", { withCredentials: true }).then(function (res) {
      setCurrentUser(false);
      navigate('/login');
    });
  }

  useEffect(() => {
    clients
      .get('/api/user_profiles/')
      .then(function (res) {
        
        setfullName(res.data.full_name)
        setfullNamefirstw(res.data.first_name_initial)
      })
      .catch(function (error) {
        
        navigate('/login');

      });

  }, [])


  return (
    <>
      <div className='flex lg:flex-row flex-col p-4'>
        <div onClick={onClick} className='lg:w-72 w-full h-fit  border  p-4 mb-4 rounded-md shadow-md dark:shadow-gray-400'>
          <div className='flex justify-center flex-col '>
            <Avatar className='shadow-md dark:shadow-gray-200 uppercase' sx={{ bgcolor: deepOrange[500], margin: 'auto' }}>{fullNamefirstw}</Avatar>
            <span className='text-xl font-semibold text-center mt-2 mb-2 uppercase'>{fullName}</span>
          </div>

          <div>
            <div>
              <Link to="/myaccount" className='flex flex-cols space-x-4 text-xl font-semibold self-center mb-2'>
                <div className={` ${location.pathname === '/myaccount' ? 'bg-rose-600 w-2 self-stretch pr-2.5 justify-start items-center inline-flex duration-500 rounded' : 'hidden duration-500'}`}>
                  <div className="w-5 h-5 relative flex-col justify-start items-start flex" />
                </div>
                <DashboardTwoToneIcon className={`self-center ${location.pathname === '/myaccount' ? 'text-rose-500' : 'text-gray-950'}`} />

                <div className={`text-sm self-center ${location.pathname === '/myaccount' ? 'text-rose-500' : 'text-gray-950'}`}>Dashboard</div>
              </Link>
            </div>
            <div>
              <Link to="/myaccount/order" className="flex flex-cols space-x-4 text-xl font-semibold self-center mb-2">
                <div className={` ${location.pathname === '/myaccount/order' ? 'bg-rose-600 w-2 self-stretch pr-2.5 justify-start items-center inline-flex duration-500 rounded' : 'hidden duration-500'}`}>
                  <div className="w-5 h-5 relative flex-col justify-start items-start flex" />
                </div>
                <ShoppingBasketTwoToneIcon className={`${location.pathname === '/myaccount/order' ? 'text-rose-500' : 'text-gray-950'}`} />
                <div className={`text-sm self-center ${location.pathname === '/myaccount/order' ? 'text-rose-500' : 'text-gray-950'}`}>Orders</div>
              </Link>
            </div>
            <div>
              <Link to="/myaccount/Request-Orders" className="flex flex-cols space-x-4 text-xl font-semibold self-center mb-2">
                <div className={` ${location.pathname === '/myaccount/Request-Orders' ? 'bg-rose-600 w-2 self-stretch pr-2.5 justify-start items-center inline-flex duration-500 rounded' : 'hidden duration-500'}`}>
                  <div className="w-5 h-5 relative flex-col justify-start items-start flex" />
                </div>
                <div className='self-center'>
                  <StoreTwoToneIcon className={`${location.pathname === '/myaccount/Request-Orders' ? 'text-rose-500' : 'text-gray-950'}`} />
                </div>

                <div className={`text-sm self-center ${location.pathname === '/myaccount/Request-Orders' ? 'text-rose-500' : 'text-gray-950'}`}>Request Orders</div>
              </Link>
            </div>
            <div>
              <Link to="/myaccount/Shipping-Request" className="flex flex-cols space-x-4 text-xl font-semibold self-center mb-2">
                <div className={` ${location.pathname === '/myaccount/Shipping-Request' ? 'bg-rose-600 w-2 self-stretch pr-2.5 justify-start items-center inline-flex duration-500 rounded' : 'hidden duration-500'}`}>
                  <div className="w-5 h-5 relative flex-col justify-start items-start flex" />
                </div>
                <div className='self-center'>
                  <RocketLaunchTwoToneIcon className={`${location.pathname === '/myaccount/Shipping-Request' ? 'text-rose-500' : 'text-gray-950'}`} />
                </div>
                <div className={`text-sm self-center ${location.pathname === '/myaccount/Shipping-Request' ? 'text-rose-500' : 'text-gray-950'}`}>Shipping Request</div>
              </Link>
            </div>
            <div>
              <Link to="/myaccount/Payment-Request" className="flex flex-cols space-x-4 text-xl font-semibold self-center mb-2">
                <div className={` ${location.pathname === '/myaccount/Payment-Request' ? 'bg-rose-600 w-2 self-stretch pr-2.5 justify-start items-center inline-flex duration-500 rounded' : 'hidden duration-500'}`}>
                  <div className="w-5 h-5 relative flex-col justify-start items-start flex" />
                </div>
                <div className='self-center'>
                  <CreditScoreIcon className={`${location.pathname === '/myaccount/Payment-Request' ? 'text-rose-500' : 'text-gray-950'}`} />
                </div>
                <div className={`text-sm self-center ${location.pathname === '/myaccount/Payment-Request' ? 'text-rose-500' : 'text-gray-950'}`}>Payment Request</div>
              </Link>
            </div>
            <div>
              <Link to="/myaccount/Delivery" className="flex flex-cols space-x-4 text-xl font-semibold self-center mb-2">
                <div className={` ${location.pathname === '/myaccount/Delivery' ? 'bg-rose-600 w-2 self-stretch pr-2.5 justify-start items-center inline-flex duration-500 rounded' : 'hidden duration-500'}`}>
                  <div className="w-5 h-5 relative flex-col justify-start items-start flex" />
                </div>
                <div className='self-center'>
                  <LocalShippingTwoToneIcon className={`${location.pathname === '/myaccount/Delivery' ? 'text-rose-500' : 'text-gray-950'}`} />
                </div>
                <div className={`text-sm self-center ${location.pathname === '/myaccount/Delivery' ? 'text-rose-500' : 'text-gray-950'}`}>Delivery</div>
              </Link>
            </div>
            <div>
              <Link to="/myaccount/Ticket" className="flex flex-cols space-x-4 text-xl font-semibold self-center mb-2">
                <div className={` ${location.pathname === '/myaccount/Ticket' ? 'bg-rose-600 w-2 self-stretch pr-2.5 justify-start items-center inline-flex duration-500 rounded' : 'hidden duration-500'}`}>
                  <div className="w-5 h-5 relative flex-col justify-start items-start flex" />
                </div>
                <div className='self-center'>
                  <SummarizeTwoToneIcon className={`${location.pathname === '/myaccount/Ticket' ? 'text-rose-500' : 'text-gray-950'}`} />
                </div>
                <div className={`text-sm self-center ${location.pathname === '/myaccount/Ticket' ? 'text-rose-500' : 'text-gray-950'}`}>Ticket</div>
              </Link>
            </div>
            <div>
              <Link to="/myaccount/Wallet" className="flex flex-cols space-x-4 text-xl font-semibold self-center mb-2">
                <div className={` ${location.pathname === '/myaccount/Wallet' ? 'bg-rose-600 w-2 self-stretch pr-2.5 justify-start items-center inline-flex duration-500 rounded' : 'hidden duration-500'}`}>
                  <div className="w-5 h-5 relative flex-col justify-start items-start flex" />
                </div>
                <div className='self-center'>
                  <AccountBalanceWalletIcon className={`${location.pathname === '/myaccount/Wallet' ? 'text-rose-500' : 'text-gray-950'}`} />
                </div>
                <div className={`text-sm self-center ${location.pathname === '/myaccount/Wallet' ? 'text-rose-500' : 'text-gray-950'}`}>Wallet</div>
              </Link>
            </div>

            <Divider />
            <div className='flex flex-cols space-x-4  font-semibold mt-2  '>
              <div className='self-center ml-4 '>
                <ExitToAppTwoToneIcon className='text-orange-600' />
              </div>
              <div>
                <form onSubmit={e => submitLogout(e)}>
                  <button type="submit">Log out</button>
                </form>
              </div>
            </div>
          </div>
        </div>
        <div className=' w-fill p-4 h-auto '>
          <Outlet />
        </div>
      </div>
    </>
  );
}

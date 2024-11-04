import {
  EditTwoTone,
  CheckCircleTwoTone,
} from '@ant-design/icons';
import { Menu, Drawer } from 'antd';
import React, { useEffect, useState } from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import SearchBar from './SearchBarComponent';
import StorefrontTwoToneIcon from '@mui/icons-material/StorefrontTwoTone';
import CartComponent from '../../Pages/cart/CartComponent';
import CircleCTABottomNavigation from './CircleCTABottomNavigation';
import AccountCircleTwoTone from '@mui/icons-material/AccountCircleTwoTone';
import { useCart } from 'react-use-cart';
import HomeOutlinedIcon from '@mui/icons-material/HomeOutlined';
import clients from '../api/Client';
import LightModeOutlinedIcon from '@mui/icons-material/LightModeOutlined';
import NightsStayOutlinedIcon from '@mui/icons-material/NightsStayOutlined';
import LockOpenTwoToneIcon from '@mui/icons-material/LockOpenTwoTone';
import VpnKeyTwoToneIcon from '@mui/icons-material/VpnKeyTwoTone';
import Footer from '../../Pages/Footer'
import LocalPhoneIcon from '@mui/icons-material/LocalPhone';
import MailIcon from '@mui/icons-material/Mail';
import LocalMallOutlinedIcon from '@mui/icons-material/LocalMallOutlined';
import ScrollToTop from "react-scroll-to-top";
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';


const Header = () => {
  const [currentUser, setCurrentUser] = useState();
  const [Siteidentity, setSiteidentity] = useState([]);
  const [isDarkMode, setIsDarkMode] = useState(false);


  const {
    items,
    totalItems,
    totalUniqueItems,
    isEmpty,
    cartTotal,
    removeItem
  } = useCart();
  const location = useLocation();




  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
    const root = document.documentElement;

    if (isDarkMode) {
      root.style.setProperty('--text-color', 'rgba(0, 0, 0, 0.87)');
      root.style.setProperty('--background-color', '#f5f5f5');
    } else {
      root.style.setProperty('--text-color', 'rgba(251, 247, 247, 0.87)');
      root.style.setProperty('--background-color', '#242424');
    }
  };

  useEffect(() => {
    clients.get("/api/user")
      .then(function (res) {
        setCurrentUser(true);
      
      })
      .catch(function (error) {
        setCurrentUser(false);
 
      });
    clients.get("/site-identity")
      .then(function (res) {
        setSiteidentity(res.data.site_identity);
       
      })
      .catch(function (error) {
        setCurrentUser(false);
      });
  }, []);


  const [isCartOpen, setIsCartOpen] = useState(false);

  const showCartDrawer = () => {
    setIsCartOpen(true);
  };

  const hideCartDrawer = () => {
    setIsCartOpen(false);
  };
  useEffect(() => {
    renderUserLinks()
  }, [currentUser]);

  const renderUserLinks = () => {
    if (currentUser) {
      return (
        <div key="s">
          <AccountCircleTwoTone />
          <Link to="/myaccount">My Account</Link>
        </div>
      );
    } else {
      return (
        <>

          <div className="flex space-x-2 text-white">
            <div key="r">
              <VpnKeyTwoToneIcon />
              <Link to="/register"> Register</Link>
            </div>
            <div key="l">
              <LockOpenTwoToneIcon />
              <Link to="/login">Login</Link>
            </div>
          </div>
        </>
      );
    }
  };

  return (
    <div >
      <ScrollToTop
        smooth
        style={{ zIndex: '99999999999' }}
        component={<ArrowUpwardIcon />}
        className="theme_color theme_colorl lg:mb-4 mb-16 hover:text-white text-black"
      />


      <div className="w-full h-10 bg-blue-950 text-white">

        <div className="flex  items-center justify-between h-full mx-auto max-w-7xl lg:text-normal text-sm">
          <div className="flex items-center space-x-4 lg:ml-0 ml-2">
            <div className='self-center flex lg:hidden' >
              <Link to="/">
                {Siteidentity.logo ? (
                  <img className='p-2 w-32' src={`https://backend.ecargo.com.bd${Siteidentity.logo}`} alt={Siteidentity.name} />
                ) : (
                  <span>{Siteidentity.name}</span>
                )}
              </Link>

            </div>
            <div className="lg:flex hidden items-center  space-x-4">
              <div className="flex items-center space-x-1">
                <LocalPhoneIcon />
                <span>{Siteidentity.phone}</span>
              </div>
              <div className="flex items-center space-x-1">
                <MailIcon />
                <span>{Siteidentity.mail}</span>
              </div>
            </div>
          </div>
          <div className="flex items-center space-x-4 lg:mr-0 mr-2">
            <Link to="/FAQS">
              <span className="link">FAQ's</span>
            </Link>
            <Link to="/forbidden_list">
              <span className="link">Forbidden Items!!</span>
            </Link>

            <div className="lg:flex hidden ">
              {renderUserLinks()}
            </div>
          </div>
        </div>
      </div>




      <div className={`flex z-40 justify-center pt-4 pb-4 flex-col pl-auto py-2 sticky-nav ${isDarkMode ? 'bg-gray-900' : 'bg-white'}`}>
        <div >
          <div className='flex justify-evenly m-auto  '>
            <div className='self-center lg:flex hidden' key="s">
              <Link to="/">
              {Siteidentity.logo ? (
                  <img className='p-2 w-32' src={`https://backend.ecargo.com.bd${Siteidentity.logo}`} alt={Siteidentity.name} />
                ) : (
                  <span>{Siteidentity.name}</span>
                )}
              </Link>
            </div>
            <div key="se" className='self-center sticky-nav lg:w-1/2 w-full lg:ml-0 ml-6 lg:mr-0 mr-6'>
              <SearchBar />
            </div>
            <div className="lg:flex justify-evenly space-x-2 hidden self-center">
              <div key="h">
                <Link to="/" >
                  <div className={` ${isDarkMode ? 'bg-gray-800' : 'bg-gray-200'} rounded-full  w-12 text-center flex justify-center h-12 `}>
                    <HomeOutlinedIcon className='self-center' />
                  </div>
                </Link>
              </div>
              <div key="sh">
                <Link to="/store"  >
                  <div className={` ${isDarkMode ? 'bg-gray-800' : 'bg-gray-200'} rounded-full  w-12 text-center flex justify-center h-12 `}>
                    <StorefrontTwoToneIcon className='self-center' />
                  </div>
                </Link>
              </div>
              <div>

              </div>
              <div key="c" onClick={showCartDrawer} >
                <div className='relative '>

                  <div className={` ${isDarkMode ? 'bg-gray-800' : 'bg-gray-200'}  rounded-full  w-12 text-center flex justify-center h-12 `}>
                    <LocalMallOutlinedIcon className='self-center' />
                  </div>
                  <div className="absolute theme_color -top-1 -right-1 opecity-75  text-white p-2 rounded-full w-auto h-6 text-xs text-center flex justify-center">
                    <span className='self-center'>{totalItems}</span>
                  </div>
                </div>

              </div>
              <div className={` ${isDarkMode ? 'bg-gray-800' : 'bg-gray-200'} rounded-full  w-12 text-center flex justify-center h-12 `}>
                <button onClick={toggleTheme} className="button-styling ">
                  {isDarkMode ? (
                    <NightsStayOutlinedIcon style={{ color: "white" }} />
                  ) : (
                    <LightModeOutlinedIcon style={{ color: "black" }} />
                  )}
                </button>

              </div>
            </div>
          </div>
        </div>
      </div>

      <div className={`  flex justify-center space-x-4 m-auto p-2 shadow-lg  ${isDarkMode ? 'bg-gray-900 shadow-gray-950' : 'bg-lime-600 shadow-gray-200'}`}>
        <div className="  rounded-md relative lg:text-md text-xs">
          <Link to={'/request-order'}>

            <div className='text-white font-bold text-sm font-serif'>Shop For Me</div>
          </Link>
        </div>
        <div className="  rounded-md relative lg:text-md text-xs">
          <Link to={'/ShipForMe'}>

            <div className='text-white font-bold text-sm font-serif'>Ship For Me</div>
          </Link>
        </div>
        <div className="  rounded-md relative lg:text-md text-xs">
          <Link to={'/PayForMe'}>

            <div className='text-white font-bold text-sm font-serif'>Pay For Me</div>
          </Link>

        </div>


      </div>
      <div >

        <Outlet />
      </div>
      <div>
        <Footer />
      </div>
      <Drawer
        title="Cart"
        placement="right"
        closable={true}
        onClose={hideCartDrawer}
        className="z-50"
        open={isCartOpen}
      >
        <CartComponent closeCart={hideCartDrawer} />
      </Drawer>
      <div className='lg:hidden flex'>
        <CircleCTABottomNavigation isDarkMode={isDarkMode} toggleTheme={toggleTheme} />

      </div>
    </div>
  );
};

export default Header;

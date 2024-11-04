import React, { useEffect, useRef, useState } from "react";
import HomeOutlinedIcon from "@mui/icons-material/HomeOutlined";
import AccountCircleOutlinedIcon from "@mui/icons-material/AccountCircleOutlined";
import ChatBubbleOutlineOutlinedIcon from "@mui/icons-material/ChatBubbleOutlineOutlined";
import ShoppingCartOutlinedIcon from "@mui/icons-material/ShoppingCartOutlined";
import CameraAltOutlinedIcon from "@mui/icons-material/CameraAltOutlined";
import StorefrontTwoToneIcon from '@mui/icons-material/StorefrontTwoTone';
import { Link } from "react-router-dom";
import { Drawer } from "antd";
import CartComponent from "../../Pages/cart/CartComponent";
import LightModeTwoToneIcon from '@mui/icons-material/LightModeTwoTone';
import Brightness4TwoToneIcon from '@mui/icons-material/Brightness4TwoTone';

const Navigation = ({isDarkMode, toggleTheme} ) => {
  const [active, setActive] = useState(0);
  const [isCartOpen, setIsCartOpen] = useState(false);
  
  

  const handleThemeToggle = () => {
    toggleTheme(); // Call the toggleTheme function when the button is clicked
  };
  const showCartDrawer = () => {
    setIsCartOpen(true);
  };

  const hideCartDrawer = () => {
    setIsCartOpen(false);
  };

 

  const menuItems = [
    {
      name: "Home",
      
      icon: <HomeOutlinedIcon />,
      index: 0,
      to: "/",
      onClick: () => {
        
      },
    },
    {
      name: "Cart",
    
      icon: <ShoppingCartOutlinedIcon />,
      index: 1,
      to: "#",
      onClick: () => {
        setIsCartOpen(true);
        
      },
    },
    {
      name: "User",

      icon: <AccountCircleOutlinedIcon />,
      index: 2,
      to: "/myaccount",
      onClick: () => {
        
      },
    },
    {
      name: "Store",

      icon: <StorefrontTwoToneIcon />,
      index: 3,
      to: "/store",
      onClick: () => {
        
      },
    }
  ];

  const handleMenuItemClick = (menuItem) => {
    setActive(menuItem.index);
  };

  return (
    <div className="bg-white fixed bottom-0 w-full max-h-[4.4rem] px-2 rounded-t-xl z-50 flex justify-center  ml-auto p-auto">
      <ul className="grid grid-cols-5 relative w-full gap-2">
       

        {menuItems.map((menuItem) => (
          <li key={menuItem.index} className="w-16">
            <Link to={menuItem.to}>
              <span
                className="flex flex-col text-center pt-6"
                onClick={() => {
                  handleMenuItemClick(menuItem);
                  menuItem.onClick();
                }}
              >
                <span
                  className={`text-xl text-orange-700 cursor-pointer duration-500 ${
                    menuItem.index === active && "-mt-16 theme_color rounded-full shadow-md dark:shadow-gray-400 p-4  z-50"
                  }`}
                >
                  {React.cloneElement(menuItem.icon, {
                    style: {
                      color: menuItem.index === active ? "white" : "orange",
                    },
                  })}
                </span>
                <span
                  className={`${
                    menuItem.index === active
                      ? "translate-y-4 duration-700 opacity-100 text-orange-700"
                      : "opacity-0 translate-y-10"
                  }`}
                >
                  {menuItem.name}
                </span>
              </span>
            </Link>
          </li>
        ))}
        <li className="w-16">
          <div className="flex flex-col text-center pt-6">
          <button onClick={handleThemeToggle} className="button-styling">
        {isDarkMode ? (
            <Brightness4TwoToneIcon style={{ color: "orange" }} />
          ) : (
          <LightModeTwoToneIcon style={{ color: "orange" }} />
        )}
      </button>
          </div>
        </li>
      </ul>
      <Drawer
        title="Cart"
        placement="right"
        closable={true}
        onClose={hideCartDrawer}
        open={isCartOpen}
      >
        <CartComponent closeCart={hideCartDrawer} />
      </Drawer>
    </div>
  );
};

export default Navigation;

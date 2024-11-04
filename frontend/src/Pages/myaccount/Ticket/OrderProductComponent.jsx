import React, { useState } from 'react';
import TimeComponent from '../../../components/FrontendTheme/timeClearComponenet'
import OrderDetailsPage from './OrderDetailsPage';

const OrderProduct = ({ order }) => {

  const [popupDetailsData, setPopupDetailsData] = useState(null); // State to manage popup data
  const [isPopupDetailsVisible, setIsPopupDetailsVisible] = useState(false); // State to manage popup visibility






  const openPopupDetails = (order) => {
    setIsPopupDetailsVisible(true);
    setPopupDetailsData(order)
    
  };


  return (
    <>
   
      <div onClick={() => openPopupDetails(order)}>
      <div className="w-full h-auto p-2 dark:border dark:border-gray-200  rounded-lg shadow grid lg:grid-cols-6 grid-cols-2 gap-4">
      <div className="ml-4    justify-start items-center inline-flex">
          <div className="w-20 h-5  text-base font-semibold font-['Open Sans'] leading-normal">#{order.ticket_no}</div>
        </div>
        <div className=" text-center justify-start items-center inline-flex">
          <div className=" self-center  bg-blue-950 dark:bg-gray-300 bg-opacity-20 rounded-full justify-center items-center inline-flex">
            <div className="w-fit self-center  p-2 text-blue-950 text-sm font-normal font-['Open Sans'] leading-none">{order.status}</div>
          </div>
        </div>
        <div className="    justify-start items-center inline-flex">
          <div className="w-fit   text-sm font-normal font-['Open Sans'] leading-tight"><TimeComponent timestamp={order.created_at} /></div>
        </div>
        <div className="    justify-start items-center inline-flex">
          <div className="  text-sm font-normal font-['Open Sans'] leading-tight"> </div>
        </div>
        <div className="      justify-start items-center inline-flex">
          <div className="  text-sm font-normal font-['Open Sans'] leading-tight"></div>
        </div>
        <div className="  rounded-full justify-center items-center hidden lg:inline-flex">
          <div className="text-sm whitespace-nowrap theme_color theme_colorl text-white p-1 rounded-full flex-col justify-start items-start flex" >More Details</div>
        </div>
        
      </div>
      </div>
      {isPopupDetailsVisible && (
          <>

            <OrderDetailsPage data={popupDetailsData} onClose={() => setIsPopupDetailsVisible(false)} />

          </>

        )}
      
    </>

  );
};

export default OrderProduct;

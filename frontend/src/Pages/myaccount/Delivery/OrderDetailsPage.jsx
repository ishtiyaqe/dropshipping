import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import ProgressBarComponent from './ProgressBarComponent'
import TimeComponent from '../../../components/FrontendTheme/timeClearComponenet'
import OrderDetailsPopup from './OrderDetailsPopup';
import clients from '../../../components/api/Client';
import CloseIcon from '@mui/icons-material/Close';


const OrderDetailsPage = (order) => {
  const [showTimeline, setShowTimeline] = useState(false);
  const [process, setprocess] = useState('');

  const [popupData, setPopupData] = useState(null); // State to manage popup data
  const [isPopupVisible, setIsPopupVisible] = useState(false); // State to manage popup visibility


  const openPopup = (id) => {
    clients.get(`/api/reqpaynow/${id}/`)
      .then((response) => {
        setPopupData(response.data);
        setIsPopupVisible(true);
      })
      .catch((error) => {
        // Handle errors if needed
        console.error(error);
      });
  };
  // Function to toggle the timeline visibility
  const toggleTimeline = () => {
    setShowTimeline(!showTimeline);
    setprocess(order)
  };
  const onClosesclass = () => {
    order.onClose(true)
  }
  return (
    <>
      {/* <div className="fixed inset-0 z-50 flex items-center justify-center backdrop-blur-sm "> */}
      <div className="border p-4 product-box rounded-md shadow-md  ">
        <div className='flex justify-between'>
          <p className="text-sm font-bold  self-center ">Order Id: {order.data.orderi}
            <span className="text-xs font-normal "> Order date: <TimeComponent timestamp={order.data.created_at} /></span>
          </p>

          <button
            className="self-center font-bold drop-shadow-md text-rose-500 p-1"
            onClick={onClosesclass}
          >

            <CloseIcon />
          </button>
        </div>
        <hr className="p-1" />
       
        <div className="">
          <div className="mb-4 space-y-2 flex flex-col justify-center">

           
            {order.data.status === "Order Received" && (
              <button onClick={() => openPopup(order.data.id)}>
                <div className="paynow p-2 text-center text-yellow-60 shadow-md text-white border-gray-200 rounded-md theme_color theme_colorl  w-full">
                  Pay Now
                </div>
              </button>
            )}
            {order.data.status === "Partial Payment Received" && (
              <div className="p-2 text-center text-yellow-60 rounded-md shadow-md text-white  border border-gray-200 theme_color theme_colorl  w-full">
                <a href={`/singleRequest_Delivery/${order.data.order_id}`}>Request Delivery Now</a>
              </div>
            )}

          </div>
        </div>
        <div className="flex   flex-col">
          <div className="w-full">
            <div className="flex lg:flex-row flex-col leading-5">
             
              <div className="lg:ml-3 ml-0 mb-4">
                  {order.data.orderi}
                  <br />
                  Delivery Details:
              <div className="p-2">

                <p className="mt-1 text-sm text-gray400 "><b >Name: {order.data.Name}</b></p>
                <p className="mt-1 text-sm text-gray400 "><b >Phone: {order.data.Phone}</b></p>
                <p className="mt-1 text-sm text-gray400 "><b >Address: {order.data.Address}</b></p>
              </div>

                {order.data.note === '' ? (
                  <p className="mt-1 text-xs text-gray400 "><b >Note:</b> {order.data.note}</p>
                ) : (
                  <></>
                )}
              </div>
            </div>
          </div>
     



        </div>




        <hr className='mt-2 mb-2' />
        {isPopupVisible && (
          <>

            <OrderDetailsPopup data={popupData} onClose={() => setIsPopupVisible(false)} />

          </>

        )}
        <div className="p-2 flex justify-center">
          <p className="text-sm "><b>&nbsp;&nbsp;Last Updated AT: &nbsp;</b><TimeComponent timestamp={order.data.updated_at} /></p>
        </div>

      </div>
      {/* </div> */}
    </>
  )
}

export default OrderDetailsPage
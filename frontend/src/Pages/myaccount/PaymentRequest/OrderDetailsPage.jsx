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
    clients.get(`/api/PayforMePayNow/${id}/`)
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
          <p className="text-sm font-bold  self-center ">Order Id: {order.data.payment_id}
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
        <div className='p-4'>

          <div className='lg:m-8 m-0 h-12 p-4'>
            <ProgressBarComponent process={order.data.status} />
          </div>
        </div>
        <div className="">
          <div className="mb-4 space-y-2 flex flex-col justify-center">

           
          
           
            {order.data.status === "Payment Confirm" && (
              <button onClick={() => openPopup(order.data.payment_id)}>
                <div className="paynow p-2 text-center text-yellow-60 shadow-md text-white border-gray-200 rounded-md theme_color theme_colorl  w-full">
                  Pay Now
                </div>
              </button>
            )}
            

          </div>
        </div>
        <div className="flex   flex-col">
          <div className="w-full">
            <div className="flex lg:flex-row flex-col leading-5">
              <div>
                <div className="block lg:w-32 w-full lg:h-32 h-auto mb-4 rounded border border-gray-200 overflow-hidden">
                  <img src={order.data.image} alt={order.data.product} />
                </div>
              </div>
              <div className="lg:ml-3 ml-0 mb-4">
                <div className=" text-2xl" >
                  {order.data.product_name}
                </div>
                <p className="mt-1 text-xs text-gray400 "><b >Payment Link: {order.data.product_link}</b></p>
                <p className="mt-1 text-xs text-gray400 "><b >Payment Color/Size: {order.data.color}</b></p>
                <p className="mt-1 text-xs text-gray400 "><b >Payment Tracking: {order.data.tracking}</b></p>

                {order.data.note === '' ? (
                  <p className="mt-1 text-xs text-gray400 "><b >Note:</b> {order.data.note}</p>
                ) : (
                  <></>
                )}
              </div>
            </div>
          </div>
          <table className="table-auto grid grid-cols-2">
            <thead>
              <tr className='flex flex-col'>
                <th className='text-xs border border-gray-950 p-2 text-end rounded-l-lg'>Total Quantity</th>
                <th className='text-xs border border-gray-950 p-2 text-end rounded-l-lg'>Total Due</th>
              </tr>
            </thead>
            <tbody>
              <tr className='flex flex-col'>
                <td className='text-xs border text-center border-gray-950 p-2 rounded-r-lg'><b>{order.data.quantity}</b></td>
                <td className='text-xs border text-center border-gray-950 p-2 rounded-r-lg'><b>{order.data.p_total | "Not Set"}</b></td>
              </tr>

            </tbody>
          </table>



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
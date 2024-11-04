import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import ProgressBarComponent from './ProgressBarComponent'
import TimeComponent from '../../../components/FrontendTheme/timeClearComponenet'
import OrderDetailsPopup from './OrderDetailsPopup';
import clients from '../../../components/api/Client';
import CloseIcon from '@mui/icons-material/Close';
import DeliveryFormPage from './DeliveryFormPage'
import OrderPayComponent from './OrderPayComponent'


const OrderDetailsPage = (order) => {
  const [showTimeline, setShowTimeline] = useState(false);
  const [process, setprocess] = useState('');

  const [popupData, setPopupData] = useState(null); // State to manage popup data
  const [popup2Data, setPopup2Data] = useState(null); // State to manage popup data
  const [popup3Data, setPopup3Data] = useState(null); // State to manage popup data
  const [isPopupVisible, setIsPopupVisible] = useState(false); // State to manage popup visibility
  const [isPopup2Visible, setIsPopup2Visible] = useState(false); // State to manage popup visibility
  const [isPopup3Visible, setIsPopup3Visible] = useState(false); // State to manage popup visibility


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

  const openPopup3 = (id) => {
    clients.get(`/ReqssPayView/${id}`)
      .then((response) => {
        setPopup3Data(response.data);
        setIsPopup3Visible(true);
      })
      .catch((error) => {
        // Handle errors if needed
        console.error(error);
      });
  };

  const openPopup2 = (id) => {

    clients.get(`/api/reqpaynow/${id}/`)
      .then((response) => {
        setPopup2Data(response.data);
        setIsPopup2Visible(true);
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
          <p className="text-sm font-bold  self-center ">Order Id: {order.data.OrderP_id}
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

           
            {order.data.status === "Order Received" && (
              <button onClick={() => openPopup(order.data.order_id)}>
                <div className="paynow p-2 text-center text-yellow-60 shadow-md text-white border-gray-200 rounded-md theme_color theme_colorl  w-full">
                  Pay Now
                </div>
              </button>
            )}
           
            {order.data.status === "Order Confirm" && (
              <button onClick={() => openPopup3(order.data.order_id)}>
                <div className="paynow p-2 text-center text-yellow-60 shadow-md text-white border-gray-200 rounded-md theme_color theme_colorl  w-full">
                  Pay Now
                </div>
              </button>
            )}
            {order.data.status === "Partial Payment Received" && (
              <button onClick={() => openPopup2(order.data.order_id)}>
                <div className="paynow p-2 text-center text-yellow-60 shadow-md text-white border-gray-200 rounded-md theme_color theme_colorl  w-full">
                Request Delivery Now
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
                  <img src={order.data.image} alt={order.data.title} />
                </div>
              </div>
              <div className="lg:ml-3 ml-0 mb-4">
                <Link className=" text-2xl" to={`${order.data.link}`} >
                  {order.data.title}
                </Link>
                <p className="mt-1 text-xs text-gray400 "><b >{order.data.color}</b></p>

                {order.data.note === '' ? (
                  <p className="mt-1 text-xs text-gray400 "><b >Note:</b> {order.data.note}</p>
                ) : (
                  <></>
                )}
              </div>
            </div>
          </div>
          <table class="table-auto grid grid-cols-2">
            <thead>
              <tr className='flex flex-col'>
                <th className='text-xs border border-gray-950 p-2 text-end rounded-l-lg'>Total Quantity</th>
                <th className='text-xs border border-gray-950 p-2 text-end rounded-l-lg'>Total Price</th>
                <th className='text-xs border border-gray-950 p-2 text-end rounded-l-lg'>Total Paid</th>
                <th className='text-xs border border-gray-950 p-2 text-end rounded-l-lg'>Total Due</th>
                <th className='text-xs border border-gray-950 p-2 text-end rounded-l-lg'>Weight /kg</th>
                <th className='text-xs border border-gray-950 p-2 text-end rounded-l-lg'>Total Weight</th>
                <th className='text-xs border border-gray-950 p-2 text-end rounded-l-lg'>Weight Charge</th>
                <th className='text-xs border border-gray-950 p-2 text-end rounded-l-lg'>Internal Shipping</th>
              </tr>
            </thead>
            <tbody>
              <tr className='flex flex-col'>
                <td className='text-xs border text-center border-gray-950 p-2 rounded-r-lg'><b>{order.data.quantity}</b></td>
                <td className='text-xs border text-center border-gray-950 p-2 rounded-r-lg'><b>{order.data.price | "Not Set"}</b></td>
                <td className='text-xs border text-center border-gray-950 p-2 rounded-r-lg'><b>{order.data.paid | "Not Set"}</b></td>
                <td className='text-xs border text-center border-gray-950 p-2 rounded-r-lg'><b>{order.data.due | "Not Set"}</b></td>
                <td className='text-xs border text-center border-gray-950 p-2 rounded-r-lg'> <b>{order.data.weight_charge || "0"}</b></td>
                <td className='text-xs border text-center border-gray-950 p-2 rounded-r-lg'> <b>{order.data.total_weight || "0"}</b></td>
                <td className='text-xs border text-center border-gray-950 p-2 rounded-r-lg'> <b>{order.data.total_weight_charge || "0"}</b></td>
                <td className='text-xs border text-center border-gray-950 p-2 rounded-r-lg'> <b>{order.data.internal_shipping_charge || "0"}</b></td>
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
        {isPopup2Visible && (
          <>

            <DeliveryFormPage data={popup2Data} onClose={() => setIsPopup2Visible(false)} />

          </>

        )}
        {isPopup3Visible && (
          <>

            <OrderPayComponent data={popup3Data} onClose={() => setIsPopup3Visible(false)} />

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
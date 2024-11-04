import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import clients from '../../components/api/client';
import CloseIcon from '@mui/icons-material/Close';

const OrderDetailsPage = (order) => {
  const [showTimeline, setShowTimeline] = useState(false);
  const [process, setprocess] = useState('');

  const [popupData, setPopupData] = useState(null); // State to manage popup data
  const [isPopupVisible, setIsPopupVisible] = useState(false); // State to manage popup visibility
  const [popup2Data, setPopup2Data] = useState(null); // State to manage popup data
  const [isPopup2Visible, setIsPopup2Visible] = useState(false); // State to manage popup visibility


  const onClosesclass = () => {
    order.onClose(true)
  }
  return (
    <>
      {/* <div className="fixed inset-0 z-50 flex items-center justify-center backdrop-blur-sm "> */}
      <div className="border m-4 p-4 product-box rounded-md shadow-md  ">



        <button
          className="flex justify-end ml-auto font-bold drop-shadow-md text-rose-500 p-1"
          onClick={onClosesclass}
        >

          <CloseIcon />
        </button>
        <hr className="p-1" />
        <div className='p-4 '>
          <div dangerouslySetInnerHTML={{ __html: order.data.answer }} />

        </div>
      </div>
      {/* </div> */}
    </>
  )
}

export default OrderDetailsPage
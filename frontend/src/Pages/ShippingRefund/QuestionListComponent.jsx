import React, { useState } from 'react';
import OrderDetailsPage from './AnswerpoupComponent.jsx';
import RemoveIcon from '@mui/icons-material/Remove';

const OrderProduct = ({ order }) => {
  const [popupDetailsData, setPopupDetailsData] = useState(null); // State to manage popup data
  const [isPopupDetailsVisible, setIsPopupDetailsVisible] = useState(false); // State to manage popup visibility

  const openPopupDetails = (order) => {
    setIsPopupDetailsVisible(true);
    setPopupDetailsData(order);
  };

  const onClosePopup = () => {
    setIsPopupDetailsVisible(false);
  };

  return (
    <>
      <div onClick={() => { openPopupDetails(order); }}>
        <div className="w-92 h-auto p-2 border m-4 border-gray-200  rounded-lg shadow flex justify-between gap-4">
          <div className="ml-4 justify-start items-center inline-flex">
            <div className="w-full h-5 text-base font-semibold font-['Open Sans'] leading-normal">#{order.question}</div>
          </div>
          <div className="rounded-full justify-center items-center hidden lg:inline-flex">
            <div className="text-sm whitespace-nowrap theme_color theme_colorl text-white p-1 rounded-full flex-col justify-start items-start flex" ><RemoveIcon /></div>
          </div>
        </div>
      </div>

      {isPopupDetailsVisible && (
        <OrderDetailsPage data={popupDetailsData} onClose={onClosePopup} />
      )}
    </>
  );
};

export default OrderProduct;

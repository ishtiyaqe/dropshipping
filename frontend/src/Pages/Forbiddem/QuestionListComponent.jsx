import React, { useState } from 'react';
import RemoveIcon from '@mui/icons-material/Remove';

const OrderProduct = ({ order }) => {



  return (
    <>
      <div >
        <div className="w-92 h-auto p-2 border m-4 border-gray-200  rounded-lg shadow flex justify-between gap-4">
          <div className="ml-4 justify-start items-center inline-flex">
            <div dangerouslySetInnerHTML={{ __html: order.Item_Name }} />
          </div>
         </div>
      </div>

     
    </>
  );
};

export default OrderProduct;

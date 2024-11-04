import React from 'react';
import Skeleton from '@mui/material/Skeleton';
import './asset/Product.css'
const SizeTableComponent = ({
  loadingSize,
  productData,
  handleSizeChange,
  handleQuantityChange,
  sizeData,
  color,
  TotalPriceMap,
}) => {
  const min = 0;
  const max = 999999; // Set your maximum value

  const handleIncrement = (index) => {
    if (productData[index].quantity < max) {
      const newQuantity = productData[index].quantity + 1;
      handleQuantityChange(index, newQuantity);
      
    }
  };

  const handleDecrement = (index) => {
    if (productData[index].quantity > min) {
      const newQuantity = productData[index].quantity - 1;
      handleQuantityChange(index, newQuantity);
      
    }
  };

  return (
    <div className="scroll overflow-x-auto shadow-md rounded-lg">
      {loadingSize ? (
        <>
        <div className='space-y-2'>

         <Skeleton variant="rectangular" width={400} height={40} />
         <Skeleton variant="rectangular" width={400} height={40} />
         <Skeleton variant="rectangular" width={400} height={40} />
         <Skeleton variant="rectangular" width={400} height={40} />
        </div>
        </>
      ):(

        <div className="table-container border border-gray-400 rounded w-1/1" style={{ height: '250px', overflowY: 'auto' }}>
          <table className="data-table w-full ">
            <tbody className="cart-items">
              <tr className="sticky-header bg-lime-600 text-white font-semibold text-md">
                <th>Size</th>
                <th>Price</th>
                <th>Quantity</th>
              </tr>
              {productData.map((sz, index) => (
                <tr className="cartrow space-y-2 p-2" key={index}>
                  <td className="size text-center text-sm mr-2 ml-2 h-full">{sz.size}</td>
                  <td className="cart-price">
                    <p className="font-semibold sizeprice text-center text-sm mr-2 h-full">{sz.price ? sz.price : 'Stock Out'}</p>
                  </td>
                  <td className="cart-quantity w-52 flex justify-center h-full m-auto">
                    <div className="container spin-input rounded-lg theme_color shadow-md flex justify-center">
                      <div >
                        <button
                          className="btn minus-btn txt_9 font-bold text-xl rounded-lg h-full text-white w-10"
                          onClick={() => handleDecrement(index)}
                          disabled={!sz.price || sz.quantity <= min}
                        >
                          -
                        </button>
                      </div>
                      <div>
                        <input
                          className="cuscss text-white cart-quantity-input w-28 h-10 text-center"
                          value={sz.quantity}
                          min={min}
                          max={max}
                          type="number"
                          onChange={(e) => handleQuantityChange(index, parseInt(e.target.value))}
                          disabled={!sz.price || sz.quantity <= min}
                        />
                      </div>
                      <div >
                        <button
                          className="btn plus-btn txt_9 text-white h-full rounded-lg w-10"
                          onClick={() => handleIncrement(index)}
                          disabled={!sz.price || sz.quantity >= max || sz.price === 'Stock Out'}
                        >
                          +
                        </button>
                      </div>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default SizeTableComponent;

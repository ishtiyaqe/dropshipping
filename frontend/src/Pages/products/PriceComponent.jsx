import React from 'react';

const PriceComponent = ({ priceData }) => {
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  return (
    <div className='flex justify-center flex-col'>
      {priceData.proprice ? (
        <p className="text-xl font-semibold">Pro Price: ৳ {priceData.proprice}</p>
      ) : (
        <p className="text-xl font-semibold">৳ {priceData.price}</p>
      )}

      {priceData.saleprice && (
        <p className="text-xl font-semibold">Sale Price: ৳ {priceData.saleprice}</p>
      )}
      <div className='flex jusitfy-center'>

      <p className="text-sm M1"> {priceData.m1} </p>
       <span className='text-center m-auto'>

       -
       </span>
       
       <p className="text-sm M2"> {priceData.m2} </p>
      </div>

    </div>
  );
};

export default PriceComponent;

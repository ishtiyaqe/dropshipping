import React, { useState, useEffect } from 'react';



const MiniBannerComponent = ({ imageurl }) => {




  return (
    <div className="relative">
      
      <img
        src={imageurl}
        alt="Mini Banner"
        className={`w-full h-44 rounded object-cover`}
      
      />
    </div>
  );
};

export default MiniBannerComponent;

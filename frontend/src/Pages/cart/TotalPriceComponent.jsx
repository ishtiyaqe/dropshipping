import React from 'react';

const TotalPriceComponent = ({ items }) => {
  const totalItems = items.length; // Total number of items
  const totalPrice = items.reduce((acc, item) => acc + item.price, 0); // Total price

  return (
    <p>
       {totalPrice.toFixed(2)}
    </p>
  );
};

export default TotalPriceComponent;

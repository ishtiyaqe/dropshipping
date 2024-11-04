

import React, { useEffect, useState } from 'react';
import Typography from '@mui/material/Typography';
import List from '@mui/material/List';
import Grid from '@mui/material/Grid';
import OrderSummaryItem from '../cart/OrderSummaryItem';
import { useCart } from 'react-use-cart';
import clients from '../../components/api/Client';

export default function Review({ address, payInfo, onSubmitOrder  }) {
  const {
    items,
    cartTotal,
    emptyCart
  } = useCart();
  const file = payInfo.transactionImage;
  const [previewImage, setPreviewImage] = React.useState(null);
  React.useEffect(() => {
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setPreviewImage(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  }, [file]);
 
  return (
    <React.Fragment>
      {cartTotal > 0 ? (
        <div>
           <Typography variant="h6" gutterBottom>
        Order summary
      </Typography>
      <OrderSummaryItem />

      <Grid container spacing={2}>
        <Grid item xs={12} sm={6}>
          <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
            Shipping
          </Typography>
          <hr />
          <Typography gutterBottom>{address.first_name} {address.last_name}</Typography>
          <Typography gutterBottom>{address.phone}</Typography>
          <Typography gutterBottom>{address.address}</Typography>
        </Grid>
        <Grid item container direction="column" xs={12} sm={6}>
          <Grid item xs={6}>
            <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
              Payment details
            </Typography>
            <hr />
            <Typography gutterBottom>{payInfo.paymentMethod}</Typography>
            <Typography gutterBottom>{payInfo.transactionId}</Typography>
            <Grid item xs={12} md={6}>
              {previewImage && (
                <img src={previewImage} alt="Transaction Image" className="w-16 h-16" />
              )}
            </Grid>
          </Grid>
        </Grid>
      </Grid>
        </div>
     
      ) : (
        // Render an empty cart message or any other content
        <div className="text-center flex justify-center flex-col p-6 m-6">
     
         <Typography variant="h5" className='self-center' gutterBottom>
           Your cart is empty.
         </Typography>
         <Typography variant="subtitle1">
           Please add items to your cart before checking out.
         </Typography>
         
       </div>
     )}
    </React.Fragment>
  );
}


import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import Typography from "@mui/material/Typography";
import { useEffect, useState } from "react";
import { useCart } from "react-use-cart";

export default function OrderSummaryItem() {
  const { emptyCart } = useCart();
  const [DueAmount, setDueAmount] = useState(0);
  const [PayableNow, setPayableNow] = useState(0);
  const {
    items,
    totalItems,
    totalUniqueItems,
    isEmpty,
    cartTotal,
    removeItem
  } = useCart();
  
    useEffect(() => {
      // Calculate 20% of cartTotal
      const twentyPercent = 0.2; // 20% expressed as a decimal
      const totalpayblenow = cartTotal * twentyPercent;
      const payblenow = cartTotal -totalpayblenow;

      // Calculate dueamount
      const dueamount = cartTotal - payblenow;

      // Assuming you have state variables to store these values
      setDueAmount(dueamount);
      setPayableNow(payblenow);

     
    }, [])
  


  
  

  return (
    <div>
 {cartTotal > 0 ? (
  <div>
      <ul>
        {items.map((item, index) => (

          <li key={index}>
            <div className='flex space-x-2 shadow-md mb-2'>
              <img src={item.imageLink} alt={item.name}
                className='w-16 h-16 mt-2 object-contain rounded shadow-md  ml-2' />
              <div>
                <span className='mini-line'>
                  {item.name}
                </span>
                <span className='flex justify-between font-semibold self-center'>
                  <span>৳ {item.price.toFixed(2)}</span>

                </span>
                <span className='text-xs'>
                  {item.sizesAndColors.map((i, index) => (
                    <span key={index}>Color: {i.color},Size: {i.size}, Price: {i.price}, Quantity: {i.quantity}, </span>
                  ))}
                </span>
              </div>
            </div>


          </li>
        ))}
      </ul>

       
          <div className="flex flex-col p-4 border rounded-md shadow-md mb-4">
          
            <div className="flex justify-between">
              <span>
                Total Amount:
              </span>
              <span>
              {cartTotal.toFixed(2)}
              </span>
            </div>
            <div className="flex justify-between">
              <span>
                Pay Now:
              </span>
              <span>
                {PayableNow.toFixed(2)}
              </span>
            </div>
            <hr />
            <div className="flex justify-between mt-2">
              <span>
                Due Amount:
              </span>
              <span>
                {DueAmount.toFixed(2)}
              </span>
            </div>
            <span className="text-center text-red-600 text-xs p-4">**প্রথমে আপনাকে প্রতি পণ্যের ৮০% পরিমাণ অগ্রিম প্রদান করতে হবে। যখন পণ্যটি আমাদের অফিসে আসবে, তখন আপনার এড্রেসে ডেলিভারি নেয়ার জন্য বাকি ২০% পেমেন্ট করতে হবে। আপনি চাইলে আমাদের অফিসে এসে ২০% পেমেন্ট করে পন্যটি গ্রহন করতে পারেন।**</span>
          </div>
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
        </div>
  );
}

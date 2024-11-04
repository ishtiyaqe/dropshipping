
import { useState } from 'react';
import { useCart } from 'react-use-cart';
import Snackbar from '@material-ui/core/Snackbar';
import MuiAlert from '@material-ui/lab/Alert';
import DeleteOutlineOutlinedIcon from '@mui/icons-material/DeleteOutlineOutlined';
import { Link } from 'react-router-dom';
import emptyshoppingcart from '../../assets/ezgif.com-video-to-gif.gif'




const CartComponent = ({ closeCart }) => {
  const { emptyCart } = useCart();
  const {
    items,
    totalItems,
    totalUniqueItems,
    isEmpty,
    cartTotal,
    removeItem
  } = useCart();
  // const totalPrice = items.reduce((acc, item) => acc + item.price, 0); // Total price
  const [openSuccessBar, setOpenSuccessBar] = useState(false);
  const [openitemSuccessBar, setOpenitemSuccessBar] = useState(false);
  const [openSnackbar, setOpenSnackbar] = useState(false);

  const handleSnackbarClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setOpenSnackbar(false);
  };
  
  // Log the cart data to the console
  
  
  
  
  
  const clearCart = () => {
    if (cartTotal === 0) {

      setOpenSnackbar(true)
    } else {
      emptyCart();
      setOpenSuccessBar(true)

    }
  };

  const handleSuccessBarClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setOpenSuccessBar(false);
  };
  const setOpenitemSuccessBarClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setOpenitemSuccessBar(false);
  };
  const [cart, setCart] = useState([]);

  const handleRemoveFromCart = (pdid) => {
    removeItem(pdid);
    setOpenitemSuccessBar(true)
  };
  const handleCheckout = () => {
    // Perform your checkout logic here

    // Close the Cart by calling the closeCart function
    closeCart();
  };
  return (
    <>
      <div  className='text-black  '>
        <div className="flex justify-between justify-items-center mb-2">

          <h2 className='text-lg p-2 font-bold self-center whitespace-nowrap'>Cart (৳ {cartTotal.toFixed(2)})</h2>
          <button className='bg-red-600 text-white text-md p-2 h-auto rounded-md font-semibold shadow-md' onClick={clearCart}>Clear Cart</button>
          <Snackbar open={openSuccessBar} autoHideDuration={6000} onClose={handleSuccessBarClose}>
            <MuiAlert elevation={6} variant="filled" onClose={handleSuccessBarClose} severity="success">
              Cart successfully empty
            </MuiAlert>
          </Snackbar>
          <Snackbar open={openSnackbar} autoHideDuration={6000} onClose={handleSnackbarClose}>
            <MuiAlert elevation={6} variant="filled" onClose={handleSnackbarClose} severity="warning">
              Please add somethng to cart .
            </MuiAlert>
          </Snackbar>
        </div>
        <hr />
        {isEmpty ? (
          <img width="640" height="360" src={emptyshoppingcart} />
        
        ):(
          <div className='flex justify-center items-end p-2 absolute bottom-0 left-0 right-0'>
          <Link to="/checkout">
            <button onClick={handleCheckout} className='theme_color theme_colorl rounded-md shadow-md w-full p-4 text-center font-semibold text-xl text-white'>Check Out</button>
          </Link>
        </div>
        )}
        


      

        <ul>
          {items.map((item, index) => (
            
            <li key={index}>
              <div className='flex space-x-2 shadow-md mb-2'>
                <img src={item.imageLink} alt={item.name}
                  className='w-16 h-16 mt-2 object-contain rounded  ml-2' />
                <div>
                  <span className='mini-line'>
                    {item.name}
                  </span>
                  <span className='flex justify-between font-semibold self-center'>
                    <div className='overflow-visible'>
                  <span className='text-xs '>
                    {item.sizesAndColors.map((i, index) => (
                      <span key={index}>Color: {i.color},Size: {i.size}, Price: {i.price}, Quantity: {i.quantity}, </span>
                    ))}
                  </span>

                    <span>৳ {item.price.toFixed(2)}</span>
                    </div>
                    <span>
                      <button className='flex justify-end mr-3 mb-2 ml-auto text-sm rounded-md shadow-md p-1' onClick={() => handleRemoveFromCart(item.id)}> <DeleteOutlineOutlinedIcon /></button>
                    </span>
                  </span>
                </div>
              </div>


            </li>
          ))}
        </ul>

        <Snackbar open={openitemSuccessBar} autoHideDuration={3000} onClose={setOpenitemSuccessBarClose}>
          <MuiAlert elevation={6} variant="filled" onClose={setOpenitemSuccessBarClose} severity="success">
            Item  successfuly removed to cart
          </MuiAlert>
        </Snackbar>
      </div>
    </>
  );
};

export default CartComponent;

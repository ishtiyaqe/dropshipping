import React, { useState, useEffect } from 'react';
import { useCart } from 'react-use-cart';
import Snackbar from '@material-ui/core/Snackbar';
import MuiAlert from '@material-ui/lab/Alert';
import ShoppingCartOutlinedIcon from '@mui/icons-material/ShoppingCartOutlined';

const TotalAmountCard = ({ productData, resetData, sizeData, handleQuantityChange, minOrder }) => {
  const { addItem, removeItem, items } = useCart();
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [openSuccessBar, setOpenSuccessBar] = useState(false);
  const [openWarnBar, setopenWarnBar] = useState(false);
  const [Disabl, setDisabl] = useState(false);
  const [totalQuantity, setTotalQuantity] = useState(0);
  const [totalPrice, setTotalPrice] = useState(0);

  useEffect(() => {
    let totalQty = 0;
    let totalPrc = 0;
if (totalQuantity < minOrder){
  setDisabl(true)
}
    if (typeof sizeData === 'object') {
      for (const color in sizeData) {
        if (sizeData.hasOwnProperty(color)) {
          const colorArray = sizeData[color];
          colorArray.forEach((item) => {
            if (item.price && item.quantity) {
              totalQty += item.quantity;
              totalPrc += parseFloat(item.price) * item.quantity;
            }
          });
        }
      }
    } else if (Array.isArray(sizeData)) {
      sizeData.forEach((item) => {
        if (item.price && item.quantity) {
          totalQty += item.quantity;
          totalPrc += parseFloat(item.price) * item.quantity;
        }
      });
    }

    setTotalQuantity(totalQty);
    productData.quantity = totalQty;
    setTotalPrice(totalPrc);
  }, [sizeData, handleQuantityChange]);

  const handleSnackbarClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setOpenSnackbar(false);
  };

  const handleSuccessBarClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setOpenSuccessBar(false);
  };
  const handleWarnBarClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setopenWarnBar(false);
  };

  const handleAddToCart = (index) => {
    const cartItems = [];
    const colorNames = Object.keys(sizeData);
    if(minOrder > totalQuantity){

      setopenWarnBar(true)
      return
    }

    // Create a unique identifier for the product
    const productId = productData.id;

    // Check if the product already exists in cartItems
    const existingProductIndex = items.findIndex((item) => {
      if (item.product_id === productId) {
        // Return the product's ID when a match is found
        return item.id;
      }
      return false; // Return false if there's no match
    });

    if (existingProductIndex !== -1) {
      const existingProductId = existingProductIndex.toString();
      removeItem(existingProductId);
    }

    // Iterate through color names
    colorNames.forEach((colorName) => {
      const colorData = sizeData[colorName];

      // Iterate through colorData to collect product details
      colorData.forEach((product) => {
        if (product.quantity > 0) {
          // Create a unique identifier for the product
          const productId = productData.id;

          // Check if the product already exists in cartItems
          const existingProductIndex = cartItems.findIndex((item) => item.product_id === productId);

          if (existingProductIndex !== -1) {
            // If the product already exists, update the quantities and sizes/colors
            cartItems[existingProductIndex].quantity == totalQuantity;
            cartItems[existingProductIndex].sizesAndColors.push({
              size: product.size,
              price: product.price,
              quantity: product.quantity,
              color: colorName,
            });
          } else {
            // If the product doesn't exist in cartItems, add it
            const proId = items.length + 1;
            cartItems.push({
              id: proId,
              product_id: productData.id,
              product_no: productData.product_no,
              name: productData.name,
              imageLink: productData.image,
              price: totalPrice,
              sizesAndColors: [
                {
                  size: product.size,
                  price: product.price,
                  quantity: product.quantity,
                  color: colorName,
                },
              ],
            });
          }
        }
      });
    });

    if (cartItems.length === 0) {
      setOpenSnackbar(true); // Show a message indicating an empty cart.
    } else {
      // Add selected products to the cart
      cartItems.forEach((item) => {
        addItem(item, 1); // Assuming addItem is a function that adds items to the cart.
      });

      resetData();
      setTotalPrice(0);
      setTotalQuantity(0);
      setOpenSuccessBar(true);
    }
  };

  return (
    <div className=" p-4 rounded-md shadow-md border  dark:border-gray-400 dark:shadow-gray-200 w-full">
      <div className="flex mb-4 justify-between">
        <div className="mr-auto p-2 bd-highlight" style={{ width: '100%' }}>
          <div className="flex justify-between ProductAddCart_totalPrice__TTuql d-flex justify-content-between">
            <span className="cart-total-quantity">Quantity: {totalQuantity}</span>
            <span className="cart-total-price">৳ {totalPrice}</span>
          </div>
          <div className="flex justify-between ProductAddCart_totalValue__1Jf2w d-flex justify-content-between mt-1">
            <span style={{ fontSize: '12px' }}>Domestic Shipping Charge</span>
            <span>0</span>
          </div>
        </div>
      </div>

      <hr />

      <div className="flex total_amount d-flex sm:justify-between justify-between mb-6 mt-2">
        <span>Total</span>
        <span className="total">৳ {totalPrice} <span style={{ color: 'red' }}>*</span></span>
      </div>

      <button 
      
       className={`theme_color theme_colorl text-2xl text-center rounded-lg p-2 text-white font-bold self-center w-full mb-4 `}
        onClick={handleAddToCart}
        >
          <ShoppingCartOutlinedIcon /> 
          Add to Cart
          </button>

      {/* Snackbar for displaying the notification */}
      <Snackbar open={openSnackbar} autoHideDuration={6000} onClose={handleSnackbarClose}>
        <MuiAlert elevation={6} variant="filled" onClose={handleSnackbarClose} severity="warning">
          Please choose color and quantity before adding to the cart.
        </MuiAlert>
      </Snackbar>
      <Snackbar open={openSuccessBar} autoHideDuration={6000} onClose={handleSuccessBarClose}>
        <MuiAlert elevation={6} variant="filled" onClose={handleSuccessBarClose} severity="success">
          Product successfully added to cart
        </MuiAlert>
      </Snackbar>
      <Snackbar open={openWarnBar} autoHideDuration={3000} onClose={handleWarnBarClose}>
        <MuiAlert elevation={6} variant="filled" onClose={handleWarnBarClose} severity="warning">
          Reach Minimum Quantity To "Add to cart"
        </MuiAlert>
      </Snackbar>
      <div className="text-right">
        <span style={{ fontSize: '10px', color: 'red' }}>*Shipping Charge will be included later</span>
      </div>
      <div className="text-right">
        <span style={{ fontSize: '10px', color: 'red' }}>
          *আপনাকে যে কোন সেলার থেকে সর্বনিম্ন ২,০০০ টাকার শপিং করতে হবে
          অন্যথায় সেলার অর্ড
        </span>
      </div>
    </div>
  );
};

export default TotalAmountCard;

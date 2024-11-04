import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Skeleton from '@mui/material/Skeleton';
import ProductThumbnailCarousel from './ThumnilCoursoleComponent';
import ColorComponent from './ColorComponent';
import SkuComponent from './SkuComponent';
import SizeTableComponent from './SizeTableComponent';
import TotalAmountCard from './TotalAmountCard';
import clients from '../../components/api/Client';
import PriceComponent from './PriceComponent'
import SellerInfoComponent from './SellerInfoComponent';
import LoadingBar from 'react-top-loading-bar'
import DescriptionComponent from './DescriptionComponent';
import ReviewComponent from './ReviewComponent';
import ProductGrid from '../../components/FrontendTheme/ProductGridComponent'
import FutureProductComponent from './FutureProductComponent';

function ProductDetails() {
  const [progress, setProgress] = useState(0)
  const { id } = useParams();
  const [product, setProduct] = useState([]);
  const [activeColor, setActiveColor] = useState('');
  const [selectedImage, setSelectedImage] = useState('');
  const [productImages, setProductImages] = useState([]);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [currentPriceIndex, setCurrentPriceIndex] = useState(0);
  const [loadingImage, setLoadingImage] = useState(true);
  const [loadingSize, setLoadingSize] = useState(true);
  const [ProductLoding, setProductLoding] = useState(true);
  const [sizeData, setSizeData] = useState([]);
  const [sizeCurrentData, setSizeCurrentData] = useState([]);
  const [productData, setProductData] = useState([]);
  const [totalQuantity, setTotalQuantity] = useState('');
  const [TotalPriceMap, setTotalPriceMap] = useState('');
  const [minOrder, setminOrder] = useState(0)
  const [showDescription, setShowDescription] = useState(true);
  const [showReviews, setShowReviews] = useState(false);

  const toggleDescription = () => {
    setShowDescription(true);
    setShowReviews(false);
  };

  const toggleReviews = () => {
    setShowDescription(false);
    setShowReviews(true);
  };

  const handleQuantityChange = (index, newQuantity) => {
    const updatedProductData = [...sizeCurrentData];
    updatedProductData[index].quantity = newQuantity;
    setSizeCurrentData(updatedProductData);
    setCurrentPriceIndex(updatedProductData[index].price);
  };
  useEffect(() => {
    let totalQty = 0;
    let totalPrc = 0;

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

  }, [sizeData, handleQuantityChange]);

  const resetData = () => {
    const updatedSizeData = { ...sizeData };
    const updatedCurrentSizeData = sizeCurrentData.map((item) => ({ ...item, quantity: 0 }));

    for (const key in updatedSizeData) {
      if (updatedSizeData.hasOwnProperty(key)) {
        updatedSizeData[key] = updatedSizeData[key].map((item) => ({ ...item, quantity: 0 }));
      }
    }

    setSizeData([]);
    setSizeCurrentData([]);
    fetchProductData(id);
    fetchSizeData(activeColor);

    const delay = 2000;
    const timeoutId = setTimeout(() => {
      window.location.reload();
    }, delay);

    return () => clearTimeout(timeoutId);
  };

  const fetchProductData = async () => {
    setProgress(10);
    try {
      const response = await clients.get(`/get_single_product/${id}`);
      const data = response.data;
      let productData = {
        id: data.id,
        product_no: data.product_no,
        name: data.name,
        image: data.image,
        prices: [],
      };
      if (Array.isArray(data.prices)) {
        productData.prices = data.prices.map((price) => ({
          price: typeof price === 'number' ? price.toFixed(2) : price,
        }));
      } else {
        productData.prices.push({
          price: typeof data.price === 'number' ? data.price.toFixed(2) : data.price,
        });
      }
      setProduct(productData);
      setProductLoding(false)
    } catch (error) {
      console.error('Error fetching product data:', error);
    }
  };

  const handleSizeChange = (index, newSize) => {
    const updatedProductData = [...sizeCurrentData];
    updatedProductData[index].size = newSize;
    setSizeCurrentData(updatedProductData);


  };



  useEffect(() => {
    fetchProductData();
  }, [id]);
  useEffect(() => {
    pricess();
  }, [totalQuantity]);

  const pricess = () => {
    if (product.prices && Array.isArray(product.prices)) {
      const quantityMap = {};
      const totalPriceMap = {};
      let calculatedPrice = 0;

      // Iterate through each price range and calculate total quantity and total price
      product.prices.forEach(({ price }) => {
        const { m1, price: priceValue } = price;

        // Check if the total quantity falls within the specified range
        if (totalQuantity >= parseInt(m1)) {
          calculatedPrice = parseFloat(priceValue);
          console.log(calculatedPrice);

          // Update sizeData using the state-setting function
          setSizeData((prevSizeData) => {
            const updatedSizeData = { ...prevSizeData };
            for (const color in updatedSizeData) {
              if (updatedSizeData.hasOwnProperty(color)) {
                const colorArray = updatedSizeData[color];
                colorArray.forEach((item) => {
                  item.price = calculatedPrice;
                });
              }
            }
            return updatedSizeData;
          });

          // Break out of the loop once the correct price range is found
          return;
        }
      });
    }
  };



  useEffect(() => {
    setProgress(80);
    const fetchData = async () => {
      try {
        if (product.id) {
        const response = await clients.get(`/get_single_product_images/${product.product_no}/`);
        const fetchedImages = response.data.images;
        setProductImages(fetchedImages);
        setLoadingImage(false);

        setSelectedImage(fetchedImages[0]);

        if (!activeColor) {
          try {
            const response = await clients.get(`/get_sizes/${product.product_no}/`);
            if (response.data.sizes) {
              setSizeData((prevSizeData) => ({
                ...prevSizeData,
                [0]: response.data.sizes,
              }));
              setSizeCurrentData(response.data.sizes);
              setLoadingSize(false)
            }
          } catch (error) {
            console.error("Error fetching data:", error);
          }
        }
      }
      } catch (error) {
        console.error('Error fetching product images:', error);
      }
    };

    fetchData();
    setProgress(100);
  }, [product]);

  const handleThumbnailClick = (index) => {
    // setCurrentImageIndex(index);
    setSelectedImage(productImages[index]);
  };

  if (!product) {
    return (
      <div className="product-details container p-2 flex justify-center flex-col m-auto">
        {/* Your skeleton loading UI */}
        <Skeleton variant="rectangular" width={380} height={350} />
      </div>
    );
  }

  const fetchSizeData = async (color) => {
    try {
      if (color.length === 0) {
        console.warn('Empty color array provided.');
        // You can set default values or handle it according to your use case
        setActiveColor()
        return;
      } else {
        if (!sizeData[color]) {
          const response = await clients.get(`/get_sizes_for_color/${product.product_no}/${color}/`);
          if (response.data.sizes) {
            setSizeData((prevSizeData) => ({
              ...prevSizeData,
              [color]: response.data.sizes,
            }));
            setSizeCurrentData(response.data.sizes);
            setLoadingSize(false);
          }
        } else {
          // Check if sizeData[color] is defined before mapping
          if (sizeData[color]) {
            setSizeCurrentData(sizeData[color]);
          } else {
            console.warn('sizeData[color] is undefined.');
            // You can set default values or handle it according to your use case
          }
        }
        
      }
    } catch (error) {
      console.error('Error fetching size data:', error);
    }
  };
  
  useEffect(() => {
    if (activeColor) {
      fetchSizeData(activeColor);
    }

  }, [activeColor]);
  const handleColorChange = (color) => {
    setActiveColor(color);
    fetchSizeData(color);
  };
console.log(activeColor)
console.log(activeColor)
console.log(activeColor)
console.log(activeColor)
console.log(activeColor)
 

  const [isVideoPlaying, setIsVideoPlaying] = useState(false);

  
  const isPriceArray = Array.isArray(product.prices) && product.prices.length > 0;
  return (
    <>
      <LoadingBar
        color='#f11946'
        progress={progress}
        onLoaderFinished={() => setProgress(0)}
      />
      <div className="product-details container  flex justify-center flex-col m-auto mt-8 p-4">
        {/* Top panel start */}
        <div className="grid lg:grid-cols-3 grid-cols-1 gap-2 justify-items-center">
          <div className="space-y-2 overflow-clip ">
            {loadingImage ? (
              <div className="space-y-2">
                <Skeleton variant="rectangular" width={380} height={350} />
              </div>
            ) : (
              <div className="space-y-2">
                <img
                className="h-96 w-96 object-fill"
                src={selectedImage.img || selectedImage}
                alt={product.name}
              />


                <div className="w-96 ">
                  <ProductThumbnailCarousel
                    images={productImages}
                    onClickThumbnail={handleThumbnailClick}
                  />
                </div>
              </div>
            )}
          </div>
          {ProductLoding ? (
            <div className="p-4 space-y-4">
               <Skeleton variant="rectangular" width={380} height={20} />
               <Skeleton variant="rectangular" width={380} height={100} />
            </div>
          ):(

            <div className=" ">
              <h2 className="text-x mb-4 ">{product.name}</h2>
              <span style={{ fontWeight: '10px' }} className="mt-2 mb-2 ">
                {product.prices && product.prices.length > 1 ? (
                  <span style={{ fontWeight: '10px' }} className="mt-2 mb-2 p-2 flex space-x-4 justify-evenly bg-white  shadow-md dark:shadow-gray-200 text-black rounded-md">
                    {product.prices.map((price, index) => (
                      <PriceComponent key={index} priceData={price.price} />
                      ))}
                  </span>
                ) : (
                  <>
                  {isPriceArray && typeof product.prices[0].price === 'object' ? (
                    <PriceComponent  priceData={product.prices[0].price} />
                    ) : (
                      <p  className="text-4xl">৳ {product.prices[0].price} </p>
                  )}
                  
                  </>
                  
                )}
              </span>
  
              <div className="w-full mb-4 mt-4 ">
                <SkuComponent
                  productNo={product.product_no}
                  onColorChange={handleColorChange}
                  activeColor={activeColor}
                  setActiveColor={setActiveColor}
                  selectedImage={selectedImage}
                  onImageChange={setSelectedImage}
                />
              </div>
              <div className="w-full mb-4 ">
  
                <ColorComponent
                  productNo={product.product_no}
                  onColorChange={handleColorChange}
                  activeColor={activeColor}
                  setActiveColor={setActiveColor}
                  selectedImage={selectedImage}
                  onImageChange={setSelectedImage}
                />
              </div>
              <div className="">
                <SizeTableComponent
                  loadingSize={loadingSize}
                  productData={sizeCurrentData}
                  sizeData={sizeData}
                  color={activeColor}
                  handleSizeChange={handleSizeChange}
                  handleQuantityChange={handleQuantityChange}
                />
              </div>
            </div>
          )}
          <div className='lg:w-full w-screen p-4'>
            <TotalAmountCard
              minOrder={minOrder}
              totalPriceMap={TotalPriceMap}
              productData={product}
              resetData={resetData}
              handleQuantityChange={handleQuantityChange}
              sizeData={sizeData}
            />
            <SellerInfoComponent
              className="mt-4 w-92"
              productNo={product.product_no}
            />
          </div>


        </div>
        <div>
          <div className='px-4  border-b w-full mt-4'>
            <div className='flex space-x-4 text-center'>
              <span
                className={`border-t-2 cursor-pointer border-r-2 border-l-2 w-full lg:w-32  rounded-t-md p-4 ${showDescription ? 'bg-gray-300 text-black' : ''
                  }`}
                onClick={toggleDescription}
              >
                Description
              </span>
              <span
                className={`border-t-2 cursor-pointer border-r-2 border-l-2 w-full lg:w-32 rounded-t-md p-4 ${showReviews ? 'bg-gray-300 text-black' : ''
                  }`}
                onClick={toggleReviews}
              >
                Reviews
              </span>
            </div>
          </div>
          <div className='p-2'>
          {product.product_no ? (
            <div>
              {showDescription && <DescriptionComponent productNo={product.product_no} />}
              {showReviews && <ReviewComponent productNo={product.product_no} />}
            </div>
          ) : (
            // You can replace this with an appropriate fallback or leave it empty
            <div></div>
          )}

          </div>
        </div>
        <div className='p-2'>
          <FutureProductComponent
            productNo={product.product_no}
          />
        </div>
      </div>
    </>
  );
}

export default ProductDetails;

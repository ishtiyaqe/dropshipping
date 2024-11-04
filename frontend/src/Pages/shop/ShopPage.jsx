import React, { useEffect, useState } from 'react';
import Slider from '@material-ui/core/Slider';
import Typography from '@material-ui/core/Typography';
import Skeleton from '@material-ui/lab/Skeleton';
import clients from '../../components/api/Client';
import FilterAltTwoToneIcon from '@mui/icons-material/FilterAltTwoTone';
import ProductCardComponent from '../../components/FrontendTheme/ProductCardComponent';
import LoadingBar from 'react-top-loading-bar'

const StorePage = () => {
  const [progress, setProgress] = useState(0)
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [priceRange, setPriceRange] = useState([0, 1000000000000]);
  const [sliderVisible, setSliderVisible] = useState(false);
  const [total, setTotal] = useState(0);

  const loadMoreData = async () => {
    try {
      const currentProducts = products.length;
      const limit = 10; // You can adjust the limit as needed
      const response = await clients.get('/load-more-data', {
        params: {
          limit: limit,
          offset: currentProducts,
        },
      });

      const newProducts = response.data.product;
      setProducts((prevProducts) => [...prevProducts, ...newProducts]);
      // setTotal(response.data.total);
    } catch (error) {
      console.error('Error loading more data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (loading) {
      loadMoreData();
    }
  }, [loading]);

  const handleClick = () => {
    setLoading(true);
  };
  useEffect(() => {
    setProgress(10);
    setLoading(true);

    clients
      .get('/get_all_products/?num=10')
      .then((response) => {
        setProgress(50);
        const productData = response.data.products.map((item) => ({
          id: item.id,
          product_no: item.product_no,
          link: item.link,
          name: item.name,
          image: item.image,
          price: parseFloat(item.price),
        }));
        setProducts(productData);
        setTotal(response.data.total_count)
        setLoading(false);
        setProgress(100);
      })
      .catch((error) => {
        setProgress(50);
        console.error('Error fetching product data:', error);
        setLoading(false);
        setProgress(100);
      });
  }, []);

  const getMaxMinPrices = (products) => {
    if (products.length === 0) {
      return { maxPrice: 0, minPrice: 0 };
    }

    let maxPrice = products[0].price;
    let minPrice = products[0].price;

    for (const product of products) {
      if (product.price > maxPrice) {
        maxPrice = product.price;
      }
      if (product.price < minPrice) {
        minPrice = product.price;
      }
    }

    return { maxPrice, minPrice };
  };

  const { maxPrice, minPrice } = getMaxMinPrices(products);

  const filterProductsByPrice = (minPrice, maxPrice) => {
    const filteredProducts = products.filter((product) => product.price >= minPrice && product.price <= maxPrice);
    return filteredProducts;
  };

  const filteredProducts = filterProductsByPrice(priceRange[0], priceRange[1]);

  return (
    <>
      <LoadingBar
        color='#f11946'
        progress={progress}
        onLoaderFinished={() => setProgress(0)}
      />
      <div className='lg:m-10 m-5 grid  grid-cols-1 gap-2'>
        <div className='w-full'>
          <Typography 
            id="price-range-slider" 
            className='flex justify-end p-1 rounded-full theme_color theme_colol w-20  text-white' 
            onClick={() => setSliderVisible(!sliderVisible)}
            gutterBottom
          >
            
            <span className='self-center'>Filter</span>
            <span><FilterAltTwoToneIcon className='flex justify-end ' /></span>
          </Typography>
          <div 
            className={`bg-white mb-4 p-4 rounded-md shadow-md dark:shadow-gray-200 transition-all duration-700 ${
              sliderVisible ? '' : 'hidden'
            }`}
          >
            Price Range 
            <Slider
              value={priceRange}
              onChange={(_event, newValue) => setPriceRange(newValue)}
              valueLabelDisplay="auto"
              className='text-black'
              aria-labelledby="price-range-slider"
              min={minPrice}
              max={maxPrice}
            />
          </div>
        </div>
        <div className='col-span-2'>
          <div className='grid lg:grid-cols-5 grid-cols-2  gap-4'>
            {loading
              ? Array.from({ length: 10 }).map((_, index) => (
                  <div key={index} className="w-full rounded-md border shadow-md dark:shadow-gray-400">
                    <Skeleton variant="rect" width="100%" height={200} animation="wave" />
                    <Skeleton variant="text" width="100%" height={20} animation="wave" />
                    <Skeleton variant="text" width="100%" height={20} animation="wave" />
                  </div>
                ))
              :filteredProducts.map((product) => (
                <div key={product.id}>
                <ProductCardComponent product={product} />
              </div>
              ))
            }
            
            
          </div>
        </div>
      </div>
      {products.length < total && (
  <button id="loadMore" onClick={handleClick} className='p-2 text-white rounded-md shadow-md flex justify-center m-auto mb-10 theme_color theme_colorl' disabled={loading}>
    {loading ? 'Loading...' : 'Load More'}
  </button>
)}
    </>
  );
};

export default StorePage;

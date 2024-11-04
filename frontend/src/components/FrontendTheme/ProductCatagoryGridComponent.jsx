import React, { useEffect, useState } from 'react';
import { Splide, SplideSlide } from '@splidejs/react-splide';
import '@splidejs/splide/dist/css/themes/splide-default.min.css';
import ProductCardComponent from './ProductCardComponent';
import './static/css/ProductGrid.css'; // You can create this for custom styling
import clients from '../api/Client';
import Skeleton from '@mui/material/Skeleton';

function ProductGrid({props}) {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Set loading state to true when starting to fetch data
    setLoading(true);

    const productData = props.map((item) => ({
      id: item.id,
      product_no: item.product_no,
      link: item.link,
      name: item.name,
      image: item.image,
      price: item.prices,
    }));
    setProducts(productData);
    setLoading(false); // Set loading state to false after data is fetched
   
  }, [setProducts]);

  const splideOptions = {
    type: 'loop',
    gap: 15,
    autoplay: true,
    interval: 4000,
    // Other options...
  };

  const ProductSlider = () => {
    const screenWidth = window.innerWidth;

    let perPage = 4;
    if (screenWidth <= 1100) {
      perPage = 4;
    }
    if (screenWidth <= 600) {
      perPage = 3;
    }
    if (screenWidth <= 400) {
      perPage = 2;
    }

    if (loading) {
      // Display a loading state or skeleton screen while data is being fetched
      return (
        <Splide options={{ ...splideOptions, perPage }} style={{ padding: '2px' }}>
          {Array.from({ length: perPage }).map((_, index) => (
            <SplideSlide key={index}>
              <div className='flex flex-col space-y-2 bg-gray-100 rounded-md shadow-md dark:shadow-gray-200'>
                <Skeleton variant="rectangular" width={200} height={200} />
                <Skeleton variant="rectangular" width={150} height={10} />
              </div>
            </SplideSlide>
          ))}
        </Splide>
      );
    }

    return (
      <div className="product-grid ml-2">
        <Splide options={{ ...splideOptions, perPage }} style={{ padding: '1px' }}>
          {products.map((product) => (
            <SplideSlide key={product.id}>
              <ProductCardComponent product={product} />
            </SplideSlide>
          ))}
        </Splide>
      </div>
    );
  };

  return <ProductSlider />;
}

export default ProductGrid;

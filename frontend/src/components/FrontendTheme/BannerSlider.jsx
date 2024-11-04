import React, { useEffect, useState } from 'react';
import { Splide, SplideSlide } from '@splidejs/react-splide';
import axios from 'axios';
import '@splidejs/react-splide/css';
import Skeleton from '@mui/material/Skeleton';
import clients from '../api/client';

const BannerSlider = () => {
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate a 5-second delay before fetching images
    setTimeout(() => {
      // Set loading to true when starting the API call
      setLoading(true);

      // Fetch images from the API
      clients.get('/home-banner')
        .then((response) => {
          const imageUrls = response.data.Home_banner.map((item) => item.image);
          setImages(imageUrls);
          setLoading(false); // Set loading to false when images are fetched
        })
        .catch((error) => {
          console.error('Error fetching images:', error);
          setLoading(false); // Ensure loading is set to false on error as well
        });
    }); // 5-second delay
  }, []);

  return (
    <div className='flex justify-center mt-2 rounded-md'>
      {loading ? ( // Show Skeleton while loading
        <Skeleton style={{ borderRadius: 5 }} variant="rectangular" width='100%' height={420} />
      ) : (
        <Splide
          options={{
            type: 'loop', // Enables looping
            perPage: 1, // Number of slides to show at a time
            autoplay: true, // Enable autoplay
            interval: 3000, // Delay in milliseconds between slides
          }}
        >
          {images.map((imageUrl, index) => ( // Wrap map function with curly braces
            <SplideSlide key={index}>
              <img style={{ borderRadius: 5 }} className='w-full h-96' src={imageUrl} alt={`Image ${index + 1}`} />
            </SplideSlide>
          ))}
        </Splide>
      )}
    </div>
  );
};

export default BannerSlider;

import  { useState } from 'react';
import { Splide, SplideSlide } from '@splidejs/react-splide';
import '@splidejs/splide/dist/css/themes/splide-default.min.css';
import Skeleton from '@mui/material/Skeleton';

const ProductThumbnailCarousel = ({ images, onClickThumbnail }) => {
  const [loading, setLoading] = useState(true);

  // Simulate a loading delay, you can remove this in production
  setTimeout(() => {
    setLoading(false);
  }, 2000);

  return (
    <div className="product-thumbnail-carousel">
      {loading ? (
        // Show a skeleton while loading
        <Splide options={{
          type: 'loop',
          perPage: 5,
          focus: 'center',
          autoplay: true,
          interval: 3000,
          gap: 4,
        }}>
          {[1, 2, 3, 4, 5].map((index) => (
            <SplideSlide key={index}>
              <div className="thumbnail">
                <Skeleton variant="rectangular" width={150} height={50} />
              </div>
            </SplideSlide>
          ))}
        </Splide>
      ) : (
        // Show the actual images when not loading
        <Splide options={{
          type: 'loop',
          perPage: 5,
          focus: 'center',
          autoplay: true,
          interval: 3000,
          gap: 2,
        }}>
          {images.map((image, index) => (
            <SplideSlide key={index}>
              <div className="thumbnail" onClick={() => onClickThumbnail(index)}>
                {image.img.startsWith('https://video01') ? (
                  <img className='w-auto h-16' src={image.cover} alt={`Thumbnail ${index}`} />
                ) : (
                  <img className='w-auto h-16' src={image.img} alt={`Thumbnail ${index}`} />
                )}
              </div>
            </SplideSlide>
          ))}
        </Splide>
        
      )}
    </div>
  );
};

export default ProductThumbnailCarousel;

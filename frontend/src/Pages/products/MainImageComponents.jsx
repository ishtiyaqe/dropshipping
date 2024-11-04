import  { useEffect, useState } from 'react';
import ProductThumbnailCarousel from './ThumnilCoursoleComponent';
import Skeleton from '@mui/material/Skeleton';
import clients from '../../components/api/Client';

const MainImageComponent = ({ product_no }) => {
  const [productImages, setProductImages] = useState([]);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [loadingImage, setLoadingImage] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        
        const response = await clients.get(`/get_single_product_images/${product_no}?color=${activeColor}`); // Include the activeColor in the request URL

        const fetchedImages = response.data.images;
        setProductImages(fetchedImages);
        setLoadingImage(false);
      } catch (error) {
        console.error('Error fetching product images:', error);
      }
    };

    fetchData();
  }, [product_no, activeColor]); // Listen for changes in activeColor

  // Use this effect to update activeColor whenever currentImageIndex changes
  useEffect(() => {
    const currentImage = productImages[currentImageIndex];
    if (currentImage) {
      // Check if the activeColor is not an empty string
      if (activeColor) {
        setActiveColor(currentImage.color);
      }
    }
  }, [currentImageIndex, productImages, activeColor]);

  // Store the selected image in a variable
  const selectedImage = activeColor
    ? productImages.find(image => image.color === activeColor)
    : productImages[currentImageIndex];

  const handleThumbnailClick = (index) => {
    setCurrentImageIndex(index);
  };

  return (
    <div>
      {loadingImage ? (
        <div className="space-y-2">
          <Skeleton variant="rectangular" width={400} height={400} />
          <Skeleton variant="rectangular" width={150} height={150} />
        </div>
      ) : (
        <>
          <div className='space-y-2'>
            <img
              className="h-80 w-full"
              src={selectedImage}
              alt=""
              onLoad={() => setLoadingImage(false)}
            />
            <ProductThumbnailCarousel
              images={productImages}
              onClickThumbnail={handleThumbnailClick}
            />
          </div>
        </>
      )}
    </div>
  );
};

export default MainImageComponent;

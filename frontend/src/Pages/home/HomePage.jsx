import { useEffect, useState } from 'react'
import BannerSlider from '../../components/FrontendTheme/BannerSlider'
import ProductGrid from '../../components/FrontendTheme/LatestproductGridComponent'
import MiniBannerComponent from './MiniBannerComponent'
import Skeleton from '@mui/material/Skeleton';
import TextBannerComponent from './TextBannerComponent';
import CatagoryComponent from './CatagoryComponent';
import ScrollingTexBanner from './ScrollingTexBanner';
import MiddelBannerComponent from './MiddelBannerComponent';
import CatagoryProductCardComponent from './CatagoryProductCardComponent';
import TwoImageBannerComponent from './TwoImageBannerComponent';
import FutureBrandsComponent from './FutureBrandsComponent';
import LoadingBar from 'react-top-loading-bar'
import clients from '../../components/api/client';
const Home = () => {
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(0)
  const [categories, setCategories] = useState([]);



  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await clients.get('/subcategories/');
        const data = await response.data;
        setCategories(data);
      } catch (error) {
        console.error('Error fetching subcategories:', error);
      }
    };

    fetchData();
  },[setCategories])


  useEffect(() => {
    setProgress(10);
    const fetchData = async () => {
      try {
        // Fetch images from the API
        const response = await clients.get('/Home_top600px_Banneer');
        setProgress(30);

        const imageUrls = response.data.Home_banner.map((item) => item.image);
       
        setProgress(80);
        setImages(imageUrls);
        setLoading(false);
        setProgress(100);
      } catch (error) {
        console.error('Error fetching images:', error);
      }
    };

    // Simulate a 5-second delay before fetching images
    setTimeout(fetchData); // 5-second delay
  }, [setProgress]);
  return (
    <>
      <LoadingBar
        color='#f11946'
        progress={progress}
        onLoaderFinished={() => setProgress(0)}
      />
      <div className='container p-2 flex justify-center flex-col m-auto'>
        <div className='grid lg:grid-cols-3 grid-cols-1 gap-3'>

          <div className='mb-2 col-span-2 '>
            <BannerSlider />
          </div>
          <div className='lg:ml-0 ml-2 mb-2 grid lg:grid-cols-1 grid-cols-2 gap-4 lg:mt-4 mt-0'>
            {loading && (
              <div className='lg:ml-0 ml-2 mb-2 grid lg:grid-cols-1 grid-cols-2 gap-4 lg:mt-4 mt-0'>
                <Skeleton style={{ borderRadius: 5 }} variant="rectangular" width='100%' height={180} />
                <Skeleton style={{ borderRadius: 5 }} variant="rectangular" width='100%' height={180} />
              </div>
            )}
            {images.map((imageUrl, index) => ( // Wrap map function with curly braces
              <div key={index}>
                <MiniBannerComponent
                  imageurl={imageUrl}
                  onLoad={() => setLoading(false)}
                />
              </div>

            ))}
            <div>
            </div>
          </div>
        </div>
        <div className='mb-4'>
          <TextBannerComponent />
        </div>
        <div className='mb-4'>
          <CatagoryComponent />
        </div>
        <div className='mb-4'>
          <ScrollingTexBanner />
        </div>
        <div>
          <span className='m-2 text-xl font-black '>Latest Products</span>
          <ProductGrid />
        </div>
        <div className='mr-5'>
          <MiddelBannerComponent />
        </div>
        <div className='mt-10 mb-6'>
          <CatagoryProductCardComponent props={categories[0]} />
        </div>
        <div className='mb-6'>
          <TwoImageBannerComponent />
        </div>
        <div className='mb-6'>
          <CatagoryProductCardComponent props={categories[1]} />
        </div>
        <div className='mb-6'>
          <FutureBrandsComponent />
        </div>
      </div>
    </>
  )
}

export default Home
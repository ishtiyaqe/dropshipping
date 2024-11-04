import { useEffect, useState } from 'react'
import './asset/MiddleBanner.css'
import clients from '../../components/api/client';
import Skeleton from '@mui/material/Skeleton';
import ScrollingText from './ScrollingText';

const ScrollingTexBanner = () => {
  const [datSet, setDatSet] = useState([]);
  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch images from the API
        const response = await clients.get('/Home_sliding_selling_text_Banneer');
       

        const datas = response.data.Home_banner;

        setDatSet(datas);
   
      } catch (error) {
        console.error('Error fetching images:', error);
      }
    };

    // Simulate a 5-second delay before fetching images
    setTimeout(fetchData); // 5-second delay
  }, [setDatSet]);
  return (
    <div className="sc-19ecb654-0 sc-f2642c76-0 sc-93872882-2 jsmmJw iaYNFu kZovfW">
      <h3 style={{ fontSize: '20px' }} className="sc-db80def1-0 hbMKme sc-93872882-3 cuCafS">{datSet.name}</h3>
      <p style={{ fontSize: '28px', zIndex: 5 }} className="sc-db80def1-0 kIEKkg">
        <span style={{ fontSize: '20px' }} className="sc-db80def1-0 gRzjr sc-93872882-5 eRjLEq text-3xl">
        {datSet.Scorlling_Text}
          {/* <span style={{ fontSize: 'inherit', fontWeight: 700 }} className="sc-db80def1-0 eChkix text-3xl"> your loving electronics</span> */}
        </span>
      </p>
      <div style={{ padding: '1.5rem', flexShrink: 0, zIndex: 5 }} className="sc-19ecb654-0 kihmmo">
        <a href={datSet.url} style={{ color: 'primary' }} className="sc-44536d9-0 ljlHTz sc-93872882-4 hYdLe theme_color theme_colorl">Shop Now</a>
      </div>
    </div>
  );
};

export default ScrollingTexBanner;

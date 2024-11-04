import { useEffect, useState } from 'react';
import './asset/MiddleBanner.css';
import clients from '../../components/api/client';
import Skeleton from '@mui/material/Skeleton';

const TwoImageBannerComponent = () => {
  const [datSet, setDatSet] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch data from the API
        const response = await clients.get('/Home_middel680x180px_Banneer');
        const datas = response.data.Home_banner.map((item) => item);

        setDatSet(datas);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    // Simulate a 5-second delay before fetching data
    setTimeout(fetchData); // 5-second delay
  }, [setDatSet]);

  return (
    <div>
      {loading && (
        <div className="lg:ml-0 ml-2 mb-2 grid grid-cols-2  gap-2 lg:mt-4 mt-0">
          <Skeleton style={{ borderRadius: 5 }} variant="rectangular" width="100%" height={100} />
          <Skeleton style={{ borderRadius: 5 }} variant="rectangular" width="100%" height={100} />
        </div>
      )}
      {!loading && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {datSet[0] && (
          <>
           {/* First Image */}
           <div className="">
            <div className="w-full h-40 relative">
              <img alt={datSet[0].name} src={datSet[0].image} className="rounded" />
            </div>
          </div>

          {/* Second Image */}
          <div className="">
            <div className="w-full h-40 relative">
              <img alt={datSet[1].name} src={datSet[1].image} className="object-cover rounded" />
            </div>
          </div>
          </>
        )}
         
        </div>
      )}
    </div>
  );
};

export default TwoImageBannerComponent;

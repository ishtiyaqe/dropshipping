import { useEffect, useState } from 'react';
import clients from '../../components/api/client';
import Skeleton from '@mui/material/Skeleton';

const FutureBrandsComponent = () => {
  const [datSet, setDatSet] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch data from the API
        const response = await clients.get('/Home_bottom_sites_Banneer');
        const datas = response.data.Home_banner.map((item) => item);

        // Log data for debugging (you can remove these lines in production)
     

        setDatSet(datas);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    // Simulate a 5-second delay before fetching data
    setTimeout(fetchData, 5000); // 5-second delay
  }, [setDatSet]);

  return (
    <div>
      <div className='text-xl font-black mb-4'>Featured Brands</div>
      <div className='bg-white grid lg:grid-cols-3 grid-cols-1 justify-items-center gap-4 p-8 rounded shadow-md'>
      {loading && (
              <div className=' grid grid-cols-4  gap-4 '>
                <Skeleton style={{ borderRadius: 5 }} variant="rectangular" width="100%" height={30} />
              </div>
            )}
        {datSet.map((item) => (
          <div key={item.id}>
            <img className='h-10 opacity-75 w-32' src={item.image} alt={item.name} />
          </div>
        ))}
      </div>
    </div>
  );
};

export default FutureBrandsComponent;

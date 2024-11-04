import { useEffect, useState } from 'react';
import clients from '../../components/api/client';
import Skeleton from '@mui/material/Skeleton';
import { Link } from 'react-router-dom';

const CatagoryComponent = () => {
  const [datSet, setDatSet] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch data from the API
        const response = await clients.get('/CatagorysList');

        const datas = response.data.Catagory_list;

        setDatSet(datas);
        setLoading(false);

      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    };

    // Simulate a 5-second delay before fetching data
    setTimeout(fetchData); // 5-second delay
  }, [setDatSet]);

  return (
    <>
      {loading && (
              <div className='flex space-x-4'>
                <Skeleton style={{ borderRadius: 5 }} variant="rectangular" width="100%" height={80} />
                <Skeleton style={{ borderRadius: 5 }} variant="rectangular" width="100%" height={80} />
                <Skeleton style={{ borderRadius: 5 }} variant="rectangular" width="100%" height={80} />
              </div>
            )}
      <div className='grid lg:grid-cols-6 grid-cols-3 gap-5'>
        {datSet.map((item) => (
          <div key={item.id} className="bg-white rounded-md shadow-md">
            <Link to={`/search?query=${item.CategorName}`}>
              <div className="relative w-full">
                <img
                  src={item.image}
                  alt="category"
                  className="top-0 left-0 bottom-0 right-0 object-cover hover:object-none w-full h-full"
                />
                <div className="absolute py-2 text-center text-black bottom-0 right-1 left-1 p-2 hover:bg-black hover:text-white hover:opecity-75">
                  <h4 className="font-semibold text-base">{item.CategorName}</h4>
                </div>
              </div>
            </Link>
          </div>
        ))}
      </div>
    </>
  );
};

export default CatagoryComponent;

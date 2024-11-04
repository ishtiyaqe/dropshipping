import { useEffect, useState } from 'react';
import clients from '../../components/api/Client';

const SellerInfoComponent = ({ productNo }) => {
  const [sellerCurrentData, setSellerCurrentData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        
        const response = await clients.get(`/get_Sellerinfo/${productNo}`);
        const fetchedInfo = response.data.SellerInfo;
        setSellerCurrentData(fetchedInfo);
      
      } catch (error) {
        console.error('Error fetching seller info:', error);
      }
    };

    fetchData();
  }, [productNo]);


  return (
    <>
      <div className=' mt-4 p-4 border border-gray-400 rounded-md flex flex-col justify-center shadow-md dark:shadow-gray-200 '>
        <div className='text-center'>Seller Info</div>
        {sellerCurrentData.length > 0 && (
          <>
            <span className='text-sm font-bold'>Company name: {sellerCurrentData[0].seller}</span>
            <span className='text-sm font-bold'>Company Country: {sellerCurrentData[0].country}</span>
            <div className='flex justify-between'>
            {sellerCurrentData[0].year ? (
  <span className='text-sm font-bold'>Company Year: {sellerCurrentData[0].year}</span>
) : (
 <></>
)}

            </div>
          </>
        )}
      </div>
    </>
  );
};

export default SellerInfoComponent;

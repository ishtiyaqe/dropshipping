import { useEffect, useState } from 'react'
import clients from '../../components/api/client';
import Skeleton from '@mui/material/Skeleton';
import LocalShippingOutlinedIcon from '@mui/icons-material/LocalShippingOutlined';
import SavingsOutlinedIcon from '@mui/icons-material/SavingsOutlined';
import AccessAlarmsOutlinedIcon from '@mui/icons-material/AccessAlarmsOutlined';
import VerifiedUserOutlinedIcon from '@mui/icons-material/VerifiedUserOutlined';
const TextBannerComponent = () => {
  const [datSet, setDatSet] = useState([]);
  const [loading, setLoading] = useState(true);
  
  
  
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch images from the API
        const response = await clients.get('/Home_4data_breadcum');
       

        const datas = response.data.Catagory_list.map((item) => item);
        
        
        
        
        setDatSet(datas);
        setLoading(false);
   
      } catch (error) {
        console.error('Error fetching images:', error);
      }
    };

    // Simulate a 5-second delay before fetching images
    setTimeout(fetchData); // 5-second delay
  }, [setDatSet]);
  return (
    <div>
        <div className="grid lg:grid-cols-4 grid-cols-1 gap-3 bg-white p-6 m-2 lg:m-0 ">
       {loading && (
              <div className='lg:ml-0 ml-2 mb-2 grid grid-cols-1  gap-2 lg:mt-4 mt-0'>
                <Skeleton style={{ borderRadius: 5 }} variant="rectangular" width='100%' height={60} />
                <Skeleton style={{ borderRadius: 5 }} variant="rectangular" width='100%' height={60} />
                <Skeleton style={{ borderRadius: 5 }} variant="rectangular" width='100%' height={60} />
                <Skeleton style={{ borderRadius: 5 }} variant="rectangular" width='100%' height={60} />
              </div>
            )}
            {!loading && (
              <>
              {datSet[0] && (
                <>
 <div className='flex lg:justify-center justify-start lg:border-r lg:border-gray-800'>

<LocalShippingOutlinedIcon className='w-10 h-20 self-center mr-4 ' />
<div className="">
  <h4 className="font-semibold text-lg text-blue-700">{datSet[0].name}</h4>
  <span className="text-sm text-gray-600">{datSet[0].Text}</span>
</div>
</div>
<div className='flex lg:justify-center justify-start lg:border-r lg:border-gray-800'>

<SavingsOutlinedIcon className='w-10 h-20 self-center mr-4 ' />
<div className="">
  <h4 className="font-semibold text-lg text-blue-700">{datSet[1].name}</h4>
  <span className="text-sm text-gray-600">{datSet[1].Text}</span>
</div>
</div>
<div className='flex lg:justify-center justify-start lg:border-r lg:border-gray-800'>

<AccessAlarmsOutlinedIcon className='w-10 h-20 self-center mr-4 ' />
<div className="">
  <h4 className="font-semibold text-lg text-blue-700">{datSet[2].name}</h4>
  <span className="text-sm text-gray-600">{datSet[2].Text}</span>
</div>
</div>
<div className='flex lg:justify-center justify-start '>

<VerifiedUserOutlinedIcon className='w-10 h-20 self-center mr-4 ' />
<div className="">
  <h4 className="font-semibold text-lg text-blue-700">{datSet[3].name}</h4>
  <span className="text-sm text-gray-600">{datSet[3].Text}</span>
</div>
</div>
                </>
              )}
         
              </>)}


        </div>
    </div>
  )
}

export default TextBannerComponent
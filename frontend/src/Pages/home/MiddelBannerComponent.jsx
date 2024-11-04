import { useEffect, useState } from 'react'
import './asset/MiddleBanner.css'
import clients from '../../components/api/client';
import Skeleton from '@mui/material/Skeleton';
const MiddelBannerComponent = () => {
    const [datSet, setDatSet] = useState([]);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
      const fetchData = async () => {
        try {
          // Fetch images from the API
          const response = await clients.get('/Home_middel502x202px_Banneer');
         
  
          const datas = response.data.Home_banner.map((item) => item);

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
            <div className='sc-1567ca4f-0 kINchA'>
            <div spacing="5" className="sc-4874dbe1-0 ieriCy">
            {loading && (
              <div className='lg:ml-0 ml-2 mb-2 grid grid-cols-1  gap-2 lg:mt-4 mt-0'>
                <Skeleton style={{ borderRadius: 5 }} variant="rectangular" width='100%' height={30} />
                <Skeleton style={{ borderRadius: 5 }} variant="rectangular" width='100%' height={30} />
                <Skeleton style={{ borderRadius: 5 }} variant="rectangular" width='100%' height={30} />
              </div>
            )}
              {datSet.length > 0 && (
            <>
              {/* Check if the first element exists before accessing its properties */}
              {datSet[0].title && (
                <>
                <div spacing="5" className="sc-4874dbe1-0 gpweuD text-black border-gray-300 border-t-2 border-b-2 border-l-2 border-dashed ">
                    <div className="sc-19ecb654-0 sc-3868d290-0 kihmmo fvaaoH">
                        <img alt={datSet[0].title} height="100%" width="100%" src={datSet[0].image} className="sc-b68cbd4b-0 fkpIxg" />
                        <div className="sc-19ecb654-0 sc-3868d290-1 kihmmo izGqcq">
                            <p className="sc-db80def1-0 hjRAHU">{datSet[0].title}</p>
                            <h4 dangerouslySetInnerHTML={{ __html: datSet[0].slogan }} />
                            <a href={datSet[0].url}><span className="sc-6bdf4176-0 dFHnDJ">Shop Now</span></a>
                        </div>
                    </div>
                </div>
                <div spacing="5" className="sc-4874dbe1-0 gpweuD text-black border-2 border-dashed border-gray-300">
                    <div className="sc-19ecb654-0 sc-3868d290-0 kihmmo fvaaoH">
                        <img alt={datSet[1].title} height="100%" width="100%" src={datSet[1].image} className="sc-b68cbd4b-0 fkpIxg" />
                        <div className="sc-19ecb654-0 sc-3868d290-1 kihmmo izGqcq">
                            <p color="white" className="sc-db80def1-0 bha-DRn">BEST SELLER</p>
                            <h4 dangerouslySetInnerHTML={{ __html: datSet[1].slogan }} />
                            <a href={datSet[1].url}><span style={{ color: 'white' }} className="sc-6bdf4176-0 dFHnDJ">Shop Now</span></a>
                        </div>
                    </div>
                </div>
                <div spacing="5" className="sc-4874dbe1-0 gpweuD text-black border-t-2 border-b-2 border-r-2 border-dashed border-gray-300">
                    <div className="sc-19ecb654-0 sc-3868d290-0 kihmmo fvaaoH">
                        <img alt={datSet[2].title} height="100%" width="100%" src={datSet[2].image} className="sc-b68cbd4b-0 fkpIxg" />
                        <div className="sc-19ecb654-0 sc-3868d290-1 kihmmo izGqcq">
                            <p className="sc-db80def1-0 hjRAHU">NEW ARRIVALS</p>
                            <h4 dangerouslySetInnerHTML={{ __html: datSet[2].slogan }} />
                            <a href={datSet[2].url}><span className="sc-6bdf4176-0 dFHnDJ">Shop Now</span></a>
                        </div>
                    </div>
                </div>
                </>
                     )}
                 </>
                 )}
            </div>
            </div>
        </div>
    )
}

export default MiddelBannerComponent